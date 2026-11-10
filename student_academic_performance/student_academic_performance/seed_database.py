"""
Database Seeder for Student Academic Performance System
Seeds at least 16 realistic student profiles with attendance, academic records,
ML-derived predictions, and faculty-entered actual final marks.
"""

from models import db, Student, Attendance, AcademicRecord, Prediction
from ml.predict import predict_performance

SAMPLE_STUDENTS = [
    {
        'student_id': 'STU-2026-001',
        'name': 'Aarav Sharma',
        'department': 'Computer Science & Engineering',
        'year': '3rd Year',
        'email': 'aarav.sharma@campus.edu',
        'phone': '+91 98451 23401',
        'attendance': {'total': 90, 'attended': 85},  # 94.4%
        'academic': {'study_hours': 5.5, 'assignment_marks': 92.0, 'internal_marks': 94.0, 'previous_semester_marks': 89.0, 'actual_final_marks': 91.5}
    },
    {
        'student_id': 'STU-2026-002',
        'name': 'Diya Patel',
        'department': 'Artificial Intelligence & Data Science',
        'year': '2nd Year',
        'email': 'diya.patel@campus.edu',
        'phone': '+91 98451 23402',
        'attendance': {'total': 90, 'attended': 82},  # 91.1%
        'academic': {'study_hours': 4.5, 'assignment_marks': 88.0, 'internal_marks': 85.0, 'previous_semester_marks': 84.0, 'actual_final_marks': 84.0}
    },
    {
        'student_id': 'STU-2026-003',
        'name': 'Rohan Iyer',
        'department': 'Electronics & Communication',
        'year': '4th Year',
        'email': 'rohan.iyer@campus.edu',
        'phone': '+91 98451 23403',
        'attendance': {'total': 90, 'attended': 76},  # 84.4%
        'academic': {'study_hours': 3.5, 'assignment_marks': 75.0, 'internal_marks': 78.0, 'previous_semester_marks': 76.0, 'actual_final_marks': 77.0}
    },
    {
        'student_id': 'STU-2026-004',
        'name': 'Ananya Verma',
        'department': 'Information Technology',
        'year': '3rd Year',
        'email': 'ananya.verma@campus.edu',
        'phone': '+91 98451 23404',
        'attendance': {'total': 90, 'attended': 68},  # 75.6%
        'academic': {'study_hours': 2.8, 'assignment_marks': 68.0, 'internal_marks': 70.0, 'previous_semester_marks': 72.0, 'actual_final_marks': 69.5}
    },
    {
        'student_id': 'STU-2026-005',
        'name': 'Vikram Malhotra',
        'department': 'Mechanical Engineering',
        'year': '2nd Year',
        'email': 'vikram.m@campus.edu',
        'phone': '+91 98451 23405',
        'attendance': {'total': 90, 'attended': 58},  # 64.4%
        'academic': {'study_hours': 1.5, 'assignment_marks': 46.0, 'internal_marks': 48.0, 'previous_semester_marks': 52.0, 'actual_final_marks': 49.0}
    },
    {
        'student_id': 'STU-2026-006',
        'name': 'Sneha Nair',
        'department': 'Computer Science & Engineering',
        'year': '1st Year',
        'email': 'sneha.nair@campus.edu',
        'phone': '+91 98451 23406',
        'attendance': {'total': 90, 'attended': 88},  # 97.8%
        'academic': {'study_hours': 5.0, 'assignment_marks': 95.0, 'internal_marks': 92.0, 'previous_semester_marks': 90.0, 'actual_final_marks': 93.0}
    },
    {
        'student_id': 'STU-2026-007',
        'name': 'Mohammed Zaid',
        'department': 'Information Technology',
        'year': '3rd Year',
        'email': 'zaid.m@campus.edu',
        'phone': '+91 98451 23407',
        'attendance': {'total': 90, 'attended': 52},  # 57.8% - critically low
        'academic': {'study_hours': 1.2, 'assignment_marks': 42.0, 'internal_marks': 38.0, 'previous_semester_marks': 45.0, 'actual_final_marks': 39.5}
    },
    {
        'student_id': 'STU-2026-008',
        'name': 'Pooja Reddy',
        'department': 'Artificial Intelligence & Data Science',
        'year': '4th Year',
        'email': 'pooja.reddy@campus.edu',
        'phone': '+91 98451 23408',
        'attendance': {'total': 90, 'attended': 79},  # 87.8%
        'academic': {'study_hours': 4.0, 'assignment_marks': 82.0, 'internal_marks': 81.0, 'previous_semester_marks': 80.0, 'actual_final_marks': 80.5}
    },
    {
        'student_id': 'STU-2026-009',
        'name': 'Rahul Das',
        'department': 'Electronics & Communication',
        'year': '2nd Year',
        'email': 'rahul.das@campus.edu',
        'phone': '+91 98451 23409',
        'attendance': {'total': 90, 'attended': 72},  # 80.0%
        'academic': {'study_hours': 2.5, 'assignment_marks': 62.0, 'internal_marks': 65.0, 'previous_semester_marks': 64.0, 'actual_final_marks': 63.5}
    },
    {
        'student_id': 'STU-2026-010',
        'name': 'Priya Sen',
        'department': 'Computer Science & Engineering',
        'year': '4th Year',
        'email': 'priya.sen@campus.edu',
        'phone': '+91 98451 23410',
        'attendance': {'total': 90, 'attended': 84},  # 93.3%
        'academic': {'study_hours': 4.2, 'assignment_marks': 84.0, 'internal_marks': 86.0, 'previous_semester_marks': 85.0, 'actual_final_marks': None}
    },
    {
        'student_id': 'STU-2026-011',
        'name': 'Karthik Raja',
        'department': 'Mechanical Engineering',
        'year': '3rd Year',
        'email': 'karthik.raja@campus.edu',
        'phone': '+91 98451 23411',
        'attendance': {'total': 90, 'attended': 65},  # 72.2%
        'academic': {'study_hours': 2.0, 'assignment_marks': 54.0, 'internal_marks': 58.0, 'previous_semester_marks': 60.0, 'actual_final_marks': None}
    },
    {
        'student_id': 'STU-2026-012',
        'name': 'Fatima Begum',
        'department': 'Artificial Intelligence & Data Science',
        'year': '1st Year',
        'email': 'fatima.b@campus.edu',
        'phone': '+91 98451 23412',
        'attendance': {'total': 90, 'attended': 86},  # 95.6%
        'academic': {'study_hours': 5.8, 'assignment_marks': 94.0, 'internal_marks': 96.0, 'previous_semester_marks': 93.0, 'actual_final_marks': None}
    },
    {
        'student_id': 'STU-2026-013',
        'name': 'Aditya Joshi',
        'department': 'Information Technology',
        'year': '2nd Year',
        'email': 'aditya.j@campus.edu',
        'phone': '+91 98451 23413',
        'attendance': {'total': 90, 'attended': 74},  # 82.2%
        'academic': {'study_hours': 3.2, 'assignment_marks': 72.0, 'internal_marks': 74.0, 'previous_semester_marks': 70.0, 'actual_final_marks': None}
    },
    {
        'student_id': 'STU-2026-014',
        'name': 'Kavya Mehra',
        'department': 'Electronics & Communication',
        'year': '3rd Year',
        'email': 'kavya.m@campus.edu',
        'phone': '+91 98451 23414',
        'attendance': {'total': 90, 'attended': 48},  # 53.3% - needs improvement
        'academic': {'study_hours': 1.0, 'assignment_marks': 38.0, 'internal_marks': 40.0, 'previous_semester_marks': 42.0, 'actual_final_marks': None}
    },
    {
        'student_id': 'STU-2026-015',
        'name': 'Arjun Nair',
        'department': 'Computer Science & Engineering',
        'year': '2nd Year',
        'email': 'arjun.nair@campus.edu',
        'phone': '+91 98451 23415',
        'attendance': {'total': 90, 'attended': 81},  # 90.0%
        'academic': {'study_hours': 3.8, 'assignment_marks': 78.0, 'internal_marks': 79.0, 'previous_semester_marks': 77.0, 'actual_final_marks': None}
    },
    {
        'student_id': 'STU-2026-016',
        'name': 'Meera Nambiar',
        'department': 'Artificial Intelligence & Data Science',
        'year': '3rd Year',
        'email': 'meera.n@campus.edu',
        'phone': '+91 98451 23416',
        'attendance': {'total': 90, 'attended': 87},  # 96.7%
        'academic': {'study_hours': 4.8, 'assignment_marks': 90.0, 'internal_marks': 89.0, 'previous_semester_marks': 88.0, 'actual_final_marks': 89.0}
    }
]


def seed_database(force=False):
    """Seed SQLite database with realistic initial student records."""
    if not force and Student.query.count() >= 15:
        print(f"Database already populated with {Student.query.count()} students.")
        return

    print("Populating database with realistic sample student records...")
    
    if force:
        # Clean existing
        Prediction.query.delete()
        AcademicRecord.query.delete()
        Attendance.query.delete()
        Student.query.delete()
        db.session.commit()

    for item in SAMPLE_STUDENTS:
        # Check if student exists
        existing = Student.query.filter_by(student_id=item['student_id']).first()
        if existing:
            continue

        student = Student(
            student_id=item['student_id'],
            name=item['name'],
            department=item['department'],
            year=item['year'],
            email=item['email'],
            phone=item['phone']
        )
        db.session.add(student)
        db.session.flush()

        # Attendance
        att_data = item['attendance']
        att_pct = round((att_data['attended'] / att_data['total']) * 100.0, 1)
        attendance = Attendance(
            student_id=student.id,
            total_working_days=att_data['total'],
            days_attended=att_data['attended'],
            attendance_percentage=att_pct
        )
        db.session.add(attendance)

        # Academic Record
        acad_data = item['academic']
        academic = AcademicRecord(
            student_id=student.id,
            study_hours=acad_data['study_hours'],
            assignment_marks=acad_data['assignment_marks'],
            internal_marks=acad_data['internal_marks'],
            previous_semester_marks=acad_data['previous_semester_marks'],
            actual_final_marks=acad_data.get('actual_final_marks')
        )
        db.session.add(academic)

        # ML Prediction using the actual trained model
        try:
            pred_res = predict_performance(
                attendance=att_pct,
                study_hours=acad_data['study_hours'],
                assignment_marks=acad_data['assignment_marks'],
                internal_marks=acad_data['internal_marks'],
                previous_semester_marks=acad_data['previous_semester_marks']
            )
            prediction = Prediction(
                student_id=student.id,
                predicted_marks=pred_res['predicted_marks'],
                performance_category=pred_res['performance_category']
            )
            db.session.add(prediction)
        except Exception as e:
            print(f"Warning: Could not predict for {student.student_id}: {e}")

    db.session.commit()
    print(f"Successfully seeded database! Total students: {Student.query.count()}")
