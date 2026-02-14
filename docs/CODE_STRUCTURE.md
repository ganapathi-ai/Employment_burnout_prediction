# 📂 Code Structure Guide

Detailed explanation of every file and folder in the project.

## Project Tree

```
Employment_burnout_prediction/
├── api/                          # Backend API
│   └── main.py                   # FastAPI application (400 lines)
├── frontend/                     # Frontend UI
│   └── streamlit_app.py          # Streamlit dashboard (500 lines)
├── scripts/                      # Utility scripts
│   ├── train_model.py            # ML training pipeline
│   ├── train_model_with_tuning.py # Hyperparameter tuning
│   ├── preprocessing.py          # Data preprocessing
│   └── data_ingestion.py         # Database operations
├── tests/                        # Test suite
│   ├── conftest.py               # Test fixtures
│   ├── test_comprehensive.py     # Main tests (10 tests)
│   └── test_api.py               # API tests
├── models/                       # Trained models
│   ├── best_model.joblib         # Random Forest model
│   ├── preprocessor.joblib       # StandardScaler
│   └── feature_names.joblib      # Feature list
├── data/                         # Datasets
│   ├── work_from_home_burnout_dataset.csv
│   ├── work_from_home_burnout_dataset_transformed.csv
│   └── schema/
│       └── database_schema.sql   # PostgreSQL schema
├── monitoring/                   # Monitoring configs
│   ├── prometheus.yml            # Prometheus config
│   ├── grafana_dashboard.json    # Grafana dashboard
│   ├── grafana_datasources.yml   # Data sources
│   └── dashboard_requests.json   # Request metrics
├── .github/                      # GitHub configs
│   └── workflows/
│       ├── backend.yml           # Backend CI/CD
│       └── frontend.yml          # Frontend CI/CD
├── .streamlit/                   # Streamlit config
│   └── config.toml               # UI configuration
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # System design
│   ├── SETUP.md                  # Setup guide
│   ├── API.md                    # API reference
│   ├── DEPLOYMENT.md             # Deployment guide
│   ├── TESTING.md                # Testing guide
│   └── CODE_STRUCTURE.md         # This file
├── notebooks/                    # Jupyter notebooks
│   └── ML_Production_Guide.ipynb # ML guide
├── wandb/                        # W&B experiment logs
│   └── run-*/                    # Training runs
├── .env                          # Environment variables (not in git)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── .pylintrc                     # Pylint configuration
├── .flake8                       # Flake8 configuration
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Multi-container setup
├── docker-compose-monitoring.yml # Monitoring stack
├── render.yaml                   # Render deployment config
├── Procfile                      # Process file for deployment
├── runtime.txt                   # Python version
├── start.sh                      # Startup script
├── check_db_data.py              # Database verification
├── test_api_local.py             # Local API testing
└── README.md                     # Project overview
```

---

## Core Files Explained

### 1. api/main.py (400 lines)

**Purpose**: FastAPI backend with ML inference

**Key Components**:

```python
# Imports and Setup (Lines 1-30)
- FastAPI, Pydantic, SQLAlchemy imports
- Environment variable loading
- Logging configuration

# FastAPI App Initialization (Lines 31-40)
- App creation with metadata
- CORS middleware setup

# Prometheus Metrics (Lines 41-50)
- REQUEST_COUNT, REQUEST_LATENCY
- PREDICTION_COUNT, ACTIVE_REQUESTS
- MODEL_LOADED, DB_OPERATIONS

# Pydantic Models (Lines 51-90)
- UserData: Input validation
- BurnoutPrediction: Response model
- HealthCheck: Health response

# Database Setup (Lines 91-150)
- Engine creation (Neon PostgreSQL)
- Table definition (user_requests)
- Metadata and schema

# Model Loading (Lines 151-220)
- _load_model_sync(): Load model at startup
- Fallback dummy model for development
- Error handling

# Feature Engineering (Lines 221-280)
- engineer_features(): 17 features from 8 inputs
- Work intensity, meeting burden, sleep deficit
- Recovery index, fatigue risk, WLB score

# API Endpoints (Lines 281-400)
- GET /health: Health check
- POST /predict: Burnout prediction
- GET /db-status: Database status
- GET /: API info
- GET /metrics: Prometheus metrics
```

**Key Functions**:

1. **engineer_features(data: UserData)**
   - Input: UserData object
   - Output: (features_array, all_features_dict)
   - Purpose: Transform 8 inputs into 17 features

2. **predict(user_data: UserData)**
   - Input: User work metrics
   - Output: BurnoutPrediction
   - Purpose: ML inference and database logging

3. **health_check()**
   - Output: HealthCheck
   - Purpose: API health monitoring

**Database Operations**:
- Stores every prediction request
- Logs all 23 features (8 input + 15 derived)
- Tracks user_id, name, timestamp

---

### 2. frontend/streamlit_app.py (500 lines)

**Purpose**: Interactive web dashboard

**Structure**:

```python
# Configuration (Lines 1-50)
- Page config, custom CSS
- API URL configuration
- Health check on startup

# Sidebar (Lines 51-80)
- System info display
- How to use guide
- Risk level legend

# Tab 1: Input Data (Lines 81-350)
- Input sliders for 8 metrics
- Real-time derived metrics calculation
- Prediction button and results display
- Visualizations (gauge, bar charts)
- Personalized recommendations

# Tab 2: Analytics (Lines 351-450)
- Dataset statistics
- Burnout distribution
- Feature correlations
- Heatmaps

# Tab 3: About (Lines 451-500)
- System information
- ML model details
- Privacy policy
```

**Key Features**:

1. **Input Form**
   - 8 sliders for user metrics
   - Real-time validation
   - Name/User ID tracking

2. **Derived Metrics Display**
   - 16 calculated metrics shown in table
   - Color-coded indicators
   - Comparison with recommended values

3. **Results Visualization**
   - Risk score gauge
   - Risk factors bar chart
   - Recommendations list
   - Health metrics comparison

4. **Analytics Dashboard**
   - Dataset insights
   - Correlation heatmap
   - Average metrics by risk level

---

### 3. scripts/train_model.py (250 lines)

**Purpose**: ML model training pipeline

**Workflow**:

```python
# 1. Data Loading (Lines 1-50)
- Load CSV dataset
- Display dataset info
- Log to W&B

# 2. Feature Engineering (Lines 51-100)
- Apply engineer_features()
- Create binary target (High=1, Low=0)
- Select 17 features

# 3. Train/Test Split (Lines 101-120)
- 80/20 split
- Stratified sampling
- Feature scaling

# 4. Model Training (Lines 121-200)
- Train 3 models: RF, GB, XGB
- Evaluate each model
- Select best based on ROC-AUC

# 5. Model Saving (Lines 201-250)
- Save best model
- Save scaler
- Save feature names
- Log to W&B
```

**Models Trained**:
1. Random Forest (n_estimators=100, max_depth=10)
2. Gradient Boosting (n_estimators=100, max_depth=5)
3. XGBoost (n_estimators=100, max_depth=5)

**Output Files**:
- `models/best_model.joblib`
- `models/preprocessor.joblib`
- `models/feature_names.joblib`

---

### 4. scripts/preprocessing.py

**Purpose**: Data preprocessing utilities

**Functions**:

1. **load_data(path)**
   - Load CSV dataset
   - Handle missing values
   - Return DataFrame

2. **clean_data(df)**
   - Remove duplicates
   - Handle outliers
   - Normalize values

3. **transform_features(df)**
   - Apply feature engineering
   - Encode categorical variables
   - Scale numerical features

---

### 5. scripts/data_ingestion.py

**Purpose**: Database operations

**Functions**:

1. **create_tables()**
   - Create user_requests table
   - Define schema
   - Add indexes

2. **insert_data(data)**
   - Insert prediction records
   - Handle errors
   - Return success status

3. **query_data(filters)**
   - Query predictions
   - Apply filters
   - Return results

---

### 6. tests/test_comprehensive.py (200 lines)

**Purpose**: Comprehensive test suite

**Test Categories**:

1. **API Tests** (Lines 1-80)
   - test_health_check()
   - test_predict_endpoint()
   - test_metrics_endpoint()

2. **Validation Tests** (Lines 81-120)
   - test_predict_validation()
   - test_invalid_input()
   - test_missing_fields()

3. **Feature Tests** (Lines 121-160)
   - test_feature_engineering()
   - test_model_loading()

4. **Integration Tests** (Lines 161-200)
   - test_database_connection()
   - test_edge_cases()

---

## Configuration Files

### .env.example

**Purpose**: Environment variable template

**Variables**:
```env
# Database
DATABASE_URL=postgresql://...
PGHOST, PGDATABASE, PGUSER, PGPASSWORD

# ML Tracking
WANDB_API_KEY, WANDB_ENTITY

# Model Paths
MODEL_PATH, PREPROCESSOR_PATH

# API Config
API_HOST, API_PORT, API_LOG_LEVEL

# Frontend Config
STREAMLIT_SERVER_PORT, API_URL

# Environment
ENVIRONMENT, DEBUG
```

### requirements.txt

**Purpose**: Python dependencies

**Categories**:
1. **Data Science**: pandas, numpy, scikit-learn, xgboost
2. **Web**: fastapi, uvicorn, streamlit
3. **Database**: sqlalchemy, psycopg2-binary
4. **ML Ops**: wandb, prometheus-client
5. **Testing**: pytest, pytest-cov, httpx
6. **Quality**: pylint, flake8, black

### Dockerfile

**Purpose**: Container image definition

**Stages**:
```dockerfile
# Base image: Python 3.9
# Install dependencies
# Copy application code
# Expose port 8000
# Run uvicorn server
```

### docker-compose.yml

**Purpose**: Multi-container orchestration

**Services**:
1. **api**: Backend service (port 8000)
2. **prometheus**: Metrics collection (port 9090)
3. **grafana**: Visualization (port 3000)

### render.yaml

**Purpose**: Render deployment configuration

**Services**:
1. **burnout-api**: Backend web service
2. **burnout-frontend**: Frontend web service

---

## Data Files

### data/work_from_home_burnout_dataset.csv

**Columns**:
- work_hours, screen_time_hours, meetings_count
- breaks_taken, after_hours_work, sleep_hours
- task_completion_rate, day_type
- burnout_risk, burnout_score

**Size**: 22,750 rows

### data/work_from_home_burnout_dataset_transformed.csv

**Purpose**: Preprocessed dataset with engineered features

**Additional Columns**:
- work_intensity_ratio, meeting_burden
- break_adequacy, sleep_deficit
- recovery_index, fatigue_risk
- workload_pressure, task_efficiency
- work_life_balance_score

---

## Model Files

### models/best_model.joblib

**Type**: Random Forest Classifier
**Size**: ~50 MB
**Features**: 17 input features
**Performance**: 98.89% accuracy, 97.79% ROC-AUC

### models/preprocessor.joblib

**Type**: StandardScaler
**Purpose**: Feature normalization
**Fitted on**: Training data (80% of dataset)

### models/feature_names.joblib

**Type**: List of strings
**Content**: 17 feature names in order
**Purpose**: Ensure correct feature order

---

## Monitoring Files

### monitoring/prometheus.yml

**Purpose**: Prometheus configuration

**Scrape Configs**:
```yaml
scrape_configs:
  - job_name: 'burnout-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### monitoring/grafana_dashboard.json

**Purpose**: Grafana dashboard definition

**Panels**:
1. API Request Rate
2. Request Latency (p50, p95, p99)
3. Prediction Count by Risk Level
4. Active Requests
5. Database Operations

---

## CI/CD Files

### .github/workflows/backend.yml

**Purpose**: Backend CI/CD pipeline

**Jobs**:
1. **test**: Run tests, linting
2. **deploy**: Deploy to Render (on main branch)

**Triggers**: Push to main, pull requests

### .github/workflows/frontend.yml

**Purpose**: Frontend CI/CD pipeline

**Jobs**:
1. **test**: Validate Streamlit app
2. **deploy**: Deploy to Render

---

## Helper Scripts

### check_db_data.py

**Purpose**: Verify database connection and data

**Usage**:
```bash
python check_db_data.py
```

**Output**: Connection status, row count, sample data

### test_api_local.py

**Purpose**: Quick local API testing

**Usage**:
```bash
python test_api_local.py
```

**Tests**: Health check, prediction endpoint

---

## File Relationships

```
train_model.py
    ↓ (trains)
best_model.joblib, preprocessor.joblib
    ↓ (loaded by)
api/main.py
    ↓ (called by)
frontend/streamlit_app.py
    ↓ (displays to)
User Browser
```

---

## Code Metrics

| File | Lines | Functions | Classes | Complexity |
|------|-------|-----------|---------|------------|
| api/main.py | 400 | 8 | 3 | Medium |
| frontend/streamlit_app.py | 500 | 0 | 0 | Low |
| scripts/train_model.py | 250 | 2 | 0 | Medium |
| tests/test_comprehensive.py | 200 | 10 | 0 | Low |

---

## Import Dependencies

### api/main.py imports:
- fastapi, pydantic, uvicorn
- sqlalchemy, psycopg2
- joblib, numpy, pandas
- prometheus_client
- python-dotenv

### frontend/streamlit_app.py imports:
- streamlit
- requests
- pandas, numpy

### scripts/train_model.py imports:
- pandas, numpy
- scikit-learn
- xgboost
- wandb
- joblib

---

## Key Design Patterns

1. **Dependency Injection**: FastAPI endpoints
2. **Factory Pattern**: Model loading
3. **Repository Pattern**: Database operations
4. **Observer Pattern**: Prometheus metrics
5. **Strategy Pattern**: Multiple ML models

---

## Code Style

- **Linting**: Pylint (10/10 score)
- **Formatting**: Black, isort
- **Docstrings**: Google style
- **Type Hints**: Pydantic models
- **Line Length**: 120 characters max

---

## Next Steps for Developers

1. **Read**: Start with README.md
2. **Setup**: Follow SETUP.md
3. **Understand**: Read ARCHITECTURE.md
4. **Code**: Explore api/main.py
5. **Test**: Run tests in tests/
6. **Deploy**: Follow DEPLOYMENT.md
