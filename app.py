"""Student Analytics Dashboard: a beginner-friendly Flask + SQLite project."""
from pathlib import Path
import csv
import sqlite3
from flask import Flask, jsonify, render_template, request, Response

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'students.db'
CSV_PATH = BASE_DIR / 'data' / 'students.csv'
app = Flask(__name__)


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def seed_database():
    """Create tables and load demo records from CSV only when the table is empty."""
    with connect_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            student_name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL,
            attendance REAL NOT NULL,
            math_marks REAL NOT NULL,
            science_marks REAL NOT NULL,
            programming_marks REAL NOT NULL
        )''')
        count = db.execute('SELECT COUNT(*) FROM students').fetchone()[0]
        if count == 0 and CSV_PATH.exists():
            with CSV_PATH.open(newline='', encoding='utf-8') as file:
                rows = csv.DictReader(file)
                db.executemany('''INSERT INTO students
                    (student_id, student_name, department, semester, attendance,
                     math_marks, science_marks, programming_marks)
                    VALUES (:student_id, :student_name, :department, :semester, :attendance,
                            :math_marks, :science_marks, :programming_marks)''', list(rows))


def get_filters():
    department = request.args.get('department', '').strip()
    semester = request.args.get('semester', '').strip()
    search = request.args.get('search', '').strip()
    return department, semester, search


def filtered_students():
    department, semester, search = get_filters()
    sql = 'SELECT * FROM students WHERE 1=1'
    params = []
    if department:
        sql += ' AND department = ?'
        params.append(department)
    if semester:
        sql += ' AND semester = ?'
        params.append(semester)
    if search:
        sql += ' AND (student_name LIKE ? OR student_id LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    sql += ' ORDER BY student_name'
    with connect_db() as db:
        return db.execute(sql, params).fetchall()


def row_to_dict(row):
    item = dict(row)
    marks = [item['math_marks'], item['science_marks'], item['programming_marks']]
    item['average'] = round(sum(marks) / len(marks), 1)
    item['status'] = 'Pass' if item['average'] >= 40 else 'Needs support'
    return item


@app.route('/')
def dashboard():
    students = [row_to_dict(row) for row in filtered_students()]
    with connect_db() as db:
        departments = [r['department'] for r in db.execute('SELECT DISTINCT department FROM students ORDER BY department')]
        semesters = [r['semester'] for r in db.execute('SELECT DISTINCT semester FROM students ORDER BY semester')]
    count = len(students)
    avg_marks = round(sum(s['average'] for s in students) / count, 1) if count else 0
    avg_attendance = round(sum(s['attendance'] for s in students) / count, 1) if count else 0
    pass_rate = round(sum(s['average'] >= 40 for s in students) * 100 / count, 1) if count else 0
    chart_data = {
        'subjects': ['Mathematics', 'Science', 'Programming'],
        'subjectAverages': [round(sum(s[k] for s in students) / count, 1) if count else 0 for k in ['math_marks', 'science_marks', 'programming_marks']],
        'gradeLabels': ['Excellent (85+)', 'Good (70–84)', 'Average (50–69)', 'Needs support (<50)'],
        'gradeCounts': [
            sum(s['average'] >= 85 for s in students),
            sum(70 <= s['average'] < 85 for s in students),
            sum(50 <= s['average'] < 70 for s in students),
            sum(s['average'] < 50 for s in students),
        ],
        'attendanceLabels': [s['student_name'].split()[0] for s in students[:10]],
        'attendanceValues': [s['attendance'] for s in students[:10]],
    }
    return render_template('index.html', students=students, departments=departments,
                           semesters=semesters, selected_department=request.args.get('department', ''),
                           selected_semester=request.args.get('semester', ''), search=request.args.get('search', ''),
                           count=count, avg_marks=avg_marks, avg_attendance=avg_attendance,
                           pass_rate=pass_rate, chart_data=chart_data)


@app.route('/api/students')
def api_students():
    return jsonify([row_to_dict(row) for row in filtered_students()])


@app.route('/export.csv')
def export_csv():
    students = [row_to_dict(row) for row in filtered_students()]
    output = Response(content_type='text/csv; charset=utf-8')
    output.headers['Content-Disposition'] = 'attachment; filename=student_analytics_export.csv'
    writer = csv.writer(output.stream)
    writer.writerow(['student_id', 'student_name', 'department', 'semester', 'attendance', 'math_marks', 'science_marks', 'programming_marks', 'average_marks', 'status'])
    for s in students:
        writer.writerow([s['student_id'], s['student_name'], s['department'], s['semester'], s['attendance'], s['math_marks'], s['science_marks'], s['programming_marks'], s['average'], s['status']])
    return output


seed_database()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
