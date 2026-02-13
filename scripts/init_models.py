#!/usr/bin/env python3
"""Initialize models directory with dummy models if needed"""
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

def create_dummy_models():
    """Create dummy models for deployment if they don't exist"""
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, "best_model.joblib")
    preprocessor_path = os.path.join(models_dir, "preprocessor.joblib")
    
    if not os.path.exists(model_path):
        print("Creating dummy model...")
        # Create a simple trained model
        X_dummy = np.random.rand(100, 8)
        y_dummy = np.random.randint(0, 2, 100)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_dummy, y_dummy)
        joblib.dump(model, model_path)
        print(f"✓ Model saved to {model_path}")
    
    if not os.path.exists(preprocessor_path):
        print("Creating dummy preprocessor...")
        preprocessor = StandardScaler()
        preprocessor.fit(np.random.rand(100, 8))
        joblib.dump(preprocessor, preprocessor_path)
        print(f"✓ Preprocessor saved to {preprocessor_path}")

if __name__ == "__main__":
    create_dummy_models()
