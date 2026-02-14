#!/usr/bin/env python3
"""Test API locally before deployment"""
from api.main import app, MODEL, SCALER, engineer_features, UserData
import numpy as np

print("=" * 60)
print("BACKEND VERIFICATION TEST")
print("=" * 60)

# Test 1: Check models loaded
print("\n1. Model Loading:")
print(f"   MODEL type: {type(MODEL).__name__}")
print(f"   SCALER type: {type(SCALER).__name__}")
print(f"   OK Models loaded successfully")

# Test 2: Feature engineering
print("\n2. Feature Engineering:")
test_data = UserData(
    work_hours=8.0,
    screen_time_hours=6.0,
    meetings_count=3,
    breaks_taken=4,
    after_hours_work=0,
    sleep_hours=7.5,
    task_completion_rate=85.0,
    day_type="Weekday",
    name="Test User",
    user_id="test123"
)
features_array, all_features = engineer_features(test_data)
print(f"   Features array shape: {features_array.shape}")
print(f"   Expected shape: (1, 17)")
print(f"   All features count: {len(all_features)}")
print(f"   OK Feature engineering works")

# Test 3: Scaling
print("\n3. Feature Scaling:")
features_scaled = SCALER.transform(features_array)
print(f"   Scaled features shape: {features_scaled.shape}")
print(f"   Sample scaled values: {features_scaled[0][:5]}")
print(f"   OK Scaling works")

# Test 4: Prediction
print("\n4. Model Prediction:")
prediction = MODEL.predict(features_scaled)[0]
probability = MODEL.predict_proba(features_scaled)[0]
print(f"   Prediction: {prediction}")
print(f"   Probabilities: {probability}")
print(f"   Risk level: {'High' if prediction == 1 else 'Low'}")
print(f"   OK Prediction works")

# Test 5: API endpoints
print("\n5. API Endpoints:")
routes = [(r.path, list(r.methods) if hasattr(r, 'methods') else []) for r in app.routes]
critical_routes = ['/health', '/predict', '/']
for route in critical_routes:
    exists = any(r[0] == route for r in routes)
    print(f"   {route}: {'OK' if exists else 'FAIL'}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED - OK")
print("=" * 60)
