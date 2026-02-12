#!/usr/bin/env python3
# File: tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

VALID_DATA = {
    "work_hours": 8.5,
    "screen_time_hours": 10.2,
    "meetings_count": 4,
    "breaks_taken": 3,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85.0,
    "day_type": "Weekday"
}


class TestHealthEndpoint:
    def test_health_check_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response(self):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestPredictEndpoint:
    def test_predict_valid_input(self):
        response = client.post("/predict", json=VALID_DATA)
        assert response.status_code == 200

    def test_predict_response_format(self):
        response = client.post("/predict", json=VALID_DATA)
        data = response.json()
        assert "risk_level" in data
        assert "risk_probability" in data
        assert data["risk_level"] in ["Low", "High"]

    def test_predict_probability_range(self):
        response = client.post("/predict", json=VALID_DATA)
        data = response.json()
        assert 0 <= data["risk_probability"] <= 1

    def test_predict_missing_field(self):
        invalid = VALID_DATA.copy()
        del invalid["work_hours"]
        response = client.post("/predict", json=invalid)
        assert response.status_code == 422

    def test_predict_invalid_range(self):
        invalid = VALID_DATA.copy()
        invalid["work_hours"] = -5
        response = client.post("/predict", json=invalid)
        assert response.status_code == 422


class TestMetricsEndpoint:
    def test_metrics_endpoint(self):
        response = client.get("/metrics")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
