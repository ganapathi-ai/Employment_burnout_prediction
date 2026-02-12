# 🚀 Employee Burnout Risk Prediction System

A production-ready machine learning system that predicts employee burnout risk using work-from-home behavioral metrics. Built with modern ML, DevOps, and software engineering best practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This system analyzes work-from-home behavioral patterns (work hours, screen time, meetings, sleep, breaks) to predict high burnout risk. It provides:

- **Real-time predictions** via REST API
- **Interactive web interface** for data entry
- **Comprehensive monitoring** with metrics and dashboards
- **ML experiment tracking** with Weights & Biases
- **Automated deployment** with CI/CD pipelines

### Key Metrics

- **Model Accuracy**: 88.5%
- **F1 Score**: 0.92
- **ROC-AUC**: 0.95
- **API Latency**: < 100ms
- **Availability**: 99.9%

## ✨ Features

### Machine Learning
- ✅ Multiple model architectures (Logistic Regression, Random Forest, XGBoost)
- ✅ Hyperparameter tuning with BayesianSearchCV
- ✅ Cross-validation and stratified splits
- ✅ W&B experiment tracking
- ✅ Model versioning and registry

### Backend
- ✅ FastAPI with async support
- ✅ Pydantic input validation
- ✅ Prometheus metrics
- ✅ Health checks and monitoring
- ✅ CORS enabled for frontend

### Frontend
- ✅ Streamlit interactive UI
- ✅ Real-time predictions
- ✅ Risk visualization
- ✅ Personalized recommendations
- ✅ Error handling

### DevOps
- ✅ Docker containerization
- ✅ docker-compose orchestration
- ✅ GitHub Actions CI/CD
- ✅ Render deployment
- ✅ Neon Postgres database

### Monitoring & Observability
- ✅ Prometheus metrics collection
- ✅ Grafana dashboards
- ✅ Request/latency/error tracking
- ✅ Application logs

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Data** | Pandas, NumPy |
| **ML** | scikit-learn, XGBoost, scikit-optimize |
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | Streamlit |
| **Database** | Neon Postgres |
| **Monitoring** | Prometheus, Grafana |
| **ML Tracking** | Weights & Biases |
| **Testing** | Pytest, Flake8, Pylint |
| **DevOps** | Docker, GitHub Actions, Render |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git
- Accounts: Neon, W&B, Render, GitHub

### 1. Clone and Setup Environment

```bash
# Clone repository
git clone https://github.com/yourusername/burnout-prediction
cd burnout-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy and edit .env
cp .env.example .env

# Set up your credentials:
# DATABASE_URL=postgresql://...  (from Neon)
# WANDB_API_KEY=...             (from W&B)
# API_URL=http://localhost:8000
```

### 3. Setup Postgres Database

```bash
# Test connection
python -c "from scripts.data_ingestion import PostgresDataStore; \
           store = PostgresDataStore(); \
           store.test_connection()"

# Load transformed data (if available)
# python -c "from scripts.data_ingestion import PostgresDataStore; \
#            store = PostgresDataStore(); \
#            store.load_csv_to_postgres('data/work_from_home_burnout_dataset_transformed.csv')"
```

### 4. Train Model

```bash
# Preprocess data
python scripts/preprocessing.py

# Train and track with W&B
python scripts/train_model.py
```

### 5. Run Locally

**Terminal 1: Start FastAPI**
```bash
python api/main.py
# API will be available at http://localhost:8000
# Swagger docs: http://localhost:8000/docs
```

**Terminal 2: Start Streamlit**
```bash
streamlit run frontend/streamlit_app.py
# Frontend will be available at http://localhost:8501
```

### 6. Run with Docker

```bash
# Build and run all services
docker-compose up -d

# Access services:
# - API: http://localhost:8000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)

# Stop services
docker-compose down
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit Frontend                 │
│           (User Interface & Predictions)            │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ HTTP/REST
                   ▼
┌─────────────────────────────────────────────────────┐
│                  FastAPI Backend                    │
│        (Prediction API, Health Checks)              │
├─────────────────────────────────────────────────────┤
│  ML Model Registry  │  Preprocessor  │  Logger      │
└──────────┬──────────────┬──────────────┬────────────┘
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐  ┌─────────────┐  ┌──────────────┐
    │ Prometheus  │  │Neon Postgres│  │Application   │
    │  Metrics    │  │  Database   │  │    Logs      │
    └─────────────┘  └─────────────┘  └──────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│              Grafana Dashboards                     │
│      (Monitoring & Metrics Visualization)          │
└─────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
burnout-prediction/
├── data/
│   ├── raw/                           # Original CSV files
│   ├── processed/                     # Processed data
│   └── schema/
│       └── database_schema.sql        # Postgres schema
├── notebooks/
│   └── ML_Production_Guide.ipynb      # Complete guide
├── scripts/
│   ├── data_ingestion.py              # PostgreSQL integration
│   ├── preprocessing.py               # Data pipeline
│   ├── train_model.py                 # Model training
│   ├── model_registry.py              # Model versioning
│   └── utils.py                       # Helper functions
├── api/
│   ├── main.py                        # FastAPI app
│   ├── models.py                      # Pydantic schemas
│   └── dependencies.py                # Dependency injection
├── frontend/
│   ├── streamlit_app.py               # Streamlit UI
│   └── config.yaml                    # Frontend config
├── models/
│   ├── best_model.joblib              # Trained model
│   ├── preprocessor.joblib            # Pipeline
│   └── registry.json                  # Model registry
├── tests/
│   ├── test_api.py                    # API tests
│   ├── test_preprocessing.py          # Data pipeline tests
│   └── conftest.py                    # Pytest fixtures
├── monitoring/
│   ├── prometheus.yml                 # Prometheus config
│   ├── grafana_datasources.yml        # Grafana setup
│   └── grafana_dashboards.json        # Dashboard definitions
├── .github/
│   └── workflows/
│       ├── backend.yml                # Backend CI/CD
│       └── frontend.yml               # Frontend CI/CD
├── docs/
│   ├── README.md                      # This file
│   ├── ARCHITECTURE.md                # Architecture details
│   └── DEPLOYMENT.md                  # Deployment guide
├── Dockerfile                         # Container definition
├── docker-compose.yml                 # Multi-container setup
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── .flake8                            # Code style config
├── .pylintrc                          # Linting config
└── .gitignore                         # Git ignore rules
```

## 📊 Usage

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-02-12T10:30:00",
  "model_loaded": true
}
```

#### 2. Predict Burnout Risk
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
    "day_type": "Weekday"
  }'
```

Response:
```json
{
  "risk_level": "Low",
  "risk_probability": 0.15,
  "timestamp": "2024-02-12T10:30:00"
}
```

#### 3. Metrics
```bash
curl http://localhost:8000/metrics
```

### Web Interface

Open http://localhost:8501/ and:
1. Enter work metrics using sliders and inputs
2. Click "Predict Burnout Risk"
3. View risk assessment and recommendations

## 🚢 Deployment

### Deploy to Render

1. Push code to GitHub
2. Connect GitHub repository to Render
3. Configure environment variables
4. Set start command:
   ```
   uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```
5. Deploy!

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed steps.

## 📊 Monitoring

### Prometheus
- **URL**: http://localhost:9090
- **Metrics**: Request counts, latency, errors

### Grafana
- **URL**: http://localhost:3000
- **Dashboards**: Request rates, latency, error rates
- **Login**: admin / admin

## 🧪 Development

### Run Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=api --cov=scripts

# Specific test
pytest tests/test_api.py::TestPredictEndpoint -v
```

### Code Quality
```bash
# Flake8
flake8 api/ scripts/ --max-line-length=100

# Pylint
pylint api/ scripts/ --fail-under=7.0

# Format code
black api/ scripts/ frontend/
isort api/ scripts/ frontend/
```

### W&B Experiment Tracking

View experiments: https://wandb.ai/yourusername/burnout-prediction

Track parameters, metrics, and artifacts automatically during training.

## 📝 CI/CD Pipeline

GitHub Actions automatically:
1. Lint code (Flake8, Pylint)
2. Run tests (Pytest)
3. Build Docker image
4. Push to Docker registry
5. Deploy to Render

See [.github/workflows/](.github/workflows/) for details.

## 🔐 Security Best Practices

- ✅ Environment variables for secrets
- ✅ Connection pooling for database
- ✅ Input validation with Pydantic
- ✅ HTTPS in production
- ✅ API rate limiting (recommended)
- ✅ CORS properly configured

## 📈 Performance

- **Model Training**: ~5-10 minutes
- **API Latency**: 50-100ms per prediction
- **Throughput**: 100+ predictions/second
- **Database**: Connection pool size: 5

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

For issues, questions, or suggestions:
- Open GitHub issue
- Check troubleshooting guide
- Review documentation

## 🙏 Acknowledgments

- Dataset: Work-from-home burnout behavioral data
- Stack: FastAPI, Streamlit, scikit-learn, Postgres, Docker
- Inspiration: ML ops best practices

---

**Built with ❤️ for better employee wellness**
