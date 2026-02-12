# File: tests/conftest.py

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from api.main import app  # noqa: E402


@pytest.fixture(scope="session")
def test_client():
    """Provide FastAPI test client"""
    return TestClient(app)


@pytest.fixture(scope="session")
def sample_user_data():
    """Provide sample user data for testing"""
    return {
        "work_hours": 8.5,
        "screen_time_hours": 10.2,
        "meetings_count": 4,
        "breaks_taken": 3,
        "after_hours_work": 0,
        "sleep_hours": 7.5,
        "task_completion_rate": 85.0,
        "day_type": "Weekday"
    }


@pytest.fixture
def mock_model():
    """Mock the ML model"""
    from unittest.mock import MagicMock
    model = MagicMock()
    model.predict.return_value = [0]  # Low risk
    model.predict_proba.return_value = [[0.85, 0.15]]  # 15% high risk prob
    return model


@pytest.fixture(autouse=True)
def mock_model_global(mock_model, monkeypatch):
    """Auto-use fixture to mock global model in api.main"""
    monkeypatch.setattr("api.main.model", mock_model)
    return mock_model
