# TODO: Get details for individual class

from flask import url_for, redirect, flash, render_template, request, jsonify

from canvas import db, app
from canvas.models import ClassList

from scripts.my_canvas import AutoCanvas, main, create_data

from sqlalchemy import text

global deleted_entries
deleted_entries = []


@app.route("/setup/home")
def setup_home():
    sql_query = text("select class_list.id, class_list.course, class_list.assignment, class_list.due, "
                     "class_list.assignment_grade, class_list.total_score, class_list.url from class_list")
    # execute
    result = db.engine.execute(sql_query)

    results_to_dict = [dict(row.items()) for row in result]
    results_to_list = []

    for i in results_to_dict:
        i.update({"remove": "remove"})
        results_to_list.append(i)

    final_results = {"data": results_to_dict}
    return jsonify(final_results)


@app.route("/")
@app.route("/home")
def home():
    return render_template("pages/home.html")


@app.route("/create_data")
def create_data():
    main()
    return redirect(url_for("home"))


@app.route("/delete/data")
def delete_data():
    db.session.query(ClassList).delete()
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete_entry(id):
    entry = ClassList.query.get(id)
    deleted_entries.append(entry.assignment)

    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/removed_data")
def delete_removed_data():
    del deleted_entries[:]
    return redirect(url_for("home"))
