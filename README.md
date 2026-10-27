# Student Analytics – Performance Analytics Dashboard

A beginner-friendly academic performance dashboard built with Python, Flask, SQLite, HTML, CSS, JavaScript, and Chart.js. It includes a CSV dataset that can also be imported into Power BI.

## Features
- KPI cards for student count, average marks, attendance, and pass rate
- Subject performance bar chart
- Grade-band doughnut chart
- Attendance chart
- Department, semester, and student search filters
- Student records table with average marks and status
- JSON API at `/api/students`
- Filtered CSV export at `/export.csv`
- SQLite database initialized automatically from `data/students.csv`

## Important data note
The included student records are fictional sample data for learning. Do not represent them as real student results. The demo uses average marks >= 40 as a pass threshold; change it to match your institution's actual policy if you adapt the project.

## Run on macOS using VS Code
Recommended: Python 3.10 or 3.11.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. Keep the terminal open while the app is running. Press Control+C to stop it.

The charts use Chart.js from a CDN, so charts require an internet connection. The Flask app and SQLite database run locally.

## Project structure
- `app.py` – routes, filtering, KPI calculations, CSV export, and database setup
- `data/students.csv` – fictional sample records
- `templates/` – HTML templates
- `static/css/style.css` – responsive dashboard styling
- `students.db` – generated automatically and excluded from Git

## Use the data in Power BI
1. Open Power BI Desktop (Windows is generally the supported desktop environment; on Mac, use an available Windows environment or Power BI Service where suitable).
2. Select **Get data → Text/CSV**.
3. Choose `data/students.csv` and load it.
4. Create measures such as average marks, average attendance, and student count.
5. Add bar, doughnut, and slicer visuals for department and semester.

For an assignment or portfolio, you can include both the web dashboard and a separate Power BI report. The Power BI report is not automatically embedded into this Flask app in this starter version.

## Push to GitHub
From the project folder in the VS Code terminal:

```bash
git init
git add .
git commit -m "Build student analytics dashboard"
```

Then create an empty repository on GitHub and follow GitHub's instructions to add the remote and push. Do not upload real student personal data. The `.gitignore` excludes the generated database and virtual environment.

## Suggested next improvements
- Add a student details page
- Add upload/validation for a new CSV file
- Add login with securely hashed passwords if needed
- Add date/semester-wise trends once historical data exists
- Add automated tests and document the dataset and grading policy
