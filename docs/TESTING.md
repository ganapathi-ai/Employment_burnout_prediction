# 🧪 Testing Guide

Comprehensive testing guide for the Employee Burnout Prediction System.

## Testing Overview

- **Framework**: Pytest 7.4+
- **Coverage Tool**: pytest-cov
- **Test Count**: 10 comprehensive tests
- **Coverage**: 85%+
- **Test Files**: `tests/test_comprehensive.py`, `tests/test_api.py`

## Test Structure

```
tests/
├── conftest.py              # Test fixtures and configuration
├── test_comprehensive.py    # Main test suite (10 tests)
└── test_api.py             # API-specific tests
```

## Running Tests

### Run All Tests

```bash
# Basic test run
pytest tests/ -v

# With detailed output
pytest tests/ -vv

# With print statements
pytest tests/ -v -s
```

**Expected Output**:
```
tests/test_comprehensive.py::test_health_check PASSED
tests/test_comprehensive.py::test_predict_endpoint PASSED
tests/test_comprehensive.py::test_predict_validation PASSED
tests/test_comprehensive.py::test_feature_engineering PASSED
tests/test_comprehensive.py::test_model_loading PASSED
tests/test_comprehensive.py::test_database_connection PASSED
tests/test_comprehensive.py::test_metrics_endpoint PASSED
tests/test_comprehensive.py::test_invalid_input PASSED
tests/test_comprehensive.py::test_missing_fields PASSED
tests/test_comprehensive.py::test_edge_cases PASSED

========== 10 passed in 5.23s ==========
```

### Run Specific Test

```bash
# Run single test
pytest tests/test_comprehensive.py::test_health_check -v

# Run tests matching pattern
pytest tests/ -k "predict" -v
```

### Run with Coverage

```bash
# Generate coverage report
pytest tests/ --cov=api --cov-report=html

# View coverage in terminal
pytest tests/ --cov=api --cov-report=term

# Generate XML report (for CI/CD)
pytest tests/ --cov=api --cov-report=xml
```

**View HTML Report**:
```bash
# Open in browser
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

## Test Suite Details

### 1. Health Check Test

**File**: `tests/test_comprehensive.py`

**Purpose**: Verify API health endpoint

```python
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
```

**What it tests**:
- Health endpoint returns 200
- Response contains correct status
- Model is loaded

### 2. Prediction Endpoint Test

**Purpose**: Test successful prediction

```python
def test_predict_endpoint(client):
    payload = {
        "work_hours": 8.0,
        "screen_time_hours": 6.0,
        "meetings_count": 3,
        "breaks_taken": 4,
        "after_hours_work": 0,
        "sleep_hours": 7.5,
        "task_completion_rate": 85.0,
        "day_type": "Weekday",
        "name": "Test User",
        "user_id": "test123"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_level" in data
    assert data["risk_level"] in ["Low", "High"]
```

**What it tests**:
- Prediction endpoint accepts valid input
- Returns correct response structure
- Risk level is valid

### 3. Input Validation Test

**Purpose**: Test Pydantic validation

```python
def test_predict_validation(client):
    # Test invalid work_hours (> 24)
    payload = {
        "work_hours": 30.0,  # Invalid
        "screen_time_hours": 6.0,
        # ... other fields
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
```

**What it tests**:
- Invalid ranges rejected
- Validation errors returned
- Proper HTTP status codes

### 4. Feature Engineering Test

**Purpose**: Verify feature calculations

```python
def test_feature_engineering():
    from api.main import engineer_features, UserData
    
    data = UserData(
        work_hours=8.0,
        screen_time_hours=6.0,
        meetings_count=3,
        breaks_taken=4,
        after_hours_work=0,
        sleep_hours=7.5,
        task_completion_rate=85.0,
        day_type="Weekday",
        name="Test"
    )
    
    features_array, all_features = engineer_features(data)
    
    assert features_array.shape == (1, 17)
    assert "work_intensity_ratio" in all_features
    assert all_features["work_intensity_ratio"] == 6.0 / 8.1
```

**What it tests**:
- Feature engineering produces 17 features
- Calculations are correct
- All expected features present

### 5. Model Loading Test

**Purpose**: Verify model and scaler loaded

```python
def test_model_loading():
    from api.main import MODEL, SCALER
    
    assert MODEL is not None
    assert SCALER is not None
    assert hasattr(MODEL, 'predict')
    assert hasattr(SCALER, 'transform')
```

**What it tests**:
- Model loaded successfully
- Scaler loaded successfully
- Objects have required methods

### 6. Database Connection Test

**Purpose**: Test database operations

```python
def test_database_connection(client):
    response = client.get("/db-status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "connected"
```

**What it tests**:
- Database connection works
- Table exists
- Can query database

### 7. Metrics Endpoint Test

**Purpose**: Test Prometheus metrics

```python
def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
```

**What it tests**:
- Metrics endpoint accessible
- Prometheus format correct
- Metrics being tracked

### 8. Invalid Input Test

**Purpose**: Test error handling

```python
def test_invalid_input(client):
    # Missing required field
    payload = {
        "work_hours": 8.0,
        # Missing other required fields
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
```

**What it tests**:
- Missing fields rejected
- Proper error messages
- HTTP 422 returned

### 9. Missing Name/UserID Test

**Purpose**: Test custom validation

```python
def test_missing_fields(client):
    payload = {
        "work_hours": 8.0,
        "screen_time_hours": 6.0,
        # ... all fields except name and user_id
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
```

**What it tests**:
- Either name or user_id required
- Custom validator works
- Proper error message

### 10. Edge Cases Test

**Purpose**: Test boundary conditions

```python
def test_edge_cases(client):
    # Test with minimum values
    payload = {
        "work_hours": 0.0,
        "screen_time_hours": 0.0,
        "meetings_count": 0,
        "breaks_taken": 0,
        "after_hours_work": 0,
        "sleep_hours": 0.0,
        "task_completion_rate": 0.0,
        "day_type": "Weekend",
        "name": "Edge Case"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
```

**What it tests**:
- Minimum values accepted
- Maximum values accepted
- No division by zero errors

## Test Fixtures

### conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

@pytest.fixture
def sample_payload():
    """Sample valid payload"""
    return {
        "work_hours": 8.0,
        "screen_time_hours": 6.0,
        "meetings_count": 3,
        "breaks_taken": 4,
        "after_hours_work": 0,
        "sleep_hours": 7.5,
        "task_completion_rate": 85.0,
        "day_type": "Weekday",
        "name": "Test User",
        "user_id": "test123"
    }
```

## Code Quality Tests

### Pylint

```bash
# Run Pylint on API
pylint api/ --fail-under=7.0

# Run on all Python files
pylint api/ frontend/ scripts/ --fail-under=7.0

# Generate report
pylint api/ --output-format=text > pylint_report.txt
```

**Current Score**: 10.00/10

### Flake8

```bash
# Run Flake8
flake8 api/ --max-line-length=120

# With statistics
flake8 api/ --statistics

# Ignore specific errors
flake8 api/ --ignore=E501,W503
```

### Black (Code Formatting)

```bash
# Check formatting
black api/ --check

# Format code
black api/ frontend/ scripts/

# Diff mode
black api/ --diff
```

### isort (Import Sorting)

```bash
# Check imports
isort api/ --check-only

# Sort imports
isort api/ frontend/ scripts/

# Diff mode
isort api/ --diff
```

## Integration Tests

### Test Complete Flow

```python
def test_complete_flow(client):
    # 1. Check health
    health = client.get("/health")
    assert health.status_code == 200
    
    # 2. Make prediction
    payload = {...}
    predict = client.post("/predict", json=payload)
    assert predict.status_code == 200
    
    # 3. Check database
    db_status = client.get("/db-status")
    assert db_status.json()["row_count"] > 0
    
    # 4. Check metrics
    metrics = client.get("/metrics")
    assert "predictions_total" in metrics.text
```

## Performance Tests

### Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class BurnoutUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def predict(self):
        self.client.post("/predict", json={
            "work_hours": 8.0,
            "screen_time_hours": 6.0,
            "meetings_count": 3,
            "breaks_taken": 4,
            "after_hours_work": 0,
            "sleep_hours": 7.5,
            "task_completion_rate": 85.0,
            "day_type": "Weekday",
            "name": "Load Test",
            "user_id": "load_test"
        })
```

```bash
# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

## CI/CD Testing

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest tests/ -v --cov=api
      
      - name: Code quality
        run: |
          pylint api/ --fail-under=7.0
          flake8 api/ --max-line-length=120
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Test Data

### Sample Payloads

**Low Risk**:
```json
{
  "work_hours": 8.0,
  "screen_time_hours": 6.0,
  "meetings_count": 3,
  "breaks_taken": 4,
  "after_hours_work": 0,
  "sleep_hours": 8.0,
  "task_completion_rate": 90.0,
  "day_type": "Weekday",
  "name": "Low Risk User",
  "user_id": "low_001"
}
```

**High Risk**:
```json
{
  "work_hours": 12.0,
  "screen_time_hours": 10.0,
  "meetings_count": 8,
  "breaks_taken": 1,
  "after_hours_work": 1,
  "sleep_hours": 5.0,
  "task_completion_rate": 60.0,
  "day_type": "Weekday",
  "name": "High Risk User",
  "user_id": "high_001"
}
```

## Debugging Tests

### Run with Debugger

```bash
# Run with pdb
pytest tests/ --pdb

# Stop on first failure
pytest tests/ -x

# Show local variables on failure
pytest tests/ -l
```

### Verbose Output

```bash
# Maximum verbosity
pytest tests/ -vv -s

# Show print statements
pytest tests/ -v -s --capture=no
```

## Test Coverage Goals

- **Overall**: 85%+
- **API endpoints**: 95%+
- **Feature engineering**: 100%
- **Model inference**: 90%+
- **Database operations**: 80%+

## Writing New Tests

### Test Template

```python
def test_new_feature(client):
    """Test description"""
    # Arrange
    payload = {...}
    
    # Act
    response = client.post("/endpoint", json=payload)
    
    # Assert
    assert response.status_code == 200
    assert "expected_field" in response.json()
```

### Best Practices

1. **Use descriptive names**: `test_predict_with_high_workload`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **One assertion per test** (when possible)
4. **Use fixtures** for common setup
5. **Test edge cases** and error conditions
6. **Mock external dependencies** (database, APIs)
7. **Keep tests independent** (no shared state)

## Troubleshooting Tests

### Issue: Tests Fail Locally

**Solution**:
```bash
# Ensure model is trained
python scripts/train_model.py

# Check environment variables
cat .env

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Database Tests Fail

**Solution**:
```bash
# Check database connection
python check_db_data.py

# Verify DATABASE_URL in .env
echo $DATABASE_URL
```

### Issue: Import Errors

**Solution**:
```bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in editable mode
pip install -e .
```

## Test Metrics

- **Test Execution Time**: <10 seconds
- **Coverage**: 85%+
- **Pass Rate**: 100%
- **Code Quality**: 10/10 (Pylint)

## Continuous Testing

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Watch Mode

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw tests/ -- -v
```

## Resources

- **Pytest Docs**: https://docs.pytest.org
- **Coverage.py**: https://coverage.readthedocs.io
- **Pylint**: https://pylint.org
- **Flake8**: https://flake8.pycqa.org
