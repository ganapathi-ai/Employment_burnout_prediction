# 📡 API Documentation

Complete API reference for the Employee Burnout Prediction System.

## Base URL

**Local**: `http://localhost:8000`  
**Production**: `https://burnout-api.onrender.com`

## Authentication

Currently no authentication required. Future versions will implement API keys.

## Endpoints

### 1. Root Endpoint

Get API information.

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Burnout Risk Prediction API v2.0",
  "docs": "/docs",
  "health": "/health",
  "features": "17 engineered features for accurate prediction"
}
```

**Example**:
```bash
curl http://localhost:8000/
```

---

### 2. Health Check

Check API and model status.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-02-14T10:30:00.123456",
  "model_loaded": true
}
```

**Status Codes**:
- `200`: Service healthy
- `503`: Service unavailable (model not loaded)

**Example**:
```bash
curl http://localhost:8000/health
```

---

### 3. Predict Burnout Risk

Make burnout risk prediction.

**Endpoint**: `POST /predict`

**Request Body**:
```json
{
  "work_hours": 8.5,
  "screen_time_hours": 10.2,
  "meetings_count": 4,
  "breaks_taken": 3,
  "after_hours_work": 0,
  "sleep_hours": 7.5,
  "task_completion_rate": 85.0,
  "day_type": "Weekday",
  "name": "John Doe",
  "user_id": "user123"
}
```

**Field Constraints**:

| Field | Type | Range | Required | Description |
|-------|------|-------|----------|-------------|
| work_hours | float | 0-24 | Yes | Daily work hours |
| screen_time_hours | float | 0-24 | Yes | Screen time in hours |
| meetings_count | int | 0-20 | Yes | Number of meetings |
| breaks_taken | int | 0-10 | Yes | Number of breaks |
| after_hours_work | int | 0-1 | Yes | 1=Yes, 0=No |
| sleep_hours | float | 0-12 | Yes | Sleep duration |
| task_completion_rate | float | 0-100 | Yes | Task completion % |
| day_type | string | "Weekday" or "Weekend" | Yes | Day type |
| name | string | - | No* | User name |
| user_id | string | - | No* | User identifier |

*At least one of `name` or `user_id` must be provided.

**Response**:
```json
{
  "risk_level": "Low",
  "risk_probability": 0.15,
  "timestamp": "2024-02-14T10:30:00.123456",
  "features": {
    "work_hours": 8.5,
    "screen_time_hours": 10.2,
    "meetings_count": 4,
    "breaks_taken": 3,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85.0,
    "is_weekday": 1,
    "work_intensity_ratio": 1.2,
    "meeting_burden": 0.47,
    "break_adequacy": 0.35,
    "sleep_deficit": 0.5,
    "recovery_index": 0.3,
    "fatigue_risk": -1.05,
    "workload_pressure": 9.5,
    "task_efficiency": 10.0,
    "work_life_balance_score": 65.5,
    "screen_time_per_meeting": 2.55,
    "work_hours_productivity": 76.5,
    "health_risk_score": 12.5,
    "after_hours_work_hours_est": 0.0,
    "high_workload_flag": 1,
    "poor_recovery_flag": 0,
    "name": "John Doe",
    "user_id": "user123"
  }
}
```

**Status Codes**:
- `200`: Prediction successful
- `422`: Validation error (invalid input)
- `500`: Server error
- `503`: Model not loaded

**Examples**:

**cURL**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "work_hours": 8.5,
    "screen_time_hours": 10.2,
    "meetings_count": 4,
    "breaks_taken": 3,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85.0,
    "day_type": "Weekday",
    "name": "John Doe",
    "user_id": "user123"
  }'
```

**Python**:
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "work_hours": 8.5,
    "screen_time_hours": 10.2,
    "meetings_count": 4,
    "breaks_taken": 3,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85.0,
    "day_type": "Weekday",
    "name": "John Doe",
    "user_id": "user123"
}

response = requests.post(url, json=data)
result = response.json()
print(f"Risk Level: {result['risk_level']}")
print(f"Probability: {result['risk_probability']:.2%}")
```

**JavaScript**:
```javascript
const url = 'http://localhost:8000/predict';
const data = {
  work_hours: 8.5,
  screen_time_hours: 10.2,
  meetings_count: 4,
  breaks_taken: 3,
  after_hours_work: 0,
  sleep_hours: 7.5,
  task_completion_rate: 85.0,
  day_type: 'Weekday',
  name: 'John Doe',
  user_id: 'user123'
};

fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(result => {
  console.log('Risk Level:', result.risk_level);
  console.log('Probability:', result.risk_probability);
});
```

---

### 4. Metrics (Prometheus)

Get Prometheus metrics.

**Endpoint**: `GET /metrics`

**Response**:
```json
{
  "status": "metrics placeholder",
  "model_loaded": true
}
```

**Note**: Full Prometheus metrics implementation coming soon.

---

## Feature Engineering

The API automatically engineers 17 features from 8 input features:

### Input Features (8)
1. work_hours
2. screen_time_hours
3. meetings_count
4. breaks_taken
5. after_hours_work
6. sleep_hours
7. task_completion_rate
8. is_weekday (encoded from day_type)

### Engineered Features (9)
1. **work_intensity_ratio** = screen_time / (work_hours + 0.1)
2. **meeting_burden** = meetings / (work_hours + 0.1)
3. **break_adequacy** = breaks / (work_hours + 0.1)
4. **sleep_deficit** = 8 - sleep_hours
5. **recovery_index** = (sleep + breaks) - screen_time
6. **fatigue_risk** = screen_time - (sleep * 1.5)
7. **workload_pressure** = work_hours + (meetings * 0.25) + after_hours
8. **task_efficiency** = task_rate / (work_hours + 0.1)
9. **work_life_balance_score** = Complex formula (0-100)

### Additional Metrics (6)
- screen_time_per_meeting
- work_hours_productivity
- health_risk_score
- after_hours_work_hours_est
- high_workload_flag
- poor_recovery_flag

## Error Handling

### Validation Errors (422)

**Example**: Missing required field
```json
{
  "detail": [
    {
      "loc": ["body", "work_hours"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Example**: Out of range value
```json
{
  "detail": [
    {
      "loc": ["body", "work_hours"],
      "msg": "ensure this value is less than or equal to 24",
      "type": "value_error.number.not_le"
    }
  ]
}
```

### Server Errors (500)

```json
{
  "detail": "Internal server error: <error message>"
}
```

### Service Unavailable (503)

```json
{
  "detail": "Model not loaded"
}
```

## Rate Limiting

Currently no rate limiting. Future versions will implement:
- 100 requests/minute per IP
- 1000 requests/hour per IP

## Interactive Documentation

Visit `/docs` for interactive Swagger UI:
- **Local**: http://localhost:8000/docs
- **Production**: https://burnout-api.onrender.com/docs

Features:
- Try API endpoints directly
- View request/response schemas
- Download OpenAPI spec

## Testing with Postman

### 1. Import Collection

Create new collection with these requests:

**Health Check**:
- Method: GET
- URL: `{{base_url}}/health`

**Predict - Low Risk**:
- Method: POST
- URL: `{{base_url}}/predict`
- Body (JSON):
```json
{
  "work_hours": 8,
  "screen_time_hours": 6,
  "meetings_count": 3,
  "breaks_taken": 4,
  "after_hours_work": 0,
  "sleep_hours": 8,
  "task_completion_rate": 90,
  "day_type": "Weekday",
  "name": "Test User",
  "user_id": "test001"
}
```

**Predict - High Risk**:
- Method: POST
- URL: `{{base_url}}/predict`
- Body (JSON):
```json
{
  "work_hours": 14,
  "screen_time_hours": 13,
  "meetings_count": 10,
  "breaks_taken": 0,
  "after_hours_work": 1,
  "sleep_hours": 4,
  "task_completion_rate": 50,
  "day_type": "Weekday",
  "name": "Stressed User",
  "user_id": "test002"
}
```

### 2. Environment Variables

Set in Postman:
- `base_url`: `http://localhost:8000` (local)
- `base_url`: `https://burnout-api.onrender.com` (production)

## Database Storage

All predictions are automatically stored in Neon Postgres with 27 columns:

**Metadata (4)**:
- id, user_id, name, created_at

**Input Features (8)**:
- work_hours, screen_time_hours, meetings_count, breaks_taken, after_hours_work, sleep_hours, task_completion_rate, is_weekday

**Engineered Features (15)**:
- All calculated features

## Performance

- **Response Time**: <100ms (average)
- **Throughput**: ~100 requests/second
- **Model Inference**: <50ms
- **Database Write**: <30ms

## Versioning

Current version: **v2.0.0**

Version history:
- v2.0.0: Feature engineering, database storage, W&B tracking
- v1.0.0: Initial release with basic prediction

## Support

- 📧 Issues: [GitHub Issues](https://github.com/ganapathi-ai/Employment_burnout_prediction/issues)
- 📚 Docs: [README.md](README.md)
- 🏗️ Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

---

**API Status**: ✅ Production Ready
