"""
Machine Learning Training Script for Student Academic Performance Prediction
Algorithm: Multiple Linear Regression (Scikit-learn)
Features:
  1. Attendance Percentage (0-100)
  2. Daily Study Hours (0-12)
  3. Assignment Marks (0-100)
  4. Internal Assessment Marks (0-100)
  5. Previous Semester Marks (0-100)
Target:
  Final Examination Marks (0-100)
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'student_performance.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.pkl')
METRICS_PATH = os.path.join(BASE_DIR, 'ml', 'model_metrics.json')


def generate_synthetic_dataset(num_samples=500, random_state=42):
    """
    Generate a realistic student academic performance dataset.
    Reflects educational research correlations:
    - High internal & assignment scores strongly correlate with final marks
    - Previous semester foundation has high predictive power
    - Study hours and attendance provide steady positive lifts
    - Realistic noise to mimic examination variance
    """
    np.random.seed(random_state)
    
    # 1. Attendance percentage: 50% to 100% with a cluster around 75-92%
    attendance = np.clip(np.random.normal(loc=82, scale=11, size=num_samples), 45, 100)
    
    # 2. Daily study hours: 1 to 10 hours with average around 3.8 hours
    study_hours = np.clip(np.random.normal(loc=3.8, scale=1.8, size=num_samples), 0.5, 11.5)
    
    # 3. Previous semester marks: 40 to 98
    previous_sem = np.clip(np.random.normal(loc=70, scale=13, size=num_samples), 35, 99)
    
    # 4. Assignment marks: slightly correlated with previous sem & study hours
    assignment_noise = np.random.normal(0, 7, size=num_samples)
    assignments = 0.55 * previous_sem + 2.5 * study_hours + 0.15 * attendance + assignment_noise
    assignments = np.clip(assignments, 30, 100)
    
    # 5. Internal assessment marks: correlated with assignments and previous sem
    internal_noise = np.random.normal(0, 6, size=num_samples)
    internals = 0.50 * previous_sem + 0.25 * assignments + 1.8 * study_hours + 0.10 * attendance + internal_noise
    internals = np.clip(internals, 30, 100)
    
    # 6. Final Examination Marks calculation:
    # Multiple linear combination of features + real-world variance
    exam_noise = np.random.normal(0, 4.2, size=num_samples)
    final_marks = (
        0.10 * attendance +
        1.50 * study_hours +
        0.22 * assignments +
        0.38 * internals +
        0.22 * previous_sem +
        exam_noise
    )
    # Calibrate and clamp to 0-100
    final_marks = np.clip(final_marks, 25, 100)
    
    df = pd.DataFrame({
        'attendance_percentage': np.round(attendance, 1),
        'study_hours': np.round(study_hours, 1),
        'assignment_marks': np.round(assignments, 1),
        'internal_marks': np.round(internals, 1),
        'previous_semester_marks': np.round(previous_sem, 1),
        'final_marks': np.round(final_marks, 2)
    })
    
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Generated realistic dataset with {num_samples} samples at: {DATASET_PATH}")
    return df


def train_and_evaluate(dataset_path=DATASET_PATH):
    """
    Trains Multiple Linear Regression model on student performance dataset.
    Saves model and metrics.
    """
    if not os.path.exists(dataset_path):
        print("Dataset not found. Generating new dataset...")
        df = generate_synthetic_dataset()
    else:
        df = pd.read_csv(dataset_path)
    
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Feature columns and target
    feature_cols = [
        'attendance_percentage',
        'study_hours',
        'assignment_marks',
        'internal_marks',
        'previous_semester_marks'
    ]
    target_col = 'final_marks'
    
    # Handle missing values
    df = df.dropna(subset=feature_cols + [target_col])
    
    X = df[feature_cols]
    y = df[target_col]
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    # Multiple Linear Regression Model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Save Model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved successfully at: {MODEL_PATH}")
    
    # Save Metrics & Info
    metrics = {
        'algorithm': 'Multiple Linear Regression',
        'framework': 'Scikit-learn',
        'total_samples': len(df),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'features': feature_cols,
        'coefficients': {col: float(coef) for col, coef in zip(feature_cols, model.coef_)},
        'intercept': float(model.intercept_),
        'metrics': {
            'mae': round(float(mae), 4),
            'mse': round(float(mse), 4),
            'rmse': round(float(rmse), 4),
            'r2_score': round(float(r2), 4),
            'r2_percentage': round(float(r2 * 100), 2)
        }
    }
    
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved at: {METRICS_PATH}")
    
    print("\n--- Model Evaluation Results ---")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)")
    print("Coefficients:")
    for col, coef in zip(feature_cols, model.coef_):
        print(f"  - {col}: {coef:.4f}")
    print(f"Intercept: {model.intercept_:.4f}")
    print("--------------------------------\n")
    
    return model, metrics


if __name__ == '__main__':
    train_and_evaluate()
