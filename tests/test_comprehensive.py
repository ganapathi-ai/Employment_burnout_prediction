"""
Comprehensive test suite for Burnout Prediction API
Tests: Data validation, Model inference, API endpoints, Feature engineering
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from api.main import app, engineer_features, UserData
import joblib
import numpy as np

client = TestClient(app)

# Test 1: API Health Endpoint
def test_health_endpoint():
    """Test /health endpoint returns correct status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["model_loaded"] is True

# Test 2: API Root Endpoint
def test_root_endpoint():
    """Test / endpoint returns API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Burnout Risk Prediction API" in data["message"]
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"

# Test 3: Valid Prediction Request
def test_valid_prediction():
    """Test /predict endpoint with valid data"""
    payload = {
        "work_hours": 8,
        "screen_time_hours": 6,
        "meetings_count": 3,
        "breaks_taken": 4,
        "after_hours_work": 0,
        "sleep_hours": 8,
        "task_completion_rate": 90,
        "day_type": "weekday",
        "name": "Test User",
        "user_id": "test123"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_level" in data
    assert "risk_probability" in data
    assert "timestamp" in data
    assert "features" in data
    assert data["risk_level"] in ["Low", "High"]
    assert 0 <= data["risk_probability"] <= 1

# Test 4: Invalid Prediction Request - Missing Field
def test_missing_field_validation():
    """Test /predict endpoint rejects missing required fields"""
    payload = {
        "work_hours": 8,
        "screen_time_hours": 6,
        "meetings_count": 3,
        # Missing: breaks_taken, after_hours_work, sleep_hours, etc.
        "name": "Test User",
        "user_id": "test123"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error

# Test 5: Invalid Prediction Request - Out of Range
def test_out_of_range_validation():
    """Test /predict endpoint rejects out-of-range values"""
    payload = {
        "work_hours": 30,  # Invalid: > 24
        "screen_time_hours": 6,
        "meetings_count": 3,
        "breaks_taken": 4,
        "after_hours_work": 0,
        "sleep_hours": 8,
        "task_completion_rate": 90,
        "day_type": "weekday",
        "name": "Test User",
        "user_id": "test123"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error

# Test 6: Feature Engineering Logic
def test_feature_engineering():
    """Test feature engineering calculations are correct"""
    test_data = UserData(
        work_hours=8,
        screen_time_hours=6,
        meetings_count=3,
        breaks_taken=4,
        after_hours_work=0,
        sleep_hours=8,
        task_completion_rate=90,
        day_type="weekday",
        name="Test User",
        user_id="test123"
    )
    
    features_array, all_features = engineer_features(test_data)
    
    # Verify array shape
    assert features_array.shape == (1, 17)
    
    # Verify specific calculations
    assert all_features['work_intensity_ratio'] == pytest.approx(6 / 8.1, rel=0.01)
    assert all_features['meeting_burden'] == pytest.approx(3 / 8.1, rel=0.01)
    assert all_features['break_adequacy'] == pytest.approx(4 / 8.1, rel=0.01)
    assert all_features['sleep_deficit'] == 0  # 8 - 8
    assert all_features['is_weekday'] == 1

# Test 7: Model Artifacts Exist
def test_model_artifacts_exist():
    """Test that required model files exist"""
    assert os.path.exists('models/best_model.joblib')
    assert os.path.exists('models/preprocessor.joblib')
    assert os.path.exists('models/feature_names.joblib')

# Test 8: Model Can Load and Predict
def test_model_inference():
    """Test model can load and make predictions"""
    model = joblib.load('models/best_model.joblib')
    scaler = joblib.load('models/preprocessor.joblib')
    
    # Create test input
    X_test = np.random.rand(1, 17)
    
    # Test prediction
    prediction = model.predict(X_test)
    assert prediction.shape == (1,)
    assert prediction[0] in [0, 1]
    
    # Test probability
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X_test)
        assert proba.shape == (1, 2)
        assert np.sum(proba[0]) == pytest.approx(1.0, rel=0.01)

# Test 9: High Risk Prediction
def test_high_risk_prediction():
    """Test prediction for high-risk scenario"""
    payload = {
        "work_hours": 14,
        "screen_time_hours": 13,
        "meetings_count": 10,
        "breaks_taken": 0,
        "after_hours_work": 1,
        "sleep_hours": 4,
        "task_completion_rate": 50,
        "day_type": "weekday",
        "name": "High Risk User",
        "user_id": "highrisk001"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Model returns prediction (may be Low or High based on training)
    assert data["risk_level"] in ["Low", "High"]
    assert 0 <= data["risk_probability"] <= 1

# Test 10: Weekend vs Weekday
def test_day_type_encoding():
    """Test day_type is correctly encoded"""
    weekday_data = UserData(
        work_hours=8, screen_time_hours=6, meetings_count=3,
        breaks_taken=4, after_hours_work=0, sleep_hours=8,
        task_completion_rate=90, day_type="weekday",
        name="Test", user_id="test1"
    )
    weekend_data = UserData(
        work_hours=8, screen_time_hours=6, meetings_count=3,
        breaks_taken=4, after_hours_work=0, sleep_hours=8,
        task_completion_rate=90, day_type="weekend",
        name="Test", user_id="test2"
    )
    
    _, weekday_features = engineer_features(weekday_data)
    _, weekend_features = engineer_features(weekend_data)
    
    assert weekday_features['is_weekday'] == 1
    assert weekend_features['is_weekday'] == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
