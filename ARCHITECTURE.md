# 🏗️ System Architecture

## Overview
Employee Burnout Prediction System - ML-powered burnout risk prediction with real-time API and interactive dashboard.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  STREAMLIT FRONTEND                         │
│  • Interactive UI (Port 8501)                               │
│  • Input Forms & Sliders                                    │
│  • Real-time Visualizations                                 │
│  • Recommendations Engine                                   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP POST /predict
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                           │
│  • REST API (Port 8000)                                     │
│  • Pydantic Validation                                      │
│  • Feature Engineering (17 features)                        │
│  • ML Model Inference                                       │
└──────┬──────────────┬──────────────┬───────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────────┐
│  MODEL   │   │   NEON   │   │  PROMETHEUS  │
│ REGISTRY │   │ POSTGRES │   │   METRICS    │
│          │   │          │   │              │
│ • RF     │   │ • User   │   │ • Requests   │
│ • XGB    │   │   Data   │   │ • Latency    │
│ • GB     │   │ • Preds  │   │ • Errors     │
└──────────┘   └──────────┘   └──────┬───────┘
                                      │
                                      ▼
                               ┌──────────────┐
                               │   GRAFANA    │
                               │  DASHBOARDS  │
                               └──────────────┘
```

## Component Details

### 1. Frontend (Streamlit)
**File**: `frontend/streamlit_app.py`

**Responsibilities**:
- User input collection (8 metrics)
- Feature calculation preview
- API communication
- Result visualization
- Recommendations display

**Key Features**:
- 3 tabs: Input, Analytics, About
- Real-time metric calculations
- Professional labels for all features
- Error handling with 60s timeout

### 2. Backend (FastAPI)
**File**: `api/main.py`

**Responsibilities**:
- REST API endpoints
- Input validation (Pydantic)
- Feature engineering (17 features)
- Model inference
- Database storage
- Metrics collection

**Endpoints**:
- `GET /` - API info
- `GET /health` - Health check
- `POST /predict` - Burnout prediction
- `GET /metrics` - Prometheus metrics

### 3. ML Pipeline
**Files**: `scripts/train_model.py`, `scripts/preprocessing.py`

**Workflow**:
```
Raw Data → Feature Engineering → Train/Test Split → 
Model Training (3 models) → Best Model Selection → 
Model Artifacts → Deployment
```

**Models Trained**:
1. Random Forest (n_estimators=100)
2. Gradient Boosting (n_estimators=100)
3. XGBoost (n_estimators=100)

**Selection Criteria**: Highest ROC-AUC score

### 4. Database (Neon Postgres)
**Schema**: 27 columns
- 4 metadata: id, user_id, name, created_at
- 8 input features: work_hours, screen_time_hours, etc.
- 15 engineered features: work_intensity_ratio, meeting_burden, etc.

**Purpose**: Store all predictions for analytics

### 5. Monitoring Stack
**Prometheus**: Metrics collection
**Grafana**: Visualization dashboards

## Data Flow

### Prediction Request Flow
```
1. User enters metrics in Streamlit
   ↓
2. Frontend calculates preview metrics
   ↓
3. POST request to /predict endpoint
   ↓
4. FastAPI validates input (Pydantic)
   ↓
5. engineer_features() creates 17 features
   ↓
6. Model predicts risk (0 or 1)
   ↓
7. Store prediction in Neon Postgres
   ↓
8. Return result with all features
   ↓
9. Frontend displays risk + recommendations
```

### Training Flow
```
1. Load raw dataset (CSV)
   ↓
2. Apply feature engineering
   ↓
3. Create binary target (High=1, Low=0)
   ↓
4. Train/test split (80/20)
   ↓
5. Scale features (StandardScaler)
   ↓
6. Train 3 models in parallel
   ↓
7. Evaluate with ROC-AUC
   ↓
8. Select best model
   ↓
9. Save artifacts (model, scaler, features)
   ↓
10. Log to W&B (metrics, plots, artifacts)
```

## Feature Engineering

### Input Features (8)
1. work_hours
2. screen_time_hours
3. meetings_count
4. breaks_taken
5. after_hours_work
6. sleep_hours
7. task_completion_rate
8. day_type (encoded to is_weekday)

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

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Interactive UI |
| Backend | FastAPI | REST API |
| ML | scikit-learn, XGBoost | Model training |
| Database | Neon Postgres | Data storage |
| Monitoring | Prometheus, Grafana | Metrics & dashboards |
| ML Tracking | Weights & Biases | Experiment tracking |
| Testing | Pytest | Unit & integration tests |
| CI/CD | GitHub Actions | Automated deployment |
| Deployment | Render | Cloud hosting |
| Containerization | Docker | Consistent environments |

## Deployment Architecture

### Development
```
localhost:8000 (API) + localhost:8501 (Frontend)
```

### Production (Render)
```
https://your-api.onrender.com (Backend)
https://your-app.onrender.com (Frontend)
```

## Security

1. **Environment Variables**: All secrets in .env
2. **Input Validation**: Pydantic models with constraints
3. **CORS**: Configured for frontend origin
4. **Database**: Connection pooling, parameterized queries
5. **API**: Rate limiting (future enhancement)

## Scalability

### Current Capacity
- API: ~100 requests/second
- Database: 10,000 predictions/day
- Model: <100ms inference time

### Future Enhancements
- Redis caching for frequent predictions
- Load balancer for multiple API instances
- Model versioning with A/B testing
- Real-time monitoring alerts

## Code Quality

- **Pylint Score**: 10.00/10
- **Test Coverage**: 10/10 tests passing
- **Code Style**: PEP 8 compliant
- **Type Hints**: Pydantic models

## File Structure

```
├── api/main.py                 # FastAPI backend (400 lines)
├── frontend/streamlit_app.py   # Streamlit UI (500 lines)
├── scripts/
│   ├── train_model.py          # ML training pipeline
│   ├── preprocessing.py        # Data preprocessing
│   └── data_ingestion.py       # Database operations
├── tests/
│   ├── test_comprehensive.py   # 10 comprehensive tests
│   └── conftest.py             # Test fixtures
├── models/
│   ├── best_model.joblib       # Trained model
│   ├── preprocessor.joblib     # Scaler
│   └── feature_names.joblib    # Feature list
├── .github/workflows/
│   ├── backend.yml             # Backend CI/CD
│   └── frontend.yml            # Frontend CI/CD
└── monitoring/
    ├── prometheus.yml          # Metrics config
    └── grafana_dashboards.json # Dashboard definitions
```

## Performance Metrics

- **Model Accuracy**: 98.89%
- **ROC-AUC**: 97.79%
- **API Response Time**: <100ms
- **Database Query Time**: <50ms
- **Frontend Load Time**: <2s

---

**Next Steps**: See [SETUP.md](SETUP.md) for local development or [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment.
