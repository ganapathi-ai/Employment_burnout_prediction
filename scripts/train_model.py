#!/usr/bin/env python3
"""Train ML model with real burnout data and feature engineering"""
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import xgboost as xgb

def engineer_features(df):
    """Apply feature engineering transformations"""
    df = df.copy()
    
    # Work intensity metrics
    df['work_intensity_ratio'] = df['screen_time_hours'] / (df['work_hours'] + 0.1)
    df['meeting_burden'] = df['meetings_count'] / (df['work_hours'] + 0.1)
    df['break_adequacy'] = df['breaks_taken'] / (df['work_hours'] + 0.1)
    
    # Health metrics
    df['sleep_deficit'] = 8 - df['sleep_hours']
    df['recovery_index'] = (df['sleep_hours'] + df['breaks_taken']) - df['screen_time_hours']
    df['fatigue_risk'] = df['screen_time_hours'] - (df['sleep_hours'] * 1.5)
    
    # Workload metrics
    df['workload_pressure'] = df['work_hours'] + (df['meetings_count'] * 0.25) + df['after_hours_work']
    df['task_efficiency'] = df['task_completion_rate'] / (df['work_hours'] + 0.1)
    
    # Balance score
    df['work_life_balance_score'] = np.clip(
        ((df['sleep_hours'] / 8) * 30 + (df['breaks_taken'] / 5) * 30 - 
         (df['work_hours'] / 10) * 20 - df['after_hours_work'] * 10) * 2,
        0, 100
    )
    
    # Day type encoding
    df['is_weekday'] = (df['day_type'] == 'Weekday').astype(int)
    
    return df

def train_model():
    """Train burnout prediction model with real data"""
    print("Loading data...")
    df = pd.read_csv('data/work_from_home_burnout_dataset.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Burnout risk distribution:\n{df['burnout_risk'].value_counts()}")
    
    # Engineer features
    print("\nEngineering features...")
    df = engineer_features(df)
    
    # Create binary target (High burnout = 1, else = 0)
    df['target'] = (df['burnout_risk'] == 'High').astype(int)
    
    # Select features for training
    feature_cols = [
        'work_hours', 'screen_time_hours', 'meetings_count', 'breaks_taken',
        'after_hours_work', 'sleep_hours', 'task_completion_rate', 'is_weekday',
        'work_intensity_ratio', 'meeting_burden', 'break_adequacy',
        'sleep_deficit', 'recovery_index', 'fatigue_risk',
        'workload_pressure', 'task_efficiency', 'work_life_balance_score'
    ]
    
    X = df[feature_cols]
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train multiple models and select best
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
        'XGBoost': xgb.XGBClassifier(n_estimators=100, max_depth=5, random_state=42)
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    
    print("\nTraining models...")
    for name, model in models.items():
        print(f"\n{name}:")
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)
        
        print(f"  Accuracy: {acc:.4f}")
        print(f"  ROC-AUC: {auc:.4f}")
        
        if auc > best_score:
            best_score = auc
            best_model = model
            best_name = name
    
    print(f"\n✓ Best model: {best_name} (ROC-AUC: {best_score:.4f})")
    
    # Final evaluation
    y_pred = best_model.predict(X_test_scaled)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low Risk', 'High Risk']))
    
    # Feature importance
    if hasattr(best_model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_cols,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        print("\nTop 10 Important Features:")
        print(importance_df.head(10).to_string(index=False))
    
    # Save model and scaler
    print("\nSaving model and scaler...")
    joblib.dump(best_model, 'models/best_model.joblib')
    joblib.dump(scaler, 'models/preprocessor.joblib')
    joblib.dump(feature_cols, 'models/feature_names.joblib')
    
    print("✓ Model training complete!")
    print(f"✓ Model saved: models/best_model.joblib")
    print(f"✓ Scaler saved: models/preprocessor.joblib")
    print(f"✓ Features saved: models/feature_names.joblib")
    
    return best_model, scaler, feature_cols

if __name__ == "__main__":
    train_model()
