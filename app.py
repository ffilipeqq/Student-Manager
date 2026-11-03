from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file

from datetime import datetime

from pathlib import Path
import csv

from pytools.flaskTools import authenticate_user, is_admin, is_logged_in
from pytools.sqlTools import sql_commit, sql_fetch, os
from pytools.validationTools import clean_text, validate_login, validate_student

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

STUDENTS_TABLE = "students"
EXPORT_DIR = Path(app.instance_path) / "exports"
EXPORT_FILE = EXPORT_DIR / "students.csv"
LOG_FILE = Path("instance/log/export_log.log")

def create_export(students, filename):
    EXPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    export_file = EXPORT_DIR / filename
    with export_file.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "name", "course"]
        )
        writer.writeheader()
        writer.writerows(students)

    return export_file


@app.post("/students/export")
def export_students():
    if not is_logged_in():
        return redirect(url_for("login"))

    students = sql_fetch("""
                SELECT id, name, course
                FROM students
                ORDER BY id""", fetch_type="all") or []
    create_export(students, "students.csv")

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:
        file.write(f"{datetime.now()} | Export generated.\n")

    return send_file(
        EXPORT_FILE,
        as_attachment=True,
        download_name="students.csv",
        mimetype="text/csv"
    )


@app.post("/students/export/course")
def export_students_by_course():
    if not is_logged_in():
        return redirect(url_for("login"))

    course = clean_text(request.form.get("course", ""))
    if not course:
        flash("Please choose a course to export.", "error")
        return redirect(url_for("students"))

    students = sql_fetch(
        f"""SELECT id, name, course
            FROM {STUDENTS_TABLE}
            WHERE course = %s
            ORDER BY id""",
        (course,),
        fetch_type="all",
    ) or []

    if not students:
        flash("No students found for that course.", "error")
        return redirect(url_for("students"))

    export_file = create_export(students, "students-by-course.csv")
    return send_file(
        export_file,
        as_attachment=True,
        download_name="students-by-course.csv",
        mimetype="text/csv"
    )


@app.get("/students/export/preview")
def preview_export():
    if not is_logged_in():
        return redirect(url_for("login"))

    if not EXPORT_FILE.is_file():
        return "No export file found.", 404

    with EXPORT_FILE.open(
        'r',
        newline="",
        encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    return render_template(
        "export_preview.html",
        rows=rows
    )

@app.post("/students/export/delete")
def delete_export():
    if not is_logged_in():
        return redirect(url_for("login"))

    try:
        EXPORT_FILE.unlink(missing_ok=True)
    except OSError:
        app.logger.exception(
            "Could not delete CSV export"
        )

        return "Could not delete the export.", 500

    flash("Export deleted successfully.", "success")
    return redirect(url_for("students"))


@app.route("/compare")
def compare():
    if not is_logged_in():
        return redirect(url_for("login"))

    sql_records = 0
    csv_records = 0

    sql_records = sql_fetch(
            f"""SELECT COUNT(*_)
                AS sql_records
                FROM {STUDENTS_TABLE}""",
            fetch_type="all",
        ) or []

    with EXPORT_FILE.open(
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            csv_records += 1
    

@app.route("/students")
def students():
    if not is_logged_in():
        return redirect(url_for("login"))

    students = sql_fetch(
        f"SELECT id, name, email, course FROM {STUDENTS_TABLE}"
    ) or []
    courses = sql_fetch(
        f"""SELECT DISTINCT course
            FROM {STUDENTS_TABLE}
            WHERE course IS NOT NULL AND course <> ''
            ORDER BY course""",
        fetch_type="all",
    ) or []
    return render_template("students.html", students=students, courses=courses)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if not is_admin():
        return redirect(url_for("login"))

    name = ""
    email = ""
    course = ""

    if request.method == "POST":
        name = clean_text(request.form.get("name", ""))
        email = clean_text(request.form.get("email", ""))
        course = clean_text(request.form.get("course", ""))
        errors = validate_student(name, email, course)

        if not errors:
            saved = sql_commit(
                f"INSERT INTO {STUDENTS_TABLE} (name, email, course) "
                "VALUES (%s, %s, %s)",
                (name, email, course),
            )
            if not saved:
                return render_template(
                    "add_student.html",
                    name=name,
                    email=email,
                    course=course,
                )

            flash("Student added successfully.", "success")
            return redirect(url_for("students"))

        for error in errors:
            flash(error, "error")

    return render_template(
        "add_student.html",
        name=name,
        email=email,
        course=course,
    )


@app.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    if not is_admin():
        return redirect(url_for("login"))

    name = ""
    email = ""
    course = ""

    if request.method == "POST":
        name = clean_text(request.form.get("name", ""))
        email = clean_text(request.form.get("email", ""))
        course = clean_text(request.form.get("course", ""))
        errors = validate_student(name, email, course)

        if not errors:
            saved = sql_commit(
                f"UPDATE {STUDENTS_TABLE} SET name = %s, email = %s, "
                "course = %s WHERE id = %s",
                (name, email, course, student_id),
            )
            if not saved:
                return render_template(
                    "edit_student.html",
                    student={
                        "id": student_id,
                        "name": name,
                        "email": email,
                        "course": course,
                    },
                )

            flash("Student updated successfully.", "success")
            return redirect(url_for("students"))

        for error in errors:
            flash(error, "error")

    student = sql_fetch(
        f"SELECT id, name, email, course FROM {STUDENTS_TABLE} WHERE id = %s",
        (student_id,),
        "one",
    )
    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("students"))

    if request.method == "POST":
        student.update(name=name, email=email, course=course)

    return render_template("edit_student.html", student=student)


@app.route("/students/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if not is_admin():
        return redirect(url_for("login"))

    deleted = sql_commit(
        f"DELETE FROM {STUDENTS_TABLE} WHERE id = %s",
        (student_id,),
    )
    if not deleted:
        return redirect(url_for("students"))

    flash("Student deleted successfully.", "success")
    return redirect(url_for("students"))


@app.route("/present", methods=["GET", "POST"])
def present():
    if not is_logged_in():
        return redirect(url_for("login"))

    name = ""
    course = ""
    if request.method == "POST":
        name = clean_text(request.form.get("name", ""))
        course = clean_text(request.form.get("course", ""))
        errors = validate_student(name, "student@example.com", course)

        if not errors:
            return render_template(
                "present.html",
                name=name,
                course=course,
                submitted=True,
            )

        for error in errors:
            flash(error, "error")

    return render_template(
        "present.html",
        name=name,
        course=course,
        submitted=False,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        errors = validate_login(username, password)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("login.html")

        role = authenticate_user(username, password)
        if role:
            session["username"] = username
            session["role"] = role
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    rows = sql_fetch("""SELECT course, COUNT(*) AS total
                FROM students
                GROUP BY course
                ORDER BY total DESC""", fetch_type="all")

    course_counts = [
        {"course": row["course"], "total": row["total"]}
        for row in rows
    ]

    total_students = sum(
        row["total"] for row in course_counts
    )

    max_count = max(
        (row["total"] for row in course_counts), 
        default = 1
    )
    
    return render_template("dashboard.html",
                           course_counts=course_counts,
                           total_students=total_students,
                           max_count=max_count,
                           username = session["username"])

if __name__ == "__main__":
    app.run(debug=True)
