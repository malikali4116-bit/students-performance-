"""
Flask Application for Student Academic Performance Prediction and Improvement Support System
Autonomous Full-Stack Architecture with Machine Learning Backend
"""

import os
from flask import Flask, render_template, request, jsonify, Response, send_file
from config import Config
from models import db, Student, Attendance, AcademicRecord, Prediction
from seed_database import seed_database
from ml.predict import predict_performance, get_metrics, categorize_performance, generate_recommendations
from ml.train_model import train_and_evaluate
from report_generator import generate_student_pdf, generate_class_csv

app = Flask(__name__)
app.config.from_object(Config)

# Ensure database directory exists
os.makedirs(os.path.join(app.root_path, 'database'), exist_ok=True)
db.init_app(app)


# -------------------------------------------------------------------------
# Application Initialization (Database & Model)
# -------------------------------------------------------------------------
with app.app_context():
    db.create_all()
    # Check if database has initial records; seed if needed
    if Student.query.count() < 15:
        print("Initializing database with sample student data...")
        seed_database()
    # Ensure ML model is trained
    if not os.path.exists(app.config['MODEL_PATH']):
        print("Training initial Machine Learning model...")
        train_and_evaluate()


# -------------------------------------------------------------------------
# Page Navigation Routes
# -------------------------------------------------------------------------
@app.route('/')
@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/students')
def students_page():
    return render_template('students.html', active_page='students')

@app.route('/attendance')
def attendance_page():
    return render_template('attendance.html', active_page='attendance')

@app.route('/academic-records')
def academic_records_page():
    return render_template('academic_records.html', active_page='academic_records')

@app.route('/prediction')
def prediction_page():
    return render_template('prediction.html', active_page='prediction')

@app.route('/performance')
def performance_page():
    return render_template('performance.html', active_page='performance')

@app.route('/recommendations')
def recommendations_page():
    return render_template('recommendations.html', active_page='recommendations')

@app.route('/reports')
def reports_page():
    return render_template('reports.html', active_page='reports')

@app.route('/settings')
def settings_page():
    return render_template('settings.html', active_page='settings')


# -------------------------------------------------------------------------
# Dashboard APIs
# -------------------------------------------------------------------------
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Calculates and returns all aggregate metrics, charts, and activity."""
    students = Student.query.all()
    total_students = len(students)

    if total_students == 0:
        return jsonify({
            'total_students': 0,
            'avg_attendance': 0,
            'avg_assignment': 0,
            'avg_internal': 0,
            'avg_predicted': 0,
            'performing_well': 0,
            'needing_improvement': 0,
            'recent_activity': [],
            'charts': {
                'performance_overview': {'labels': [], 'predicted': [], 'actual': []},
                'attendance_distribution': {'labels': ['Below 75%', '75% - 85%', 'Above 85%'], 'counts': [0, 0, 0]},
                'actual_vs_predicted': {'labels': [], 'actual': [], 'predicted': []},
                'performance_categories': {'labels': ['Excellent', 'Very Good', 'Good', 'Average', 'Needs Improvement'], 'counts': [0, 0, 0, 0, 0]}
            }
        })

    total_att = 0.0
    att_count = 0
    total_assign = 0.0
    total_internal = 0.0
    acad_count = 0
    total_pred = 0.0
    pred_count = 0

    performing_well = 0
    needing_improvement = 0

    category_counts = {
        'Excellent': 0,
        'Very Good': 0,
        'Good': 0,
        'Average': 0,
        'Needs Improvement': 0
    }

    att_dist = {
        'below_75': 0,
        'between_75_85': 0,
        'above_85': 0
    }

    recent_activity = []
    overview_labels = []
    overview_predicted = []
    overview_actual = []

    actual_vs_pred_labels = []
    actual_vs_pred_actual = []
    actual_vs_pred_predicted = []

    for s in students:
        att = s.latest_attendance
        acad = s.latest_academic
        pred = s.latest_prediction

        att_pct = att.attendance_percentage if att else 0.0
        if att:
            total_att += att_pct
            att_count += 1
            if att_pct < 75.0:
                att_dist['below_75'] += 1
            elif att_pct <= 85.0:
                att_dist['between_75_85'] += 1
            else:
                att_dist['above_85'] += 1

        assign_m = acad.assignment_marks if acad else 0.0
        internal_m = acad.internal_marks if acad else 0.0
        actual_m = acad.actual_final_marks if acad else None

        if acad:
            total_assign += assign_m
            total_internal += internal_m
            acad_count += 1

        pred_m = pred.predicted_marks if pred else None
        pred_cat = pred.performance_category if pred else 'Not Predicted'

        if pred:
            total_pred += pred_m
            pred_count += 1
            if pred_m >= 60.0:
                performing_well += 1
            else:
                needing_improvement += 1

            if pred_cat in category_counts:
                category_counts[pred_cat] += 1
            else:
                category_counts['Needs Improvement'] += 1

        # Activity row
        cat_badge = 'secondary'
        if pred_cat == 'Excellent': cat_badge = 'success'
        elif pred_cat == 'Very Good': cat_badge = 'primary'
        elif pred_cat == 'Good': cat_badge = 'info'
        elif pred_cat == 'Average': cat_badge = 'warning'
        elif pred_cat == 'Needs Improvement': cat_badge = 'danger'

        recent_activity.append({
            'id': s.id,
            'student_id': s.student_id,
            'name': s.name,
            'attendance': f"{att_pct:.1f}%" if att else "N/A",
            'assignment_marks': f"{assign_m:.1f}" if acad else "N/A",
            'internal_marks': f"{internal_m:.1f}" if acad else "N/A",
            'predicted_final': f"{pred_m:.2f}" if pred else "N/A",
            'actual_final': f"{actual_m:.2f}" if actual_m is not None else "Pending",
            'category': pred_cat,
            'category_badge': cat_badge
        })

        # Chart 1: Performance overview for top 10 students
        if len(overview_labels) < 10 and pred_m is not None:
            overview_labels.append(s.name.split()[0])
            overview_predicted.append(pred_m)
            overview_actual.append(actual_m if actual_m is not None else 0.0)

        # Chart 3: Actual vs Predicted where actual marks exist
        if actual_m is not None and pred_m is not None:
            actual_vs_pred_labels.append(s.name.split()[0])
            actual_vs_pred_actual.append(actual_m)
            actual_vs_pred_predicted.append(pred_m)

    avg_attendance = round(total_att / att_count, 1) if att_count > 0 else 0.0
    avg_assignment = round(total_assign / acad_count, 1) if acad_count > 0 else 0.0
    avg_internal = round(total_internal / acad_count, 1) if acad_count > 0 else 0.0
    avg_predicted = round(total_pred / pred_count, 2) if pred_count > 0 else 0.0

    return jsonify({
        'total_students': total_students,
        'avg_attendance': avg_attendance,
        'avg_assignment': avg_assignment,
        'avg_internal': avg_internal,
        'avg_predicted': avg_predicted,
        'performing_well': performing_well,
        'needing_improvement': needing_improvement,
        'recent_activity': recent_activity,
        'charts': {
            'performance_overview': {
                'labels': overview_labels,
                'predicted': overview_predicted,
                'actual': overview_actual
            },
            'attendance_distribution': {
                'labels': ['< 75% (Critical)', '75% - 85% (Average)', '> 85% (Excellent)'],
                'counts': [att_dist['below_75'], att_dist['between_75_85'], att_dist['above_85']]
            },
            'actual_vs_predicted': {
                'labels': actual_vs_pred_labels,
                'actual': actual_vs_pred_actual,
                'predicted': actual_vs_pred_predicted
            },
            'performance_categories': {
                'labels': ['Excellent (90-100)', 'Very Good (75-89)', 'Good (60-74)', 'Average (40-59)', 'Needs Improvement (<40)'],
                'counts': [
                    category_counts['Excellent'],
                    category_counts['Very Good'],
                    category_counts['Good'],
                    category_counts['Average'],
                    category_counts['Needs Improvement']
                ]
            }
        }
    })


# -------------------------------------------------------------------------
# Student CRUD Operations
# -------------------------------------------------------------------------
@app.route('/api/students', methods=['GET'])
def get_students():
    """List students with optional search and filters."""
    query = request.args.get('q', '').strip()
    dept = request.args.get('department', '').strip()
    year = request.args.get('year', '').strip()

    stmt = Student.query
    if query:
        stmt = stmt.filter((Student.name.ilike(f'%{query}%')) | (Student.student_id.ilike(f'%{query}%')) | (Student.email.ilike(f'%{query}%')))
    if dept:
        stmt = stmt.filter(Student.department == dept)
    if year:
        stmt = stmt.filter(Student.year == year)

    students = stmt.order_by(Student.id.asc()).all()
    return jsonify([s.to_dict() for s in students])


@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    student = db.get_or_404(Student, id)
    return jsonify(student.to_dict())


@app.route('/api/students/next-id', methods=['GET'])
def get_next_student_id():
    """Auto-generate next sequential student ID."""
    last_student = Student.query.order_by(Student.id.desc()).first()
    next_num = (last_student.id + 1) if last_student else 1
    return jsonify({'next_id': f"STU-2026-{next_num:03d}"})


@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    department = data.get('department', '').strip()
    year = data.get('year', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    student_id = data.get('student_id', '').strip()

    # Validations
    if not name or not department or not year or not email or not phone:
        return jsonify({'error': 'All fields are required.'}), 400

    if not student_id:
        last_s = Student.query.order_by(Student.id.desc()).first()
        next_num = (last_s.id + 1) if last_s else 1
        student_id = f"STU-2026-{next_num:03d}"

    if Student.query.filter_by(student_id=student_id).first():
        return jsonify({'error': f"Student ID '{student_id}' is already registered."}), 400

    student = Student(
        student_id=student_id,
        name=name,
        department=department,
        year=year,
        email=email,
        phone=phone
    )
    db.session.add(student)
    db.session.flush()

    # Initialize default blank attendance and academic records
    attendance = Attendance(student_id=student.id, total_working_days=90, days_attended=0, attendance_percentage=0.0)
    academic = AcademicRecord(student_id=student.id, study_hours=2.0, assignment_marks=50.0, internal_marks=50.0, previous_semester_marks=50.0)
    db.session.add(attendance)
    db.session.add(academic)
    db.session.commit()

    return jsonify({'message': 'Student created successfully.', 'student': student.to_dict()}), 201


@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = db.get_or_404(Student, id)
    data = request.get_json() or {}

    name = data.get('name', '').strip()
    department = data.get('department', '').strip()
    year = data.get('year', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()

    if not name or not department or not year or not email or not phone:
        return jsonify({'error': 'All fields are required.'}), 400

    student.name = name
    student.department = department
    student.year = year
    student.email = email
    student.phone = phone

    db.session.commit()
    return jsonify({'message': 'Student updated successfully.', 'student': student.to_dict()})


@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = db.get_or_404(Student, id)
    name = student.name
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': f"Student '{name}' has been deleted successfully."})


# -------------------------------------------------------------------------
# Attendance CRUD Operations
# -------------------------------------------------------------------------
@app.route('/api/attendance', methods=['GET'])
def list_attendance():
    students = Student.query.order_by(Student.id.asc()).all()
    results = []
    for s in students:
        att = s.latest_attendance
        results.append({
            'student_id': s.id,
            'code': s.student_id,
            'name': s.name,
            'department': s.department,
            'total_working_days': att.total_working_days if att else 90,
            'days_attended': att.days_attended if att else 0,
            'attendance_percentage': att.attendance_percentage if att else 0.0,
            'updated_at': att.created_at.strftime('%Y-%m-%d %H:%M') if (att and att.created_at) else 'N/A'
        })
    return jsonify(results)


@app.route('/api/attendance', methods=['POST'])
def save_attendance():
    data = request.get_json() or {}
    student_id = data.get('student_id')
    try:
        total_days = int(data.get('total_working_days', 0))
        attended_days = int(data.get('days_attended', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Working days and days attended must be valid integers.'}), 400

    if not student_id:
        return jsonify({'error': 'Please select a student.'}), 400
    if total_days <= 0:
        return jsonify({'error': 'Total working days must be greater than 0.'}), 400
    if attended_days < 0:
        return jsonify({'error': 'Days attended cannot be negative.'}), 400
    if attended_days > total_days:
        return jsonify({'error': 'Days attended cannot exceed total working days.'}), 400

    student = db.session.get(Student, student_id)
    if not student:
        return jsonify({'error': 'Student not found.'}), 404

    percentage = round((attended_days / total_days) * 100.0, 1)
    if percentage > 100.0:
        return jsonify({'error': 'Attendance cannot exceed 100%.'}), 400

    # Create new attendance record entry
    record = Attendance(
        student_id=student.id,
        total_working_days=total_days,
        days_attended=attended_days,
        attendance_percentage=percentage
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'message': f"Attendance for {student.name} saved successfully.",
        'attendance_percentage': percentage,
        'record': record.to_dict()
    })


@app.route('/api/attendance/<int:student_id>', methods=['GET'])
def get_student_attendance_history(student_id):
    records = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.created_at.desc()).all()
    return jsonify([r.to_dict() for r in records])


# -------------------------------------------------------------------------
# Academic Records CRUD Operations
# -------------------------------------------------------------------------
@app.route('/api/academic-records', methods=['GET'])
def list_academic_records():
    students = Student.query.order_by(Student.id.asc()).all()
    results = []
    for s in students:
        acad = s.latest_academic
        results.append({
            'student_id': s.id,
            'code': s.student_id,
            'name': s.name,
            'department': s.department,
            'study_hours': acad.study_hours if acad else 0.0,
            'assignment_marks': acad.assignment_marks if acad else 0.0,
            'internal_marks': acad.internal_marks if acad else 0.0,
            'previous_semester_marks': acad.previous_semester_marks if acad else 0.0,
            'actual_final_marks': acad.actual_final_marks if (acad and acad.actual_final_marks is not None) else None,
            'updated_at': acad.created_at.strftime('%Y-%m-%d %H:%M') if (acad and acad.created_at) else 'N/A'
        })
    return jsonify(results)


@app.route('/api/academic-records', methods=['POST'])
def save_academic_record():
    data = request.get_json() or {}
    student_id = data.get('student_id')

    try:
        study_hours = float(data.get('study_hours', 0.0))
        assignment_marks = float(data.get('assignment_marks', 0.0))
        internal_marks = float(data.get('internal_marks', 0.0))
        previous_sem = float(data.get('previous_semester_marks', 0.0))
        actual_marks_raw = data.get('actual_final_marks')
        actual_final_marks = float(actual_marks_raw) if (actual_marks_raw is not None and str(actual_marks_raw).strip() != '') else None
    except (ValueError, TypeError) as e:
        return jsonify({'error': f"Invalid numerical value: {str(e)}"}), 400

    if not student_id:
        return jsonify({'error': 'Please select a student.'}), 400
    if not (0.0 <= study_hours <= 12.0):
        return jsonify({'error': 'Daily study hours must be between 0 and 12.'}), 400
    if not (0.0 <= assignment_marks <= 100.0):
        return jsonify({'error': 'Assignment marks must be between 0 and 100.'}), 400
    if not (0.0 <= internal_marks <= 100.0):
        return jsonify({'error': 'Internal assessment marks must be between 0 and 100.'}), 400
    if not (0.0 <= previous_sem <= 100.0):
        return jsonify({'error': 'Previous semester marks must be between 0 and 100.'}), 400
    if actual_final_marks is not None and not (0.0 <= actual_final_marks <= 100.0):
        return jsonify({'error': 'Actual final marks must be between 0 and 100.'}), 400

    student = db.session.get(Student, student_id)
    if not student:
        return jsonify({'error': 'Student not found.'}), 404

    record = AcademicRecord(
        student_id=student.id,
        study_hours=study_hours,
        assignment_marks=assignment_marks,
        internal_marks=internal_marks,
        previous_semester_marks=previous_sem,
        actual_final_marks=actual_final_marks
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'message': f"Academic record for {student.name} saved successfully.",
        'record': record.to_dict()
    })


# -------------------------------------------------------------------------
# Machine Learning Prediction Endpoints
# -------------------------------------------------------------------------
@app.route('/api/predict', methods=['POST'])
def run_prediction():
    """
    Executes trained Scikit-learn Multiple Linear Regression model on 5 features.
    Saves prediction to database if student_id is provided.
    """
    data = request.get_json() or {}
    student_id = data.get('student_id')

    try:
        att = float(data.get('attendance_percentage', 0))
        sh = float(data.get('study_hours', 0))
        assign = float(data.get('assignment_marks', 0))
        internal = float(data.get('internal_marks', 0))
        prev_sem = float(data.get('previous_semester_marks', 0))

        result = predict_performance(att, sh, assign, internal, prev_sem)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

    # If student is selected and save_prediction flag is requested, persist prediction to DB
    if student_id:
        try:
            student = db.session.get(Student, student_id)
            if student:
                pred_entry = Prediction(
                    student_id=student.id,
                    predicted_marks=result['predicted_marks'],
                    performance_category=result['performance_category']
                )
                db.session.add(pred_entry)
                db.session.commit()
                result['saved_to_db'] = True
        except Exception as db_err:
            print(f"Failed to persist prediction: {db_err}")

    return jsonify(result)


@app.route('/api/ml/metrics', methods=['GET'])
def get_ml_metrics():
    """Returns evaluation metrics, sample counts, and feature weights of the ML model."""
    metrics = get_metrics()
    return jsonify(metrics)


@app.route('/api/ml/retrain', methods=['POST'])
def retrain_model():
    """Retrain Multiple Linear Regression model."""
    try:
        model, metrics = train_and_evaluate()
        return jsonify({
            'message': 'Machine Learning model retrained successfully!',
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({'error': f"Retraining failed: {str(e)}"}), 500


# -------------------------------------------------------------------------
# Performance Analysis Endpoints
# -------------------------------------------------------------------------
@app.route('/api/performance/<int:student_id>', methods=['GET'])
def get_student_performance(student_id):
    student = db.get_or_404(Student, student_id)
    att = student.latest_attendance
    acad = student.latest_academic
    pred = student.latest_prediction

    # Class averages for comparison
    all_students = Student.query.all()
    avg_att = sum((s.latest_attendance.attendance_percentage for s in all_students if s.latest_attendance), 0) / max(len(all_students), 1)
    avg_study = sum((s.latest_academic.study_hours for s in all_students if s.latest_academic), 0) / max(len(all_students), 1)
    avg_assign = sum((s.latest_academic.assignment_marks for s in all_students if s.latest_academic), 0) / max(len(all_students), 1)
    avg_internal = sum((s.latest_academic.internal_marks for s in all_students if s.latest_academic), 0) / max(len(all_students), 1)
    avg_prev = sum((s.latest_academic.previous_semester_marks for s in all_students if s.latest_academic), 0) / max(len(all_students), 1)

    s_att = att.attendance_percentage if att else 0.0
    s_study = acad.study_hours if acad else 0.0
    # Normalize study hours to 0-100 scale for radar comparison (12h = 100%)
    s_study_norm = min(100.0, (s_study / 12.0) * 100.0)
    avg_study_norm = min(100.0, (avg_study / 12.0) * 100.0)

    s_assign = acad.assignment_marks if acad else 0.0
    s_internal = acad.internal_marks if acad else 0.0
    s_prev = acad.previous_semester_marks if acad else 0.0
    actual_final = acad.actual_final_marks if (acad and acad.actual_final_marks is not None) else None
    pred_final = pred.predicted_marks if pred else None

    # Performance history (attendance & academic progression)
    history_records = AcademicRecord.query.filter_by(student_id=student.id).order_by(AcademicRecord.created_at.asc()).all()
    history_labels = [f"Record {i+1}" for i in range(len(history_records))]
    history_assign = [r.assignment_marks for r in history_records]
    history_internal = [r.internal_marks for r in history_records]

    return jsonify({
        'student': student.to_dict(),
        'actual_final_marks': actual_final,
        'predicted_marks': pred_final,
        'has_actual_marks': (actual_final is not None),
        'radar': {
            'labels': ['Attendance (%)', 'Study Intensity', 'Assignments', 'Internal Tests', 'Previous Sem'],
            'student_scores': [round(s_att, 1), round(s_study_norm, 1), round(s_assign, 1), round(s_internal, 1), round(s_prev, 1)],
            'class_averages': [round(avg_att, 1), round(avg_study_norm, 1), round(avg_assign, 1), round(avg_internal, 1), round(avg_prev, 1)]
        },
        'comparison_bar': {
            'labels': ['Final Examination Marks'],
            'actual': [actual_final] if actual_final is not None else [],
            'predicted': [pred_final] if pred_final is not None else []
        },
        'history': {
            'labels': history_labels if history_labels else ['Current'],
            'assignment': history_assign if history_assign else [s_assign],
            'internal': history_internal if history_internal else [s_internal]
        }
    })


@app.route('/api/performance/scatter', methods=['GET'])
def get_scatter_data():
    """Attendance vs Final Marks scatter points for all students."""
    students = Student.query.all()
    points = []
    for s in students:
        att = s.latest_attendance
        acad = s.latest_academic
        pred = s.latest_prediction
        if att and (pred or (acad and acad.actual_final_marks is not None)):
            mark = acad.actual_final_marks if (acad and acad.actual_final_marks is not None) else pred.predicted_marks
            points.append({
                'x': round(att.attendance_percentage, 1),
                'y': round(mark, 1),
                'name': s.name,
                'id': s.student_id,
                'type': 'Actual' if (acad and acad.actual_final_marks is not None) else 'Predicted'
            })
    return jsonify(points)


# -------------------------------------------------------------------------
# Improvement Recommendations Endpoints
# -------------------------------------------------------------------------
@app.route('/api/recommendations/<int:student_id>', methods=['GET'])
def get_student_recommendations(student_id):
    student = db.get_or_404(Student, student_id)
    att = student.latest_attendance
    acad = student.latest_academic
    pred = student.latest_prediction

    att_pct = att.attendance_percentage if att else 75.0
    sh = acad.study_hours if acad else 3.0
    assign = acad.assignment_marks if acad else 70.0
    internal = acad.internal_marks if acad else 70.0
    prev_sem = acad.previous_semester_marks if acad else 70.0

    if pred:
        pred_marks = pred.predicted_marks
    else:
        # Predict on the fly
        pred_res = predict_performance(att_pct, sh, assign, internal, prev_sem)
        pred_marks = pred_res['predicted_marks']

    recs = generate_recommendations(att_pct, sh, assign, internal, prev_sem, pred_marks)
    cat_info = categorize_performance(pred_marks)

    return jsonify({
        'student': student.to_dict(),
        'inputs': {
            'attendance_percentage': att_pct,
            'study_hours': sh,
            'assignment_marks': assign,
            'internal_marks': internal,
            'previous_semester_marks': prev_sem
        },
        'predicted_marks': pred_marks,
        'category_info': cat_info,
        'diagnosis': recs
    })


# -------------------------------------------------------------------------
# Reports & Export Endpoints (PDF, CSV, Class Report)
# -------------------------------------------------------------------------
@app.route('/api/reports/class', methods=['GET'])
def get_class_report():
    students = Student.query.order_by(Student.id.asc()).all()
    rows = []
    for s in students:
        att = s.latest_attendance
        acad = s.latest_academic
        pred = s.latest_prediction

        rows.append({
            'id': s.id,
            'student_id': s.student_id,
            'name': s.name,
            'department': s.department,
            'year': s.year,
            'attendance': att.attendance_percentage if att else 0.0,
            'study_hours': acad.study_hours if acad else 0.0,
            'assignment_marks': acad.assignment_marks if acad else 0.0,
            'internal_marks': acad.internal_marks if acad else 0.0,
            'previous_semester_marks': acad.previous_semester_marks if acad else 0.0,
            'predicted_marks': pred.predicted_marks if pred else None,
            'performance_category': pred.performance_category if pred else 'Pending',
            'actual_final_marks': acad.actual_final_marks if (acad and acad.actual_final_marks is not None) else None
        })
    return jsonify({'students': rows, 'total': len(rows)})


@app.route('/api/reports/student/<int:student_id>', methods=['GET'])
def get_student_report_data(student_id):
    student = db.get_or_404(Student, student_id)
    att = student.latest_attendance
    acad = student.latest_academic
    pred = student.latest_prediction

    att_pct = att.attendance_percentage if att else 0.0
    sh = acad.study_hours if acad else 0.0
    assign = acad.assignment_marks if acad else 0.0
    internal = acad.internal_marks if acad else 0.0
    prev_sem = acad.previous_semester_marks if acad else 0.0
    pred_marks = pred.predicted_marks if pred else 0.0

    recs = generate_recommendations(att_pct, sh, assign, internal, prev_sem, pred_marks)
    metrics = get_metrics()

    s_dict = student.to_dict()
    s_dict['recommendations_data'] = recs
    s_dict['model_metrics'] = metrics

    return jsonify(s_dict)


@app.route('/api/reports/csv', methods=['GET'])
def download_csv_report():
    students = Student.query.order_by(Student.id.asc()).all()
    csv_content = generate_class_csv(students)
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=student_performance_records.csv"}
    )


@app.route('/api/reports/pdf/<int:student_id>', methods=['GET'])
def download_pdf_report(student_id):
    student = db.get_or_404(Student, student_id)
    att = student.latest_attendance
    acad = student.latest_academic
    pred = student.latest_prediction

    att_pct = att.attendance_percentage if att else 75.0
    sh = acad.study_hours if acad else 3.0
    assign = acad.assignment_marks if acad else 70.0
    internal = acad.internal_marks if acad else 70.0
    prev_sem = acad.previous_semester_marks if acad else 70.0
    pred_marks = pred.predicted_marks if pred else 70.0

    recs = generate_recommendations(att_pct, sh, assign, internal, prev_sem, pred_marks)
    metrics = get_metrics()

    s_dict = student.to_dict()
    s_dict['recommendations_data'] = recs

    pdf_bytes = generate_student_pdf(s_dict, metrics.get('metrics', {}))
    import io
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"Report_{student.student_id}_{student.name.replace(' ', '_')}.pdf"
    )


# -------------------------------------------------------------------------
# Settings Endpoints
# -------------------------------------------------------------------------
@app.route('/api/settings/reset-db', methods=['POST'])
def reset_database_endpoint():
    """Reset database and re-seed default records."""
    try:
        seed_database(force=True)
        return jsonify({'message': 'Database has been successfully reset and seeded with initial records.'})
    except Exception as e:
        return jsonify({'error': f"Failed to reset database: {str(e)}"}), 500


# -------------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n=================================================================")
    print(f" Student Academic Performance Prediction System")
    print(f" Running at: http://127.0.0.1:{port}")
    print(f"=================================================================\n")
    app.run(host='0.0.0.0', port=port, debug=True)
