# 🧠 Employee Burnout Prediction System

An advanced ML-powered system that predicts employee burnout risk using work-from-home behavioral metrics. Built with production-ready MLOps practices, comprehensive testing, and automated CI/CD.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code Quality](https://img.shields.io/badge/pylint-10.00/10-brightgreen.svg)](https://www.pylint.org/)
[![Tests](https://img.shields.io/badge/tests-10/10%20passing-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📚 Complete Documentation

| Document | Description |
|----------|-------------|
| **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** | System design, components, data flow, tech stack |
| **[SETUP.md](docs/SETUP.md)** | Step-by-step local development setup |
| **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** | Production deployment guide (Render, AWS, GCP) |
| **[API.md](docs/API.md)** | Complete API reference with examples |
| **[TESTING.md](docs/TESTING.md)** | Testing guide and best practices |
| **[CODE_STRUCTURE.md](docs/CODE_STRUCTURE.md)** | Detailed code organization and file explanations |
| **[ML_MODEL.md](docs/ML_MODEL.md)** | ML model details, training, and feature engineering |
| **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** | How to contribute to the project |
| **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** | Common issues and solutions |

## 🎯 Quick Links

- 🚀 **[Get Started in 5 Minutes](#-quick-start)**
- 🏗️ **[Understand the Architecture](docs/ARCHITECTURE.md)**
- 📡 **[API Documentation](docs/API.md)**
- 🧪 **[Run Tests](docs/TESTING.md)**
- 🚢 **[Deploy to Production](docs/DEPLOYMENT.md)**

## ✨ Key Features

- **Real-time Predictions**: ML model with 17 engineered features
- **Interactive Dashboard**: Gauge charts, bar charts, heatmaps
- **Personalized Insights**: Custom recommendations based on metrics
- **Analytics**: Dataset insights and correlations
- **REST API**: FastAPI backend with health monitoring
- **CI/CD**: Automated deployment with GitHub Actions
- **ML Tracking**: Live experiment tracking with Weights & Biases

## 🛠️ Technology Stack

- **Backend**: FastAPI, scikit-learn, XGBoost, PostgreSQL
- **Frontend**: Streamlit
- **Deployment**: Render (Free tier)
- **CI/CD**: GitHub Actions, Docker Hub
- **ML Tracking**: Weights & Biases

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- Neon account (free Postgres)
- W&B account (optional)

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/ganapathi-ai/Employment_burnout_prediction.git
cd Employment_burnout_prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your DATABASE_URL and WANDB_API_KEY

# 4. Train model
python scripts/train_model.py

# 5. Run backend (Terminal 1)
python api/main.py

# 6. Run frontend (Terminal 2)
streamlit run frontend/streamlit_app.py
```

**Access**:
- 🌐 Frontend: http://localhost:8501
- 🔌 API: http://localhost:8000
- 📖 API Docs: http://localhost:8000/docs

**Need help?** See [SETUP.md](docs/SETUP.md) for detailed instructions.

## 📊 System Architecture

```
┌─────────────┐
│    USER     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Streamlit Frontend │ (Port 8501)
│  • Input Forms      │
│  • Visualizations   │
│  • Recommendations  │
└──────┬──────────────┘
       │ HTTP POST
       ▼
┌─────────────────────┐
│   FastAPI Backend   │ (Port 8000)
│  • Validation       │
│  • Feature Eng.     │
│  • ML Inference     │
└──┬────┬────┬────────┘
   │    │    │
   ▼    ▼    ▼
┌────┐┌────┐┌────┐
│ ML ││ DB ││Prom│
└────┘└────┘└────┘
```

**See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.**

## 🧠 Machine Learning Model

**Model Performance**:
- Accuracy: 98.89%
- ROC-AUC: 97.79%
- Inference Time: <50ms

**Feature Engineering**: 17 features from 8 inputs

**Input Features (8)**:
1. Work hours
2. Screen time
3. Meetings count
4. Breaks taken
5. After-hours work
6. Sleep hours
7. Task completion rate
8. Day type

**Engineered Features (9)**:
1. Work intensity ratio
2. Meeting burden
3. Break adequacy
4. Sleep deficit
5. Recovery index
6. Fatigue risk
7. Workload pressure
8. Task efficiency
9. Work-life balance score

**Models Evaluated**:
- ✅ Random Forest (Best: 98.89% accuracy)
- Gradient Boosting
- XGBoost

Selection based on ROC-AUC score with W&B tracking.

## 📱 Dashboard Features

### Input Tab
- Interactive sliders for all metrics
- Real-time metric calculations
- Quick insights display

### Results
- Gauge chart for risk score
- Bar chart for risk factors
- Personalized recommendations
- Comparison with recommended values

### Analytics Tab
- Burnout risk distribution
- Average metrics by risk level
- Correlation heatmap
- Dataset statistics

## 🔒 Security & Quality

**Security**:
- ✅ Environment variables for all credentials
- ✅ No hardcoded secrets
- ✅ CORS configured
- ✅ Input validation (Pydantic)
- ✅ Secure database connections

**Code Quality**:
- ✅ Pylint: 10.00/10
- ✅ Tests: 10/10 passing
- ✅ Coverage: 85%+
- ✅ PEP 8 compliant

## 🧪 Testing & CI/CD

**Testing**:
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=api --cov-report=html

# Code quality
pylint api/ --fail-under=7.0
```

**CI/CD Pipeline**:
- ✅ Automated testing on push
- ✅ Code quality checks (Pylint, Flake8)
- ✅ Docker build and push
- ✅ Auto-deployment to Render

**See [TESTING.md](docs/TESTING.md) for comprehensive testing guide.**

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/predict` | POST | Burnout prediction |
| `/metrics` | GET | Prometheus metrics |
| `/docs` | GET | Interactive API docs |

**Example Request**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "work_hours": 8,
    "screen_time_hours": 6,
    "meetings_count": 3,
    "breaks_taken": 4,
    "after_hours_work": 0,
    "sleep_hours": 7.5,
    "task_completion_rate": 85,
    "day_type": "Weekday",
    "name": "Test User",
    "user_id": "test123"
  }'
```

**See [API.md](docs/API.md) for complete API documentation.**

## 📁 Project Structure

```
Employment_burnout_prediction/
├── api/
│   └── main.py              # FastAPI backend (400 lines)
├── frontend/
│   └── streamlit_app.py     # Streamlit UI (500 lines)
├── scripts/
│   ├── train_model.py       # ML training pipeline
│   ├── preprocessing.py     # Data preprocessing
│   └── data_ingestion.py    # Database operations
├── tests/
│   ├── test_comprehensive.py # 10 comprehensive tests
│   └── conftest.py          # Test fixtures
├── models/
│   ├── best_model.joblib    # Trained model
│   ├── preprocessor.joblib  # Scaler
│   └── feature_names.joblib # Feature list
├── data/
│   └── work_from_home_burnout_dataset.csv
├── .github/workflows/
│   ├── backend.yml          # Backend CI/CD
│   └── frontend.yml         # Frontend CI/CD
├── monitoring/
│   ├── prometheus.yml       # Metrics config
│   └── grafana_dashboards.json
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # System design
│   ├── SETUP.md             # Setup guide
│   ├── DEPLOYMENT.md        # Deployment guide
│   ├── API.md               # API documentation
│   ├── TESTING.md           # Testing guide
│   ├── CODE_STRUCTURE.md    # Code organization
│   ├── ML_MODEL.md          # ML model details
│   ├── CONTRIBUTING.md      # Contribution guidelines
│   └── TROUBLESHOOTING.md   # Common issues
├── requirements.txt         # Dependencies
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-container setup
└── render.yaml              # Render configuration
```

## 🚀 Deployment

**Supported Platforms**:
- ✅ Render (Recommended - Free tier)
- ✅ AWS (EC2, ECS, Lambda)
- ✅ Google Cloud (Cloud Run)
- ✅ Azure (App Service)

**Quick Deploy to Render**:
1. Fork this repository
2. Create Render account
3. Connect repository
4. Add environment variables
5. Deploy!

**See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for step-by-step guide.**

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

**Quick Start**:
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Make changes and add tests
4. Commit: `git commit -m 'feat: add amazing feature'`
5. Push: `git push origin feature/amazing`
6. Open Pull Request

## 📊 Performance Metrics

- **Model Accuracy**: 98.89%
- **ROC-AUC**: 97.79%
- **API Response Time**: <100ms
- **Database Query Time**: <50ms
- **Test Coverage**: 85%+
- **Code Quality**: 10/10 (Pylint)

## 🔗 Resources

- **Live Demo**: Coming soon
- **API Docs**: http://localhost:8000/docs (local)
- **W&B Dashboard**: https://wandb.ai/kakarlagana18-iihmr
- **GitHub Actions**: [View Workflows](.github/workflows/)
- **Issues**: [Report Bug](https://github.com/ganapathi-ai/Employment_burnout_prediction/issues)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset: Work From Home Burnout Dataset
- ML Framework: scikit-learn, Random Forest
- Web Frameworks: FastAPI, Streamlit
- Deployment: Render, Neon
- ML Tracking: Weights & Biases
