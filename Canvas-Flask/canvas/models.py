from canvas import db


class ClassList(db.Model):
    __tablename__ = "class_list"
    
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    course = db.Column('course', db.String)
    assignment = db.Column('assignment', db.String)
    due = db.Column('due', db.String)
    assignment_grade = db.Column('assignment_grade', db.String)
    total_score = db.Column('total_score', db.Float)
    # deleted = db.Column('deleted', db.String)
    url = db.Column('url', db.String)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"ClassList('{self.id}', '{self.course}', '{self.assignment}', '{self.due}'," \
            f" '{self.assignment_grade}', '{self.total_score}', '{self.url}')"
