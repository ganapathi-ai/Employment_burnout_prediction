#!/usr/bin/env python3
"""Test prediction endpoint directly"""
import json
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

test_payload = {
    "work_hours": 8.0,
    "screen_time_hours": 6.0,
    "meetings_count": 3,
    "breaks_taken": 2,
    "after_hours_work": 0,
    "sleep_hours": 7.0,
    "task_completion_rate": 80.0,
    "day_type": "Weekday",
    "name": "Test User",
    "user_id": "test123"
}

print("Testing /predict endpoint...")
print(f"Payload: {json.dumps(test_payload, indent=2)}")

response = client.post("/predict", json=test_payload)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    data = response.json()
    print("\nSUCCESS")
    print(f"  Risk Level: {data['risk_level']}")
    print(f"  Probability: {data['risk_probability']:.2%}")
    print(f"  Timestamp: {data['timestamp']}")
    print(f"  Features returned: {len(data['features'])}")
else:
    print("\nFAILED")
    print(f"  Error: {response.text}")
