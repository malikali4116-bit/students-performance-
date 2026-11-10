from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    attendances = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')
    academic_records = db.relationship('AcademicRecord', backref='student', lazy=True, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='student', lazy=True, cascade='all, delete-orphan')

    @property
    def latest_attendance(self):
        return Attendance.query.filter_by(student_id=self.id).order_by(Attendance.created_at.desc()).first()

    @property
    def latest_academic(self):
        return AcademicRecord.query.filter_by(student_id=self.id).order_by(AcademicRecord.created_at.desc()).first()

    @property
    def latest_prediction(self):
        return Prediction.query.filter_by(student_id=self.id).order_by(Prediction.created_at.desc()).first()

    def to_dict(self):
        att = self.latest_attendance
        acad = self.latest_academic
        pred = self.latest_prediction

        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'department': self.department,
            'year': self.year,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'attendance': att.to_dict() if att else None,
            'academic_record': acad.to_dict() if acad else None,
            'prediction': pred.to_dict() if pred else None
        }


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    total_working_days = db.Column(db.Integer, nullable=False, default=100)
    days_attended = db.Column(db.Integer, nullable=False, default=0)
    attendance_percentage = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'total_working_days': self.total_working_days,
            'days_attended': self.days_attended,
            'attendance_percentage': round(self.attendance_percentage, 1),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }


class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    study_hours = db.Column(db.Float, nullable=False, default=0.0)
    assignment_marks = db.Column(db.Float, nullable=False, default=0.0)
    internal_marks = db.Column(db.Float, nullable=False, default=0.0)
    previous_semester_marks = db.Column(db.Float, nullable=False, default=0.0)
    actual_final_marks = db.Column(db.Float, nullable=True)  # Entered only when faculty provides it
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'study_hours': round(self.study_hours, 1),
            'assignment_marks': round(self.assignment_marks, 1),
            'internal_marks': round(self.internal_marks, 1),
            'previous_semester_marks': round(self.previous_semester_marks, 1),
            'actual_final_marks': round(self.actual_final_marks, 2) if self.actual_final_marks is not None else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    predicted_marks = db.Column(db.Float, nullable=False)
    performance_category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'predicted_marks': round(self.predicted_marks, 2),
            'performance_category': self.performance_category,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }
