import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'student-academic-perf-system-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(BASE_DIR, 'database', 'students.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'student_performance.csv')
    MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.pkl')
    METRICS_PATH = os.path.join(BASE_DIR, 'ml', 'model_metrics.json')
