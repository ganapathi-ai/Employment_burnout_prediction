# 🏗️ System Architecture

## Overview

The Employee Burnout Prediction System is a full-stack ML application with a microservices architecture, featuring real-time predictions, monitoring, and automated CI/CD.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                               │
│                    (Browser / API Client)                        │
└────────────┬────────────────────────────────┬───────────────────┘
             │                                │
             ▼                                ▼
┌────────────────────────┐      ┌────────────────────────┐
│  STREAMLIT FRONTEND    │      │   EXTERNAL API         │
│  Port: 8501            │      │   CLIENTS              │
│  • Input Forms         │      │   • curl/Postman       │
│  • Visualizations      │      │   • Mobile Apps        │
│  • Analytics Dashboard │      │   • Third-party        │
└────────────┬───────────┘      └────────────┬───────────┘
             │                                │
             │         HTTP POST /predict     │
             └────────────────┬───────────────┘
                              ▼
             ┌────────────────────────────────┐
             │     FASTAPI BACKEND            │
             │     Port: 8000                 │
             │  ┌──────────────────────────┐  │
             │  │  API Layer               │  │
             │  │  • /predict              │  │
             │  │  • /health               │  │
             │  │  • /metrics              │  │
             │  └──────────┬───────────────┘  │
             │             ▼                   │
             │  ┌──────────────────────────┐  │
             │  │  Business Logic          │  │
             │  │  • Input Validation      │  │
             │  │  • Feature Engineering   │  │
             │  │  • ML Inference          │  │
             │  └──────────┬───────────────┘  │
             └─────────────┼───────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌──────────────┐  ┌──────────────┐
│  ML MODELS    │  │  DATABASE    │  │  MONITORING  │
│               │  │              │  │              │
│ • RF Model    │  │ PostgreSQL   │  │ Prometheus   │
│ • Scaler      │  │ (Neon)       │  │ Grafana      │
│ • Features    │  │              │  │ W&B          │
└───────────────┘  └──────────────┘  └──────────────┘
```

## System Components

### 1. Frontend Layer (Streamlit)

**File**: `frontend/streamlit_app.py` (500 lines)

**Responsibilities**:
- User interface for data input
- Real-time metric calculations
- Interactive visualizations (gauge charts, bar charts, heatmaps)
- Personalized recommendations display
- Analytics dashboard

**Key Features**:
- 3 tabs: Input Data, Analytics, About
- Real-time derived metrics calculation
- API health check on startup
- Responsive design with custom CSS

**Technology**: Streamlit 1.28+, Pandas, NumPy, Requests

### 2. Backend Layer (FastAPI)

**File**: `api/main.py` (400 lines)

**Responsibilities**:
- RESTful API endpoints
- Input validation (Pydantic)
- Feature engineering (17 features)
- ML model inference
- Database operations
- Prometheus metrics export

**Endpoints**:
- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Burnout prediction
- `GET /metrics` - Prometheus metrics
- `GET /docs` - Interactive API docs
- `GET /db-status` - Database status

**Technology**: FastAPI 0.100+, Pydantic, SQLAlchemy, Prometheus Client

### 3. Machine Learning Layer

**Files**:
- `models/best_model.joblib` - Trained Random Forest model
- `models/preprocessor.joblib` - StandardScaler
- `models/feature_names.joblib` - Feature list

**Training Script**: `scripts/train_model.py`

**Model Details**:
- Algorithm: Random Forest Classifier (selected from 3 models)
- Features: 17 (8 input + 9 engineered)
- Accuracy: 98.89%
- ROC-AUC: 97.79%
- Training: W&B experiment tracking

**Feature Engineering**:
```python
# Work Intensity Metrics
work_intensity_ratio = screen_time / (work_hours + 0.1)
meeting_burden = meetings / (work_hours + 0.1)
break_adequacy = breaks / (work_hours + 0.1)

# Health Metrics
sleep_deficit = 8 - sleep_hours
recovery_index = (sleep_hours + breaks) - screen_time
fatigue_risk = screen_time - (sleep_hours * 1.5)

# Workload Metrics
workload_pressure = work_hours + (meetings * 0.25) + after_hours
task_efficiency = task_completion_rate / (work_hours + 0.1)

# Balance Score
work_life_balance_score = ((sleep/8)*30 + (breaks/5)*30 - (work/10)*20 - after_hours*10)*2
```

### 4. Database Layer

**Technology**: PostgreSQL (Neon - Serverless)

**Schema**: `data/schema/database_schema.sql`

**Table**: `user_requests`

**Columns**:
- `id` (Primary Key)
- `user_id`, `name` (Tracking)
- `created_at` (Timestamp)
- 8 input features
- 15 engineered features

**Purpose**:
- Store all prediction requests
- Enable analytics and reporting
- Track user patterns
- Audit trail

### 5. Monitoring Layer

**Components**:
- **Prometheus**: Metrics collection (Port 9090)
- **Grafana**: Visualization dashboards (Port 3000)
- **W&B**: ML experiment tracking

**Metrics Tracked**:
- API request count (by endpoint, status)
- Request latency (histogram)
- Prediction count (by risk level)
- Active requests (gauge)
- Model loaded status
- Database operations

**Configuration**:
- `monitoring/prometheus.yml`
- `monitoring/grafana_dashboard.json`
- `monitoring/grafana_datasources.yml`

### 6. CI/CD Pipeline

**GitHub Actions Workflows**:
- `.github/workflows/backend.yml` - Backend testing & deployment
- `.github/workflows/frontend.yml` - Frontend deployment

**Pipeline Steps**:
1. Code checkout
2. Python setup
3. Dependency installation
4. Linting (Pylint, Flake8)
5. Testing (Pytest)
6. Docker build & push
7. Deployment to Render

## Data Flow

### Prediction Request Flow

```
1. User Input (Frontend)
   ↓
2. Form Validation (Streamlit)
   ↓
3. HTTP POST to /predict (API)
   ↓
4. Pydantic Validation (Backend)
   ↓
5. Feature Engineering (17 features)
   ↓
6. Feature Scaling (StandardScaler)
   ↓
7. Model Prediction (Random Forest)
   ↓
8. Database Storage (PostgreSQL)
   ↓
9. Metrics Export (Prometheus)
   ↓
10. Response to Frontend (JSON)
   ↓
11. Visualization & Recommendations (Streamlit)
```

### Training Pipeline Flow

```
1. Load Dataset (CSV)
   ↓
2. Feature Engineering
   ↓
3. Train/Test Split (80/20)
   ↓
4. Feature Scaling
   ↓
5. Train 3 Models (RF, GB, XGB)
   ↓
6. Model Evaluation (ROC-AUC)
   ↓
7. Select Best Model
   ↓
8. Save Model & Scaler
   ↓
9. Log to W&B
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.100+
- **ML**: scikit-learn 1.3+, XGBoost 2.0+
- **Database**: PostgreSQL (Neon), SQLAlchemy 2.0+
- **Validation**: Pydantic 2.0+
- **Server**: Uvicorn 0.23+

### Frontend
- **Framework**: Streamlit 1.28+
- **Data**: Pandas 2.0+, NumPy 1.24+
- **HTTP**: Requests 2.31+

### ML & Data Science
- **Training**: scikit-learn, XGBoost, Gradient Boosting
- **Tracking**: Weights & Biases (W&B)
- **Optimization**: scikit-optimize

### Monitoring
- **Metrics**: Prometheus Client 0.17+
- **Visualization**: Grafana
- **Logging**: Python logging, Loguru

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Deployment**: Render (Free tier)

### Testing & Quality
- **Testing**: Pytest 7.4+, pytest-cov
- **Linting**: Pylint 3.0+, Flake8 6.1+
- **Formatting**: Black 23.10+, isort 5.12+

## Security Architecture

### Environment Variables
All sensitive data stored in `.env`:
- `DATABASE_URL` - PostgreSQL connection
- `WANDB_API_KEY` - W&B authentication
- `PGHOST`, `PGUSER`, `PGPASSWORD` - Database credentials

### API Security
- CORS middleware configured
- Input validation (Pydantic)
- No hardcoded secrets
- Secure database connections (SSL)

### Database Security
- SSL/TLS encryption (Neon)
- Connection pooling
- Prepared statements (SQLAlchemy)

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Load balancer ready

### Vertical Scaling
- Efficient feature engineering
- Model inference <50ms
- Database query optimization

### Caching Strategy
- Model loaded once at startup
- Median values cached
- Static assets cached

## Deployment Architecture

### Development
```
Local Machine
├── Backend: localhost:8000
├── Frontend: localhost:8501
├── Database: Neon (cloud)
└── Monitoring: localhost:9090, localhost:3000
```

### Production (Render)
```
Render Platform
├── Backend Service (Web)
│   ├── Auto-scaling
│   ├── Health checks
│   └── Environment variables
├── Frontend Service (Web)
│   ├── Auto-scaling
│   └── API URL from backend
└── Database: Neon (external)
```

## Performance Metrics

- **API Response Time**: <100ms (avg)
- **Model Inference**: <50ms
- **Database Query**: <50ms
- **Frontend Load**: <2s
- **Uptime**: 99.9% (target)

## Future Enhancements

1. **Authentication**: JWT-based user authentication
2. **Caching**: Redis for prediction caching
3. **Batch Predictions**: Bulk prediction endpoint
4. **Model Versioning**: A/B testing framework
5. **Real-time Monitoring**: WebSocket for live updates
6. **Mobile App**: React Native frontend
7. **Advanced Analytics**: Time-series analysis
8. **Auto-retraining**: Scheduled model updates
