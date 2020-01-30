"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def homepage():

    student_rows = hackbright.get_students()

    project_rows = hackbright.get_projects()


    return render_template("homepage.html", student_rows=student_rows, 
                                            project_rows=project_rows)


@app.route("/new-student-form")
def student_form():

    return render_template("student_add.html")


@app.route("/student-add", methods=['GET', 'POST'])
def student_add():
    """Add a student."""

    github = request.form.get('github')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("redirect_to_student_info.html", github=github)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           rows=rows)
    return html

@app.route("/project")
def show_project_info():

    title = request.args.get('title')
    row_title = hackbright.get_project_by_title(title)  

    description = row_title[1]
    max_grade = row_title[2]

    rows_grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", title=title,
                                                description=description,
                                                max_grade=max_grade,
                                                rows_grades=rows_grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
