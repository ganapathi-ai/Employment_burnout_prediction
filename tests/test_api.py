#!/usr/bin/env python3
# File: tests/test_api.py

import os
import pytest
from fastapi.testclient import TestClient

# ensure tests use an in-memory SQLite database
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

from api.main import app, engine, user_requests

client = TestClient(app)

VALID_DATA = {
    "work_hours": 8.5,
    "screen_time_hours": 10.2,
    "meetings_count": 4,
    "breaks_taken": 3,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85.0,
    "day_type": "Weekday",
    "name": "Test User"
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
        # new field with full feature set
        assert "features" in data
        assert isinstance(data["features"], dict)
        # basic sanity checks on feature content
        assert "work_hours" in data["features"]
        assert "work_intensity_ratio" in data["features"]
        # additional engineered values added recently
        assert "meeting_burden" in data["features"]
        assert "health_risk_score" in data["features"]
        assert "high_workload_flag" in data["features"]
        assert "poor_recovery_flag" in data["features"]

    def test_predict_probability_range(self):
        response = client.post("/predict", json=VALID_DATA)
        data = response.json()
        assert 0 <= data["risk_probability"] <= 1

    def test_db_insertion(self):
        # count rows before
        with engine.connect() as conn:
            before_rows = conn.execute(user_requests.select()).fetchall()
            before = len(before_rows)
        response = client.post("/predict", json=VALID_DATA)
        assert response.status_code == 200
        # count after insertion
        with engine.connect() as conn:
            after_rows = conn.execute(user_requests.select()).fetchall()
            after = len(after_rows)
            rows = conn.execute(user_requests.select().order_by(user_requests.c.id.desc()).limit(1)).fetchall()
        assert after == before + 1
        # the latest row should contain our name or user_id
        assert rows, "no rows returned"
        latest = rows[0]
        assert latest.name == VALID_DATA["name"] or latest.user_id == VALID_DATA.get("user_id")

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
