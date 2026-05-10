from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "students.txt"

app = Flask(__name__)
app.secret_key = "student-grade-manager-dev-key"


def load_students():
    students = []

    if not DATA_FILE.exists():
        return students

    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("#")

            if len(parts) != 3:
                continue

            student_id = parts[0].strip()
            student_name = parts[1].strip()
            grades_text = parts[2].strip()

            try:
                grades = [] if grades_text == "" else [
                    float(grade) for grade in grades_text.split()
                ]
            except ValueError:
                continue

            students.append({
                "id": student_id,
                "name": student_name,
                "grades": grades,
            })

    return students


def save_students(students):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        for student in students:
            grades_text = " ".join(str(float(grade)) for grade in student["grades"])
            file.write(f'{student["id"]}# {student["name"]}# {grades_text}\n')


def find_student(students, student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def parse_grade(raw_grade):
    try:
        grade = float(raw_grade)
    except (TypeError, ValueError):
        raise ValueError("Grade must be a number.")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100.")

    return grade


def parse_grade_list(raw_grades):
    cleaned_text = raw_grades.replace(",", " ").strip()

    if cleaned_text == "":
        return []

    return [parse_grade(item) for item in cleaned_text.split()]


def average_grade(grades):
    if len(grades) == 0:
        return None
    return sum(grades) / len(grades)


def status_for_average(average):
    if average is None:
        return "No Tests"
    if average >= 80:
        return "Strong"
    if average >= 60:
        return "Steady"
    return "Needs Focus"


def enrich_students(students):
    enriched = []

    for student in students:
        average = average_grade(student["grades"])
        enriched.append({
            **student,
            "average": average,
            "status": status_for_average(average),
            "tests": len(student["grades"]),
        })

    return enriched


def summarize(students):
    all_grades = [
        grade
        for student in students
        for grade in student["grades"]
    ]
    graded_students = [
        student
        for student in students
        if student["average"] is not None
    ]
    top_student = max(
        graded_students,
        key=lambda student: student["average"],
        default=None,
    )

    return {
        "total_students": len(students),
        "total_grades": len(all_grades),
        "max_tests": max((student["tests"] for student in students), default=0),
        "class_average": average_grade(all_grades),
        "top_student": top_student,
        "needs_focus": len([
            student for student in students
            if student["average"] is not None and student["average"] < 60
        ]),
        "empty_students": len([
            student for student in students
            if student["average"] is None
        ]),
    }


@app.template_filter("grade_tone")
def grade_tone(grade):
    if grade >= 80:
        return "grade-high"
    if grade >= 60:
        return "grade-mid"
    return "grade-low"


@app.template_filter("format_average")
def format_average(value):
    if value is None:
        return "No tests"
    return f"{value:.1f}"


@app.route("/")
def index():
    query = request.args.get("q", "").strip().lower()
    students = enrich_students(load_students())
    stats = summarize(students)

    if query:
        visible_students = [
            student for student in students
            if query in student["id"].lower() or query in student["name"].lower()
        ]
    else:
        visible_students = students

    return render_template(
        "index.html",
        students=visible_students,
        all_students=students,
        stats=stats,
        query=query,
        focus=request.args.get("focus", ""),
    )


@app.post("/students")
def add_student():
    students = load_students()
    student_id = request.form.get("student_id", "").strip()
    name = request.form.get("name", "").strip()
    raw_grades = request.form.get("grades", "")

    if student_id == "" or name == "":
        flash("Student ID and name are required.", "error")
        return redirect(url_for("index"))

    if "#" in student_id or "#" in name:
        flash("Student ID and name cannot contain #.", "error")
        return redirect(url_for("index"))

    if find_student(students, student_id) is not None:
        flash("A student with that ID already exists.", "error")
        return redirect(url_for("index"))

    try:
        grades = parse_grade_list(raw_grades)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))

    students.append({
        "id": student_id,
        "name": name,
        "grades": grades,
    })
    save_students(students)
    flash(f"{name} was added successfully.", "success")
    return redirect(url_for("index", focus=student_id))


@app.post("/grades/update")
def update_grade():
    students = load_students()
    student_id = request.form.get("student_id", "").strip()
    raw_quiz_number = request.form.get("quiz_number", "").strip()
    raw_grade = request.form.get("grade", "").strip()
    student = find_student(students, student_id)

    if student is None:
        flash("Student ID was not found.", "error")
        return redirect(url_for("index"))

    try:
        quiz_number = int(raw_quiz_number)
    except ValueError:
        flash("Quiz number must be a whole number.", "error")
        return redirect(url_for("index", focus=student_id))

    try:
        grade = parse_grade(raw_grade)
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index", focus=student_id))

    current_test_count = len(student["grades"])

    if quiz_number < 1:
        flash("Quiz number must be 1 or higher.", "error")
        return redirect(url_for("index", focus=student_id))

    if quiz_number <= current_test_count:
        student["grades"][quiz_number - 1] = grade
        message = f"Updated Test {quiz_number} for {student['name']}."
    elif quiz_number == current_test_count + 1:
        student["grades"].append(grade)
        message = f"Added Test {quiz_number} for {student['name']}."
    else:
        next_test_number = current_test_count + 1
        flash(
            f"Fill Test {next_test_number} for {student['name']} before Test {quiz_number}.",
            "error",
        )
        return redirect(url_for("index", focus=student_id))

    save_students(students)
    flash(message, "success")
    return redirect(url_for("index", focus=student_id))


@app.post("/tests/add")
def add_test_for_all():
    students = load_students()

    if len(students) == 0:
        flash("No student records found.", "error")
        return redirect(url_for("index"))

    new_grades = []

    try:
        for student in students:
            raw_grade = request.form.get(f"grade_{student['id']}", "").strip()
            if raw_grade == "":
                raise ValueError("Enter a grade for every student.")
            new_grades.append((student, parse_grade(raw_grade)))
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("index"))

    for student, grade in new_grades:
        student["grades"].append(grade)

    save_students(students)
    flash("New test grades were added for the whole class.", "success")
    return redirect(url_for("index"))


@app.post("/students/<student_id>/delete")
def delete_student(student_id):
    students = load_students()
    student = find_student(students, student_id)

    if student is None:
        flash("Student ID was not found.", "error")
        return redirect(url_for("index"))

    students = [
        current_student for current_student in students
        if current_student["id"] != student_id
    ]
    save_students(students)
    flash(f"{student['name']} was deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
