import threading
from threading import Thread

import iso8601
import re
import pytz
from canvasapi import Canvas
from canvasapi.exceptions import ResourceDoesNotExist
from canvasapi.requester import Requester

import canvas.routes
from canvas import db
from canvas.models import ClassList


def create_data(class_name, assignment, due, assignment_grade, score, submission_type, url):
    data = ClassList(course=class_name, assignment=assignment, due=due, assignment_grade=assignment_grade,
                     total_score=score, url=url)
    does_exist = bool(ClassList.query.filter_by(assignment=assignment).first())

    if not does_exist:
        if data.assignment not in canvas.routes.deleted_entries:
            db.session.add(data)
            db.session.commit()


class AutoCanvas:
    def __init__(self):
        self.API_URL = "https://test.instructure.com"
        self.API_KEY = "your_apikey"

        self.account_id = 6681700
        self.requester = Requester(self.API_URL, self.API_KEY)
        self.canvas = Canvas(self.API_URL, self.API_KEY)
        self.account = self.canvas.get_user(self.account_id)

        self.timezone = pytz.timezone('America/New_York')

    def get_current_class_ids(self, semester):
        course_list = []
        course_ids = []

        try:
            courses = self.account.get_courses()

            for course in courses:
                if semester in course.name:
                    # print(course)
                    # print()
                    course_list.append(str(course))
        except AttributeError:
            pass

        for find_course in course_list:
            regex = re.findall(r"(?<=\()(.*?)(?=\))", find_course)

            for each in regex:
                if each.isdigit():
                    course_ids.append(each)

        return course_ids

    def get_class_by_id(self, class_id):
        single_class = self.canvas.get_course(class_id)
        return single_class

    def get_class_by_name(self, class_name):
        single_class = self.account.get_courses(search_by="course", search_term=class_name)
        return single_class

    def get_users_in_class(self, class_id):
        class_name = self.canvas.get_course(class_id)

        class_users = class_name.get_users()
        for user in class_users:
            print(user)

    def get_assignment_ids_in_classes(self, semester):
        classes = self.get_current_class_ids(semester)
        assignment_list = []
        assignment_ids = []

        for each in classes:
            course = self.canvas.get_course(each)
            user_assignments = course.get_assignments()

            for assignment in user_assignments:
                # print(assignment)
                assignment_list.append(assignment)

        for find_assignment in assignment_list:
            regex = re.findall(r"(?<=\()(.*?)(?=\))", str(find_assignment))

            for reg in regex:
                if reg.isdigit():
                    assignment_ids.append(reg)

        return assignment_ids

    def get_class_grade(self, class_id):
        single_class = self.get_class_by_id(class_id)

        get_enrollment = single_class.get_enrollments(user_id=self.account_id)
        for enrollment in get_enrollment:
            class_grade = enrollment

            return class_grade.grades["current_score"]

    def get_all_assignment_details(self, semester, create=True):
        all_classes = self.get_current_class_ids(semester)
        all_assignments = self.get_assignment_ids_in_classes(semester)

        for class_id in all_classes:
            single_class = self.get_class_by_id(class_id)

            print(single_class.name)
            print(self.get_class_grade(class_id))
            print()
            for assignment in all_assignments:
                try:
                    single_assignment = single_class.get_assignment(assignment, all_dates=True)
                    raw_due = str(single_assignment.all_dates[0]["due_at"])

                    get_assignment_grade = single_class.get_submission(single_assignment, self.account).entered_score

                    try:
                        assignment_due = iso8601.parse_date(raw_due). \
                            astimezone(self.timezone).strftime("%a, %B %d %Y, %H:%M:%S")
                    except iso8601.ParseError:
                        assignment_due = "No due date"
                        pass

                    print(single_assignment.name, ":", assignment_due, ":",
                          single_assignment.submission_types, ":", single_assignment.points_possible)

                    if create:
                        create_data(single_class.course_code, single_assignment.name,
                                    assignment_due, str(get_assignment_grade),
                                    str(single_assignment.points_possible),
                                    str(single_assignment.submission_types), str(single_assignment.html_url))

                except ResourceDoesNotExist:
                    pass

    def get_all_assignment_details_by_class_id(self, semester, class_id, create=True):
        all_assignments = self.get_assignment_ids_in_classes(semester)

        single_class = self.get_class_by_id(class_id)

        print()
        print(single_class.name)
        print(self.get_class_grade(class_id))
        print()
        for assignment in all_assignments:
            try:
                single_assignment = single_class.get_assignment(assignment, all_dates=True)
                raw_due = str(single_assignment.all_dates[0]["due_at"])

                get_assignment_grade = single_class.get_submission(single_assignment, self.account).entered_score
                try:
                    assignment_due = iso8601.parse_date(raw_due). \
                        astimezone(self.timezone).strftime("(%m/%d/%Y) %a, %B %d %Y, %H:%M:%S")
                except iso8601.ParseError:
                    assignment_due = "No due date"
                    pass

                print(single_assignment.name, ":", assignment_due, ":",
                      single_assignment.submission_types, ":", single_assignment.points_possible)

                if create:
                    create_data(single_class.course_code, single_assignment.name, assignment_due, get_assignment_grade,
                                single_assignment.points_possible,
                                single_assignment.submission_types, single_assignment.html_url)
            except ResourceDoesNotExist:
                pass

    def get_all_assignment_details_by_class_name(self, semester, class_name, create=True):
        all_assignments = self.get_assignment_ids_in_classes(semester)

        single_class = self.get_class_by_name(class_name)
        for course in single_class:
            print(course)

        print()
        print(single_class.name)
        print(self.get_class_grade(class_name))
        print()
        for assignment in all_assignments:
            try:
                single_assignment = single_class.get_assignment(assignment, all_dates=True)
                raw_due = str(single_assignment.all_dates[0]["due_at"])

                get_assignment_grade = single_class.get_submission(single_assignment, self.account).entered_score
                try:
                    assignment_due = iso8601.parse_date(raw_due). \
                        astimezone(self.timezone).strftime("(%m/%d/%Y) %a, %B %d %Y, %H:%M:%S")
                except iso8601.ParseError:
                    assignment_due = "No due date"
                    pass

                print(single_assignment.name, ":", assignment_due, ":",
                      single_assignment.submission_types, ":", single_assignment.points_possible)

                if create:
                    create_data(single_class.course_code, single_assignment.name, assignment_due, get_assignment_grade,
                                single_assignment.points_possible,
                                single_assignment.submission_types, single_assignment.html_url)
            except ResourceDoesNotExist:
                pass

    # testing
    def get_todo_items(self):
        events = self.canvas.get_upcoming_events()

        for event in events:
            print(event)
            print()
            for key, value in event.items():
                print("Key:", key)
                print("Value:", value)
                print()

    def get_accounts(self):
        accounts = self.canvas.search_all_courses(search="ICT552")
        return accounts


def main():
    canvas = AutoCanvas()
    class_list = canvas.get_current_class_ids("Fall 2019")
    # canvas.get_all_assignment_details_by_class_name("Fall 2019", "ICT552-201", create=False)

    for course in class_list:
        thread = Thread(target=canvas.get_all_assignment_details_by_class_id, args=("Fall 2019", course,))
        thread.start()

    for t in threading.enumerate():
        t.join(20) if t is not threading.currentThread() else None


if __name__ == "__main__":
    main()
