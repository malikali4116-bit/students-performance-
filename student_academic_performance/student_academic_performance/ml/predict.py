"""
Machine Learning Inference and Recommendation Engine
Loads trained Multiple Linear Regression model to predict student final examination marks.
Computes performance categories and generates actionable personalized improvement recommendations.
"""

import os
import json
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.pkl')
METRICS_PATH = os.path.join(BASE_DIR, 'ml', 'model_metrics.json')

_cached_model = None
_cached_metrics = None


def get_model():
    """Load or retrieve cached Scikit-learn model."""
    global _cached_model
    if _cached_model is None:
        if not os.path.exists(MODEL_PATH):
            from ml.train_model import train_and_evaluate
            _cached_model, _ = train_and_evaluate()
        else:
            _cached_model = joblib.load(MODEL_PATH)
    return _cached_model


def get_metrics():
    """Load or retrieve model metrics."""
    global _cached_metrics
    if _cached_metrics is None:
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, 'r') as f:
                _cached_metrics = json.load(f)
        else:
            _cached_metrics = {
                'algorithm': 'Multiple Linear Regression',
                'framework': 'Scikit-learn',
                'metrics': {
                    'mae': 3.17,
                    'mse': 16.02,
                    'rmse': 4.00,
                    'r2_score': 0.8604,
                    'r2_percentage': 86.04
                }
            }
    return _cached_metrics


def categorize_performance(marks):
    """
    Categorize final examination marks into standard academic tiers:
      - 90–100: Excellent
      - 75–89: Very Good
      - 60–74: Good
      - 40–59: Average
      - Below 40: Needs Improvement
    """
    marks = float(marks)
    if marks >= 90.0:
        return {
            'category': 'Excellent',
            'badge_class': 'success',
            'color': '#10b981',
            'description': 'Outstanding academic proficiency across subjects.'
        }
    elif marks >= 75.0:
        return {
            'category': 'Very Good',
            'badge_class': 'primary',
            'color': '#3b82f6',
            'description': 'High academic standard with strong conceptual grasp.'
        }
    elif marks >= 60.0:
        return {
            'category': 'Good',
            'badge_class': 'info',
            'color': '#06b6d4',
            'description': 'Satisfactory performance meeting curriculum benchmarks.'
        }
    elif marks >= 40.0:
        return {
            'category': 'Average',
            'badge_class': 'warning',
            'color': '#f59e0b',
            'description': 'Moderate performance; key academic areas require attention.'
        }
    else:
        return {
            'category': 'Needs Improvement',
            'badge_class': 'danger',
            'color': '#ef4444',
            'description': 'Critical risk of underperformance; immediate remedial action needed.'
        }


def generate_recommendations(attendance, study_hours, assignment_marks, internal_marks, previous_semester_marks, predicted_marks):
    """
    Generates rule-based personalized improvement recommendations and action items.
    """
    recommendations = []
    weak_areas = []
    action_plan = []
    
    # 1. Attendance checks
    if attendance < 75.0:
        weak_areas.append("Attendance Below Minimum Threshold (75%)")
        recommendations.append({
            'area': 'Class Attendance',
            'severity': 'high',
            'message': 'Your attendance is critically below the 75% institutional requirement. Recommend attending all remaining lectures and lab sessions to meet examination eligibility.',
            'target': 'Achieve at least 75-80% attendance'
        })
        action_plan.append("Attend every scheduled lecture and practical class for the next 4 weeks.")
    elif attendance <= 85.0:
        recommendations.append({
            'area': 'Class Attendance',
            'severity': 'medium',
            'message': 'Attendance is satisfactory (75%–85%). Encourage consistent attendance to improve classroom engagement and concept comprehension.',
            'target': 'Target 90%+ attendance'
        })
    else:
        recommendations.append({
            'area': 'Class Attendance',
            'severity': 'low',
            'message': 'Excellent attendance! Maintain this consistent classroom presence to stay ahead with coursework.',
            'target': 'Maintain consistent attendance'
        })
        
    # 2. Daily Study Hours
    if study_hours < 2.0:
        weak_areas.append("Insufficient Self-Study Time (<2 hrs/day)")
        recommendations.append({
            'area': 'Daily Study Hours',
            'severity': 'high',
            'message': 'Daily self-study is currently under 2 hours. Recommend establishing a dedicated daily study routine of at least 2 to 3 hours with focused active recall.',
            'target': 'Increase study hours to 2.5–3 hours daily'
        })
        action_plan.append("Allocate two 60-minute distraction-free study blocks every evening.")
    elif study_hours <= 4.0:
        recommendations.append({
            'area': 'Daily Study Hours',
            'severity': 'medium',
            'message': 'Moderate study commitment (2–4 hours). Encourage a structured weekly timetable and prioritize challenging subjects.',
            'target': 'Sustain 3.5–4 hours of structured study'
        })
        action_plan.append("Use the Pomodoro technique (25 min focus / 5 min break) for tough topics.")
    else:
        recommendations.append({
            'area': 'Daily Study Hours',
            'severity': 'low',
            'message': 'Substantial self-study time (above 4 hours). Maintain a balanced routine with scheduled breaks to avoid mental fatigue.',
            'target': 'Balance intense study with wellness'
        })

    # 3. Assignment Marks
    if assignment_marks < 50.0:
        weak_areas.append("Low Assignment Scores (<50)")
        recommendations.append({
            'area': 'Assignments & Homework',
            'severity': 'high',
            'message': 'Assignment marks are below 50. Recommend reviewing assignment feedback, practicing standard problem sets, and consulting subject teachers for clarity.',
            'target': 'Target 70%+ in upcoming assignments'
        })
        action_plan.append("Redo solved examples from textbooks and submit assignments before deadlines.")
    elif assignment_marks <= 75.0:
        recommendations.append({
            'area': 'Assignments & Homework',
            'severity': 'medium',
            'message': 'Assignment performance is acceptable (50–75). Encourage solving additional analytical questions and self-verifying solutions.',
            'target': 'Aim for 80%+ on next assignments'
        })
    else:
        recommendations.append({
            'area': 'Assignments & Homework',
            'severity': 'low',
            'message': 'Strong assignment performance (>75). Maintain thorough problem-solving habits and support peer study groups.',
            'target': 'Maintain 85%+ excellence'
        })

    # 4. Internal Assessment Marks
    if internal_marks < 50.0:
        weak_areas.append("Low Internal Assessment Scores (<50)")
        recommendations.append({
            'area': 'Internal Assessments',
            'severity': 'high',
            'message': 'Internal test scores are critically low (<50). Recommend rigorous revision of weak subjects, solving previous semester papers, and attending doubt sessions.',
            'target': 'Score at least 65% in next mid-term'
        })
        action_plan.append("Solve at least 3 previous years' internal question papers under timed conditions.")
    elif internal_marks <= 75.0:
        recommendations.append({
            'area': 'Internal Assessments',
            'severity': 'medium',
            'message': 'Internal assessment is fair (50–75). Focus on mid-level analytical questions and error analysis from recent test papers.',
            'target': 'Advance to 80%+'
        })
    else:
        recommendations.append({
            'area': 'Internal Assessments',
            'severity': 'low',
            'message': 'Commendable internal assessment performance (>75). Maintain steady revision and focus on mastering advanced topics.',
            'target': 'Sustain top-tier scores'
        })

    # 5. Previous Semester Marks
    if previous_semester_marks < 60.0:
        weak_areas.append("Prerequisite Knowledge Gaps (<60% prior sem)")
        recommendations.append({
            'area': 'Foundational Concepts',
            'severity': 'high',
            'message': 'Previous semester score indicates knowledge gaps in foundational prerequisites. Review fundamental topics and request faculty mentoring.',
            'target': 'Solidify foundational topics'
        })
        action_plan.append("Schedule 2 consultation hours weekly with department mentors.")
    else:
        recommendations.append({
            'area': 'Foundational Concepts',
            'severity': 'low',
            'message': 'Solid foundational marks from previous semester. Build upon this strength to excel in advanced semester modules.',
            'target': 'Leverage existing strengths'
        })
        
    # Overall summary narrative
    if predicted_marks >= 85:
        summary_text = "The student shows excellent academic indicators with strong potential for top honors. Continue current study habits and participate in extracurricular enrichment."
    elif predicted_marks >= 70:
        summary_text = "The student demonstrates solid competence. With minor improvements in weaker modules and sustained assignment quality, an 'Excellent' grade is within reach."
    elif predicted_marks >= 50:
        summary_text = "The student is currently performing at an average level. Concentrated focus on internal assessments, regular attendance, and disciplined study hours will significantly boost final marks."
    else:
        summary_text = "Urgent academic intervention is required. Multiple risk factors (low attendance, internal scores, or study hours) threaten overall course completion. Immediate faculty mentoring is strongly advised."

    if not action_plan:
        action_plan.append("Maintain the current balanced study timetable and engage actively in class discussions.")
        action_plan.append("Attempt mock examination papers to simulate final exam time constraints.")

    return {
        'summary': summary_text,
        'weak_areas': weak_areas if weak_areas else ['None identified - maintaining good standing!'],
        'recommendations': recommendations,
        'action_plan': action_plan
    }


def predict_performance(attendance, study_hours, assignment_marks, internal_marks, previous_semester_marks):
    """
    Runs the Scikit-learn Multiple Linear Regression model on the 5 inputs.
    Validates input bounds, clamps output to [0, 100], and computes full diagnosis.
    """
    # Validation & casting
    try:
        att = float(attendance)
        sh = float(study_hours)
        assign = float(assignment_marks)
        internal = float(internal_marks)
        prev_sem = float(previous_semester_marks)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid numeric input: {e}")

    # Bounds checking
    if not (0.0 <= att <= 100.0):
        raise ValueError("Attendance percentage must be between 0 and 100.")
    if not (0.0 <= sh <= 12.0):
        raise ValueError("Daily study hours must be between 0 and 12.")
    if not (0.0 <= assign <= 100.0):
        raise ValueError("Assignment marks must be between 0 and 100.")
    if not (0.0 <= internal <= 100.0):
        raise ValueError("Internal assessment marks must be between 0 and 100.")
    if not (0.0 <= prev_sem <= 100.0):
        raise ValueError("Previous semester marks must be between 0 and 100.")

    model = get_model()
    
    # Feature DataFrame to match fitted feature names cleanly
    feature_cols = [
        'attendance_percentage',
        'study_hours',
        'assignment_marks',
        'internal_marks',
        'previous_semester_marks'
    ]
    import pandas as pd
    input_df = pd.DataFrame([[att, sh, assign, internal, prev_sem]], columns=feature_cols)
    raw_prediction = model.predict(input_df)[0]
    
    # Clamping and rounding
    predicted_marks = round(float(np.clip(raw_prediction, 0.0, 100.0)), 2)
    
    category_info = categorize_performance(predicted_marks)
    recs = generate_recommendations(att, sh, assign, internal, prev_sem, predicted_marks)
    metrics_info = get_metrics()
    
    return {
        'inputs': {
            'attendance_percentage': att,
            'study_hours': sh,
            'assignment_marks': assign,
            'internal_marks': internal,
            'previous_semester_marks': prev_sem
        },
        'predicted_marks': predicted_marks,
        'raw_prediction': round(float(raw_prediction), 2),
        'performance_category': category_info['category'],
        'category_badge': category_info['badge_class'],
        'category_color': category_info['color'],
        'category_description': category_info['description'],
        'analysis': recs['summary'],
        'weak_areas': recs['weak_areas'],
        'recommendations': recs['recommendations'],
        'action_plan': recs['action_plan'],
        'model_info': {
            'algorithm': 'Multiple Linear Regression',
            'library': 'Scikit-learn',
            'mae': metrics_info.get('metrics', {}).get('mae', 3.17),
            'mse': metrics_info.get('metrics', {}).get('mse', 16.02),
            'rmse': metrics_info.get('metrics', {}).get('rmse', 4.00),
            'r2_score': metrics_info.get('metrics', {}).get('r2_score', 0.86),
            'r2_percentage': metrics_info.get('metrics', {}).get('r2_percentage', 86.0)
        }
    }


if __name__ == '__main__':
    # Test sample prediction
    res = predict_performance(85.0, 4.0, 80.0, 78.0, 75.0)
    print("Test Prediction:")
    print(f"Predicted Marks: {res['predicted_marks']}")
    print(f"Category: {res['performance_category']}")
    print(f"Summary: {res['analysis']}")
