"""
Comprehensive Automated Test Suite for Student Academic Performance System
Validates all 9 page routes, API endpoints, CRUD operations, ML model inferences,
PDF generation, and CSV exports.
"""

import unittest
import json
from app import app
from models import db, Student, Attendance, AcademicRecord, Prediction


class ComprehensiveAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_01_all_page_routes(self):
        """Verify all 9 navigation pages render HTTP 200 with HTML content."""
        routes = [
            '/',
            '/dashboard',
            '/students',
            '/attendance',
            '/academic-records',
            '/prediction',
            '/performance',
            '/recommendations',
            '/reports',
            '/settings'
        ]
        for route in routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed with status {res.status_code}")
            self.assertIn(b'<!DOCTYPE html>', res.data, f"Route {route} did not return valid HTML")
        print("[PASS] All 9 page routes passed.")

    def test_02_dashboard_stats_api(self):
        """Verify dashboard statistics and chart datasets."""
        res = self.client.get('/api/dashboard/stats')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('total_students', data)
        self.assertGreaterEqual(data['total_students'], 15)
        self.assertIn('avg_attendance', data)
        self.assertIn('avg_assignment', data)
        self.assertIn('avg_internal', data)
        self.assertIn('avg_predicted', data)
        self.assertIn('performing_well', data)
        self.assertIn('needing_improvement', data)
        self.assertIn('recent_activity', data)
        self.assertIn('charts', data)
        self.assertIn('performance_overview', data['charts'])
        self.assertIn('attendance_distribution', data['charts'])
        self.assertIn('actual_vs_predicted', data['charts'])
        self.assertIn('performance_categories', data['charts'])
        print("[PASS] Dashboard statistics & charts API passed.")

    def test_03_student_crud(self):
        """Test Student creation, retrieval, updating, and deletion."""
        # 1. Next ID
        id_res = self.client.get('/api/students/next-id')
        self.assertEqual(id_res.status_code, 200)
        next_id = id_res.get_json()['next_id']
        self.assertTrue(next_id.startswith('STU-2026-'))

        # 2. Create student
        new_student = {
            'student_id': 'STU-TEST-999',
            'name': 'Test Student Autonoma',
            'department': 'Computer Science & Engineering',
            'year': '3rd Year',
            'email': 'autonoma.test@campus.edu',
            'phone': '+91 99999 11111'
        }
        create_res = self.client.post('/api/students', json=new_student)
        self.assertEqual(create_res.status_code, 201)
        created_id = create_res.get_json()['student']['id']

        # 3. Retrieve student
        get_res = self.client.get(f'/api/students/{created_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()['name'], 'Test Student Autonoma')

        # 4. Update student
        update_data = {
            'name': 'Test Student Updated',
            'department': 'Information Technology',
            'year': '4th Year',
            'email': 'updated.test@campus.edu',
            'phone': '+91 99999 22222'
        }
        put_res = self.client.put(f'/api/students/{created_id}', json=update_data)
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()['student']['name'], 'Test Student Updated')

        # 5. Delete student
        del_res = self.client.delete(f'/api/students/{created_id}')
        self.assertEqual(del_res.status_code, 200)

        # Confirm deleted
        get_after_del = self.client.get(f'/api/students/{created_id}')
        self.assertEqual(get_after_del.status_code, 404)
        print("[PASS] Student CRUD operations passed.")

    def test_04_attendance_management(self):
        """Test Attendance logging and history."""
        student = Student.query.first()
        self.assertIsNotNone(student)

        # Valid attendance
        payload = {
            'student_id': student.id,
            'total_working_days': 100,
            'days_attended': 85
        }
        res = self.client.post('/api/attendance', json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['attendance_percentage'], 85.0)

        # Invalid attendance (attended > total)
        invalid_payload = {
            'student_id': student.id,
            'total_working_days': 80,
            'days_attended': 95
        }
        inv_res = self.client.post('/api/attendance', json=invalid_payload)
        self.assertEqual(inv_res.status_code, 400)

        # History
        hist_res = self.client.get(f'/api/attendance/{student.id}')
        self.assertEqual(hist_res.status_code, 200)
        self.assertIsInstance(hist_res.get_json(), list)
        print("[PASS] Attendance management and validation passed.")

    def test_05_academic_records(self):
        """Test Academic Record updating with actual final marks."""
        student = Student.query.first()
        payload = {
            'student_id': student.id,
            'study_hours': 5.0,
            'assignment_marks': 90.0,
            'internal_marks': 88.0,
            'previous_semester_marks': 85.0,
            'actual_final_marks': 87.5
        }
        res = self.client.post('/api/academic-records', json=payload)
        self.assertEqual(res.status_code, 200)
        record = res.get_json()['record']
        self.assertEqual(record['actual_final_marks'], 87.5)
        print("[PASS] Academic records updating passed.")

    def test_06_ml_prediction(self):
        """Test Machine Learning prediction inference and categorization."""
        # Test case: High performer
        high_payload = {
            'attendance_percentage': 95.0,
            'study_hours': 6.0,
            'assignment_marks': 92.0,
            'internal_marks': 94.0,
            'previous_semester_marks': 90.0
        }
        res = self.client.post('/api/predict', json=high_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('predicted_marks', data)
        self.assertGreaterEqual(data['predicted_marks'], 80.0)
        self.assertIn(data['performance_category'], ['Excellent', 'Very Good'])
        self.assertIn('weak_areas', data)
        self.assertIn('action_plan', data)
        self.assertIn('model_info', data)

        # Test case: Low performer
        low_payload = {
            'attendance_percentage': 50.0,
            'study_hours': 1.0,
            'assignment_marks': 35.0,
            'internal_marks': 38.0,
            'previous_semester_marks': 40.0
        }
        res_low = self.client.post('/api/predict', json=low_payload)
        self.assertEqual(res_low.status_code, 200)
        data_low = res_low.get_json()
        self.assertLess(data_low['predicted_marks'], 50.0)
        self.assertIn(data_low['performance_category'], ['Average', 'Needs Improvement'])
        print("[PASS] ML Prediction inference and category validation passed.")

    def test_07_reports_pdf_and_csv(self):
        """Test PDF generation via ReportLab and CSV export."""
        student = Student.query.first()
        
        # PDF test
        pdf_res = self.client.get(f'/api/reports/pdf/{student.id}')
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res.content_type, 'application/pdf')
        self.assertTrue(pdf_res.data.startswith(b'%PDF'), "PDF content did not begin with standard PDF header")

        # CSV test
        csv_res = self.client.get('/api/reports/csv')
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.content_type, 'text/csv; charset=utf-8')
        self.assertIn(b'Student ID,Student Name,Department', csv_res.data)
        print("[PASS] PDF generation and CSV exports passed.")

    def test_08_model_retraining(self):
        """Test ML model retraining endpoint."""
        res = self.client.post('/api/ml/retrain')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('metrics', data)
        self.assertGreater(data['metrics']['metrics']['r2_score'], 0.7)
        print("[PASS] ML Model retraining endpoint passed.")


if __name__ == '__main__':
    unittest.main()
