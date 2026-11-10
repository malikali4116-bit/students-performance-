# Student Academic Performance Prediction and Improvement Support System

A modern, responsive, full-stack academic intelligence platform powered by **Machine Learning (Multiple Linear Regression with Scikit-learn)**, **Flask**, **Flask-SQLAlchemy**, **SQLite**, and **Bootstrap 5**.

The system helps students, educators, and institutional faculty understand student learning patterns, predict final examination performance based on continuous internal indicators, identify specific weak areas, and generate personalized, actionable improvement recommendations.

---

## 🌟 Key Modules & Features

1. **Dashboard Module (`/dashboard`)**:
   - 7 Key Performance Indicator (KPI) cards: Total Students, Average Attendance %, Average Assignment Marks, Average Internal Assessment Marks, Average Predicted Final Examination Marks, Students Performing Well (≥ 60%), Students Needing Improvement (< 60%).
   - 4 Dynamic interactive Chart.js charts:
     - **Student Performance Overview** (Bar Chart)
     - **Attendance Distribution** (Doughnut Chart)
     - **Actual vs Predicted Marks** (Line Chart)
     - **Performance Categories** (Pie Chart)
   - Real-time recent student activity table synced directly with SQLite.

2. **Student Management Module (`/students`)**:
   - Add new students with automatically generated sequential IDs (e.g., `STU-2026-001`).
   - View complete roster with instant search (by name, student ID, email) and multi-level filtering by Department and Academic Year.
   - Edit student profiles and delete students with confirmation modals.
   - View individual student academic snapshot modals.

3. **Attendance Management Module (`/attendance`)**:
   - Log working days and days attended with automatic real-time percentage calculation:
     $$\text{Attendance Percentage} = \left(\frac{\text{Days Attended}}{\text{Total Working Days}}\right) \times 100$$
   - Color-coded progress bars (Green ≥ 85%, Yellow 75–84%, Red < 75%).
   - Strict validation: days attended cannot exceed working days, no negative values, maximum 100%.
   - Full historical attendance logs per student.

4. **Academic Records Module (`/academic-records`)**:
   - Enter and update: Daily Study Hours (0–12 hrs), Assignment Marks (0–100), Internal Assessment Marks (0–100), Previous Semester Marks (0–100).
   - Enter **Actual Final Examination Marks** (0–100, optional / faculty entered).
   - Full data integrity: actual marks are stored separately and displayed only when entered by faculty.

5. **Machine Learning Prediction Module (`/prediction`)**:
   - Real, authentic Multiple Linear Regression model from Scikit-learn (`LinearRegression`).
   - Accepts 5 input features:
     1. Attendance Percentage (0–100)
     2. Daily Study Hours (0–12)
     3. Assignment Marks (0–100)
     4. Internal Assessment Marks (0–100)
     5. Previous Semester Marks (0–100)
   - Displays model evaluation metrics: **Mean Absolute Error (MAE)**, **Mean Squared Error (MSE)**, and **$R^2$ Score (86.0%)**.
   - Option to auto-populate from any enrolled student or simulate custom hypothetical scores.
   - Large attractive result card with predicted final marks (rounded to 2 decimal places, clamped to 0–100), performance classification tier, circular progress meter, diagnostic analysis, identified weak areas, and actionable next steps.
   - Performance categories:
     - **90–100**: Excellent
     - **75–89**: Very Good
     - **60–74**: Good
     - **40–59**: Average
     - **Below 40**: Needs Improvement

6. **Performance Analysis Module (`/performance`)**:
   - Student selector with multi-dimensional analytics.
   - 4 Interactive comparison charts:
     - **Academic Performance Comparison** (Radar chart: Student vs Class Average across 5 dimensions)
     - **Actual vs Predicted Marks** (Bar chart: Displays faculty-verified actual marks alongside ML predictions)
     - **Student Performance History** (Line chart)
     - **Attendance vs Final Marks** (Cohort Scatter plot)

7. **Improvement Recommendations Module (`/recommendations`)**:
   - Adaptive rule-based advisory engine.
   - Evaluates Attendance, Study Hours, Assignment Scores, Internal Assessments, and Foundational Prerequisite grades.
   - Produces targeted diagnostic narratives, priority badges (Critical, Moderate, On Track), and milestone action plans.

8. **Reports & Export Module (`/reports`)**:
   - **Individual Student Performance Report**: Official evaluation dossier with student info, attendance breakdown, academic metrics, ML prediction details, and remedial recommendations.
   - **Download as PDF**: Generates and downloads publication-grade PDF reports powered by ReportLab.
   - **Class Performance Report**: Cohort table with instant filtering.
   - **Export CSV**: Instant one-click CSV download of all students, academic metrics, predictions, and actual grades.
   - **Print Optimization**: Clean print layout formatted for paper or PDF printer.

9. **Settings Module (`/settings`)**:
   - Real-time ML model telemetry, regression coefficients ($\beta$ weights), and intercept display.
   - One-click ML model retraining trigger.
   - Database reset and sample re-seeding tool.
   - Institutional parameter overview.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask 3.1, Flask-SQLAlchemy 3.1
- **Database**: SQLite (`database/students.db`)
- **Machine Learning**: Scikit-learn (`LinearRegression`), Pandas, NumPy, Joblib
- **Document Generation**: ReportLab (PDF), Python `csv` (CSV)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Chart.js 4.4, Font Awesome 6

---

## 📁 Project Directory Structure

```
student_academic_performance/
│
├── app.py                     # Main Flask application and RESTful APIs
├── config.py                  # Database and path configuration
├── models.py                  # SQLAlchemy ORM models (Student, Attendance, AcademicRecord, Prediction)
├── seed_database.py           # Pre-populates 16 realistic student profiles and records
├── report_generator.py        # PDF and CSV report builder using ReportLab
├── requirements.txt           # Python dependency specifications
├── README.md                  # Comprehensive setup and usage documentation
│
├── dataset/
│   └── student_performance.csv # 500-sample academic dataset
│
├── ml/
│   ├── train_model.py         # Model training, validation, and evaluation script
│   ├── predict.py             # Inference pipeline and recommendation engine
│   ├── model.pkl              # Serialized Multiple Linear Regression model
│   └── model_metrics.json     # Saved evaluation metrics (MAE, MSE, R²)
│
├── database/
│   └── students.db            # SQLite database file (auto-generated)
│
├── templates/
│   ├── base.html              # Responsive base layout with sidebar and navbar
│   ├── dashboard.html         # KPI cards, 4 Chart.js charts, recent activity
│   ├── students.html          # Student management CRUD with modals
│   ├── attendance.html        # Attendance tracking and live calculation
│   ├── academic_records.html  # Continuous evaluations and actual marks
│   ├── prediction.html        # Machine Learning prediction studio
│   ├── performance.html       # Radar, Bar, Line, and Scatter analytics
│   ├── recommendations.html   # Dynamic rule-based diagnostic guidance
│   ├── reports.html           # PDF & CSV reporting center
│   └── settings.html          # ML retraining & database administration
│
└── static/
    ├── css/
    │   └── style.css          # Modern SaaS blue/white dashboard stylesheet
    ├── js/
    │   └── main.js            # Toast notifications, progress bars, responsive toggle
    └── images/                # Static image assets
```

---

## 🚀 Installation & Local Execution Instructions

### Prerequisites
- Python 3.9+ installed on your system.

### Step 1: Clone or Navigate to Project Directory
```bash
cd "c:\Users\FAYAS AHAMED K\Downloads\student_academic_performance"
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Train Machine Learning Model (Optional - Auto-trained on startup)
```bash
python ml/train_model.py
```

### Step 4: Run the Flask Web Application
```bash
python app.py
```

### Step 5: Open Application in Web Browser
Open your preferred web browser and navigate to:
```
http://127.0.0.1:5000
```
or
```
http://localhost:5000
```

---

## 🧪 Comprehensive Verification Checklist

| Feature | Status | Verification Detail |
|---|---|---|
| Flask application starts | ✅ Verified | Running cleanly with zero startup errors |
| SQLite database initialized | ✅ Verified | `database/students.db` created automatically |
| Pre-seeded sample students | ✅ Verified | 16 diverse student profiles with attendance & marks |
| Student CRUD operations | ✅ Verified | Add, edit, delete, auto-ID, search, and department filter |
| Attendance calculation | ✅ Verified | Real-time percentage, progress bars, validation |
| Academic records management | ✅ Verified | Daily study hours, assignments, internals, actual marks |
| ML Model Training | ✅ Verified | Scikit-learn Multiple Linear Regression trained on 500 records |
| Model Evaluation Metrics | ✅ Verified | $R^2 = 86.04\%$, $\text{MAE} = 3.17$, $\text{MSE} = 16.02$ |
| Real-time predictions | ✅ Verified | Computes clamped [0-100] prediction with 2 decimals |
| Performance categorization | ✅ Verified | Categorizes into 5 tiers (Excellent to Needs Improvement) |
| Improvement recommendations | ✅ Verified | Dynamic conditional guidance and actionable study plans |
| Performance analysis charts | ✅ Verified | Radar, Bar (actual vs predicted), Line, and Scatter charts |
| PDF Report Generation | ✅ Verified | ReportLab compiles professional student report PDF |
| CSV Data Export | ✅ Verified | Class roster exported with all academic parameters |
| Responsive UI | ✅ Verified | Bootstrap 5 with responsive sidebar and mobile drawer |
