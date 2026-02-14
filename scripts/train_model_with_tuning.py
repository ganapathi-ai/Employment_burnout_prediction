# pylint: disable=too-many-locals,too-many-statements,unused-variable,line-too-long,invalid-name,trailing-whitespace,unspecified-encoding
#!/usr/bin/env python3
"""Model training with hyperparameter tuning using BayesianSearch"""
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, make_scorer
from skopt import BayesSearchCV
from skopt.space import Real, Integer
import xgboost as xgb
import wandb


def engineer_features(df):
    """Apply feature engineering transformations"""
    df = df.copy()
    df['work_intensity_ratio'] = df['screen_time_hours'] / (df['work_hours'] + 0.1)
    df['meeting_burden'] = df['meetings_count'] / (df['work_hours'] + 0.1)
    df['break_adequacy'] = df['breaks_taken'] / (df['work_hours'] + 0.1)
    df['sleep_deficit'] = 8 - df['sleep_hours']
    df['recovery_index'] = (df['sleep_hours'] + df['breaks_taken']) - df['screen_time_hours']
    df['fatigue_risk'] = df['screen_time_hours'] - (df['sleep_hours'] * 1.5)
    df['workload_pressure'] = df['work_hours'] + (df['meetings_count'] * 0.25) + df['after_hours_work']
    df['task_efficiency'] = df['task_completion_rate'] / (df['work_hours'] + 0.1)
    df['work_life_balance_score'] = np.clip(
        ((df['sleep_hours'] / 8) * 30 + (df['breaks_taken'] / 5) * 30
         - (df['work_hours'] / 10) * 20 - df['after_hours_work'] * 10) * 2,
        0, 100
    )
    df['is_weekday'] = (df['day_type'] == 'Weekday').astype(int)
    return df


def train_with_tuning():
    """Train models with Bayesian hyperparameter optimization"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # Initialize W&B
    run = wandb.init(
        entity=os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr'),
        project="burnout-prediction",
        name=f"bayesian_tuning_{timestamp}",
        config={"tuning_method": "BayesianSearch", "n_iter": 20},
        tags=["hyperparameter-tuning", "bayesian", "production"],
        notes="Bayesian hyperparameter optimization for 3 models"
    )

    print("Loading data...")
    df = pd.read_csv('data/work_from_home_burnout_dataset.csv')
    print(f"Dataset shape: {df.shape}")

    # Engineer features
    print("\nEngineering features...")
    df = engineer_features(df)
    df['target'] = (df['burnout_risk'] == 'High').astype(int)

    feature_cols = [
        'work_hours', 'screen_time_hours', 'meetings_count', 'breaks_taken',
        'after_hours_work', 'sleep_hours', 'task_completion_rate', 'is_weekday',
        'work_intensity_ratio', 'meeting_burden', 'break_adequacy',
        'sleep_deficit', 'recovery_index', 'fatigue_risk',
        'workload_pressure', 'task_efficiency', 'work_life_balance_score'
    ]

    X = df[feature_cols]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTraining set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define search spaces
    search_spaces = {
        'RandomForest': {
            'n_estimators': Integer(50, 200),
            'max_depth': Integer(5, 20),
            'min_samples_split': Integer(2, 10),
            'min_samples_leaf': Integer(1, 5)
        },
        'GradientBoosting': {
            'n_estimators': Integer(50, 200),
            'max_depth': Integer(3, 10),
            'learning_rate': Real(0.01, 0.3, prior='log-uniform'),
            'subsample': Real(0.6, 1.0)
        },
        'XGBoost': {
            'n_estimators': Integer(50, 200),
            'max_depth': Integer(3, 10),
            'learning_rate': Real(0.01, 0.3, prior='log-uniform'),
            'subsample': Real(0.6, 1.0)
        }
    }

    models = {
        'RandomForest': RandomForestClassifier(random_state=42),
        'GradientBoosting': GradientBoostingClassifier(random_state=42),
        'XGBoost': xgb.XGBClassifier(random_state=42, eval_metric='logloss')
    }

    best_model = None
    best_score = 0
    best_name = ""
    best_params = {}

    print("\nPerforming Bayesian hyperparameter tuning...")

    for name, model in models.items():
        print(f"\n{'=' * 60}")
        print(f"Tuning {name}...")
        print(f"{'=' * 60}")

        # Bayesian optimization
        opt = BayesSearchCV(
            model,
            search_spaces[name],
            n_iter=20,
            cv=3,
            scoring='roc_auc',
            n_jobs=-1,
            random_state=42,
            verbose=1
        )

        opt.fit(X_train_scaled, y_train)

        # Best model from search
        best_estimator = opt.best_estimator_
        y_pred = best_estimator.predict(X_test_scaled)
        y_proba = best_estimator.predict_proba(X_test_scaled)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)

        print(f"\nBest parameters: {opt.best_params_}")
        print(f"Best CV score: {opt.best_score_:.4f}")
        print(f"Test Accuracy: {acc:.4f}")
        print(f"Test ROC-AUC: {auc:.4f}")

        # Log to W&B
        wandb.log({
            f"{name}_best_cv_score": opt.best_score_,
            f"{name}_test_accuracy": acc,
            f"{name}_test_roc_auc": auc,
            f"{name}_best_params": opt.best_params_
        })

        if auc > best_score:
            best_score = auc
            best_model = best_estimator
            best_name = name
            best_params = opt.best_params_

    print(f"\n{'=' * 60}")
    print(f"[BEST] Best model: {best_name}")
    print(f"[BEST] ROC-AUC: {best_score:.4f}")
    print(f"[BEST] Parameters: {best_params}")
    print(f"{'=' * 60}")

    # Log best model
    wandb.run.summary["best_model"] = best_name
    wandb.run.summary["best_roc_auc"] = best_score
    wandb.run.summary["best_params"] = best_params

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

        wandb.log({"feature_importance_table": wandb.Table(dataframe=importance_df)})

    # Save models
    print("\nSaving tuned model...")
    joblib.dump(best_model, 'models/best_model_tuned.joblib')
    joblib.dump(scaler, 'models/preprocessor_tuned.joblib')
    joblib.dump(feature_cols, 'models/feature_names_tuned.joblib')

    # Save hyperparameters
    with open('models/best_hyperparameters.txt', 'w') as f:
        f.write(f"Best Model: {best_name}\n")
        f.write(f"ROC-AUC: {best_score:.4f}\n")
        f.write(f"Parameters:\n")
        for param, value in best_params.items():
            f.write(f"  {param}: {value}\n")

    # Log artifacts
    artifact = wandb.Artifact('burnout-model-tuned', type='model')
    artifact.add_file('models/best_model_tuned.joblib')
    artifact.add_file('models/preprocessor_tuned.joblib')
    artifact.add_file('models/best_hyperparameters.txt')
    wandb.log_artifact(artifact)

    wandb.finish()

    print("\n[OK] Hyperparameter tuning complete!")
    print(f"[OK] Tuned model saved: models/best_model_tuned.joblib")
    print(f"[OK] Best parameters saved: models/best_hyperparameters.txt")

    return best_model, scaler, feature_cols, best_params


if __name__ == "__main__":
    train_with_tuning()
