# 📡 API Documentation

Complete API reference for the Employee Burnout Prediction System.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-app.onrender.com`

## Authentication

Currently, no authentication is required. Future versions will implement JWT-based authentication.

## Endpoints Overview

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | API information | No |
| `/health` | GET | Health check | No |
| `/predict` | POST | Burnout prediction | No |
| `/metrics` | GET | Prometheus metrics | No |
| `/docs` | GET | Interactive API docs | No |
| `/db-status` | GET | Database status | No |

---

## 1. Root Endpoint

### `GET /`

Get API information and available endpoints.

**Request**:
```bash
curl http://localhost:8000/
```

**Response** (200 OK):
```json
{
  "message": "Burnout Risk Prediction API v2.0",
  "docs": "/docs",
  "health": "/health",
  "features": "17 engineered features for accurate prediction"
}
```

---

## 2. Health Check

### `GET /health`

Check if the API and ML model are loaded and healthy.

**Request**:
```bash
curl http://localhost:8000/health
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2024-02-14T10:30:00.123456",
  "model_loaded": true
}
```

**Response Fields**:
- `status` (string): "healthy" or "unhealthy"
- `timestamp` (string): ISO 8601 timestamp
- `model_loaded` (boolean): Whether ML model is loaded

**Use Case**: Load balancer health checks, monitoring

---

## 3. Burnout Prediction

### `POST /predict`

Predict burnout risk based on work-from-home metrics.

**Request**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "work_hours": 8.0,
    "screen_time_hours": 6.0,
    "meetings_count": 3,
    "breaks_taken": 4,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85.0,
    "day_type": "Weekday",
    "name": "John Doe",
    "user_id": "user123"
  }'
```

**Request Body** (JSON):

| Field | Type | Required | Range | Description |
|-------|------|----------|-------|-------------|
| `work_hours` | float | Yes | 0-24 | Daily work hours |
| `screen_time_hours` | float | Yes | 0-24 | Screen time in hours |
| `meetings_count` | integer | Yes | 0-20 | Number of meetings |
| `breaks_taken` | integer | Yes | 0-10 | Number of breaks |
| `after_hours_work` | integer | Yes | 0-1 | After-hours work (0=No, 1=Yes) |
| `sleep_hours` | float | Yes | 0-12 | Sleep duration |
| `task_completion_rate` | float | Yes | 0-100 | Task completion percentage |
| `day_type` | string | Yes | - | "Weekday" or "Weekend" |
| `name` | string | No | - | User name (for tracking) |
| `user_id` | string | No | - | User ID (for tracking) |

**Note**: Either `name` or `user_id` must be provided.

**Response** (200 OK):
```json
{
  "risk_level": "Low",
  "risk_probability": 0.15,
  "timestamp": "2024-02-14T10:30:00.123456",
  "features": {
    "work_hours": 8.0,
    "screen_time_hours": 6.0,
    "meetings_count": 3,
    "breaks_taken": 4,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85.0,
    "is_weekday": 1,
    "work_intensity_ratio": 0.75,
    "meeting_burden": 0.375,
    "break_adequacy": 0.5,
    "sleep_deficit": 0.5,
    "recovery_index": 5.5,
    "fatigue_risk": -5.25,
    "workload_pressure": 8.75,
    "task_efficiency": 10.625,
    "work_life_balance_score": 72.5,
    "screen_time_per_meeting": 2.0,
    "work_hours_productivity": 39.67,
    "health_risk_score": 2.5,
    "after_hours_work_hours_est": 0.0,
    "high_workload_flag": 0,
    "poor_recovery_flag": 0,
    "name": "John Doe",
    "user_id": "user123"
  }
}
```

**Response Fields**:
- `risk_level` (string): "Low" or "High"
- `risk_probability` (float): Probability of burnout (0-1)
- `timestamp` (string): Prediction timestamp
- `features` (object): All input and engineered features

**Error Responses**:

**422 Unprocessable Entity** (Validation Error):
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

**503 Service Unavailable** (Model Not Loaded):
```json
{
  "detail": "Model not loaded"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Error message here"
}
```

---

## 4. Database Status

### `GET /db-status`

Check database connection and table status.

**Request**:
```bash
curl http://localhost:8000/db-status
```

**Response** (200 OK):
```json
{
  "status": "connected",
  "table_exists": true,
  "row_count": 42,
  "database_url": "postgresql://neondb_owner:***@ep-rapid-grass..."
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "connection refused",
  "database_url": "postgresql://..."
}
```

---

## 5. Prometheus Metrics

### `GET /metrics`

Export Prometheus metrics for monitoring.

**Request**:
```bash
curl http://localhost:8000/metrics
```

**Response** (200 OK):
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{endpoint="/predict",method="POST",status="200"} 42.0

# HELP api_request_duration_seconds Request latency
# TYPE api_request_duration_seconds histogram
api_request_duration_seconds_bucket{endpoint="/predict",method="POST",le="0.005"} 10.0

# HELP predictions_total Total predictions made
# TYPE predictions_total counter
predictions_total{risk_level="High"} 15.0
predictions_total{risk_level="Low"} 27.0

# HELP model_loaded Whether model is loaded (1=yes, 0=no)
# TYPE model_loaded gauge
model_loaded 1.0
```

**Metrics Available**:
- `api_requests_total`: Total API requests (by method, endpoint, status)
- `api_request_duration_seconds`: Request latency histogram
- `predictions_total`: Total predictions (by risk level)
- `api_active_requests`: Current active requests
- `model_loaded`: Model load status (1=loaded, 0=not loaded)
- `database_operations_total`: Database operations (by operation, status)

---

## 6. Interactive API Docs

### `GET /docs`

Access Swagger UI for interactive API documentation.

**URL**: http://localhost:8000/docs

**Features**:
- Try out endpoints directly
- View request/response schemas
- See validation rules
- Download OpenAPI spec

---

## Feature Engineering Details

The API automatically engineers 9 additional features from 8 input features:

### Input Features (8)
1. `work_hours` - Daily work hours
2. `screen_time_hours` - Screen time
3. `meetings_count` - Number of meetings
4. `breaks_taken` - Number of breaks
5. `after_hours_work` - After-hours work flag
6. `sleep_hours` - Sleep duration
7. `task_completion_rate` - Task completion %
8. `day_type` - Weekday/Weekend (converted to `is_weekday`)

### Engineered Features (9)
1. **work_intensity_ratio** = screen_time / (work_hours + 0.1)
2. **meeting_burden** = meetings / (work_hours + 0.1)
3. **break_adequacy** = breaks / (work_hours + 0.1)
4. **sleep_deficit** = 8 - sleep_hours
5. **recovery_index** = (sleep_hours + breaks) - screen_time
6. **fatigue_risk** = screen_time - (sleep_hours * 1.5)
7. **workload_pressure** = work_hours + (meetings * 0.25) + after_hours
8. **task_efficiency** = task_completion_rate / (work_hours + 0.1)
9. **work_life_balance_score** = Complex formula (0-100 scale)

### Additional Derived Metrics (6)
10. **screen_time_per_meeting** = screen_time / (meetings + 0.1)
11. **work_hours_productivity** = task_completion_rate * (1 - work_hours/15)
12. **health_risk_score** = Based on sleep and fatigue (0-100)
13. **after_hours_work_hours_est** = after_hours * (work_hours * 0.1)
14. **high_workload_flag** = 1 if (work_hours > median AND meetings > median)
15. **poor_recovery_flag** = 1 if (sleep < 6 AND recovery_index < 0)

---

## Code Examples

### Python (requests)
```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "work_hours": 10.0,
    "screen_time_hours": 8.0,
    "meetings_count": 5,
    "breaks_taken": 2,
    "after_hours_work": 1,
    "sleep_hours": 6.0,
    "task_completion_rate": 70.0,
    "day_type": "Weekday",
    "name": "Jane Smith",
    "user_id": "user456"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Risk Level: {result['risk_level']}")
print(f"Probability: {result['risk_probability']:.2%}")
```

### JavaScript (fetch)
```javascript
const url = "http://localhost:8000/predict";
const payload = {
  work_hours: 10.0,
  screen_time_hours: 8.0,
  meetings_count: 5,
  breaks_taken: 2,
  after_hours_work: 1,
  sleep_hours: 6.0,
  task_completion_rate: 70.0,
  day_type: "Weekday",
  name: "Jane Smith",
  user_id: "user456"
};

fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
})
  .then(res => res.json())
  .then(data => {
    console.log(`Risk Level: ${data.risk_level}`);
    console.log(`Probability: ${(data.risk_probability * 100).toFixed(2)}%`);
  });
```

### cURL
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "work_hours": 10.0,
    "screen_time_hours": 8.0,
    "meetings_count": 5,
    "breaks_taken": 2,
    "after_hours_work": 1,
    "sleep_hours": 6.0,
    "task_completion_rate": 70.0,
    "day_type": "Weekday",
    "name": "Jane Smith",
    "user_id": "user456"
  }'
```

---

## Rate Limiting

Currently, no rate limiting is implemented. Future versions will include:
- 100 requests/minute per IP
- 1000 requests/hour per user

---

## CORS Configuration

CORS is enabled for all origins:
```python
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

**Production**: Restrict to specific domains.

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Model not loaded |

### Error Response Format
```json
{
  "detail": "Error message or validation details"
}
```

---

## Performance

- **Average Response Time**: <100ms
- **Model Inference**: <50ms
- **Database Write**: <50ms
- **Concurrent Requests**: Supports 100+ concurrent requests

---

## Monitoring

### Health Check Endpoint
Use `/health` for:
- Load balancer health checks
- Uptime monitoring
- Automated alerts

### Metrics Endpoint
Use `/metrics` for:
- Prometheus scraping
- Grafana dashboards
- Performance monitoring

---

## Best Practices

1. **Always validate input** before sending to API
2. **Handle errors gracefully** in your client
3. **Use health check** before making predictions
4. **Log request/response** for debugging
5. **Monitor metrics** in production
6. **Provide either name or user_id** for tracking

---

## Changelog

### v2.0.0 (Current)
- Added 17 engineered features
- Improved model accuracy (98.89%)
- Added Prometheus metrics
- Database integration
- W&B tracking

### v1.0.0
- Initial release
- Basic prediction endpoint
- 8 input features

---

## Support

- **API Docs**: http://localhost:8000/docs
- **GitHub Issues**: [Report Bug](https://github.com/ganapathi-ai/Employment_burnout_prediction/issues)
- **Documentation**: See other docs in `docs/` folder
