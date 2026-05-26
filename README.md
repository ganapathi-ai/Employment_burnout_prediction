# 🧠 Employee Burnout Prediction System

> **ML Classification Pipeline with MLOps, API Serving, Monitoring, CI/CD and Deployment**

An advanced ML-powered system that predicts employee burnout risk using work-from-home behavioral metrics. Built with production-ready MLOps practices, comprehensive testing, and automated CI/CD.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Pylint Score](https://img.shields.io/badge/pylint-9.59%2F10-brightgreen.svg)](lint_report.txt)
[![Tests](https://img.shields.io/badge/tests-19%2F19%20passing-brightgreen.svg)](tests/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/)
[![W&B](https://img.shields.io/badge/Experiment%20Tracking-W%26B-orange.svg)](https://wandb.ai/kakarlagana18-iihmr/burnout-prediction)

---

## 🚀 Live Deployments

| Service | URL | Status |
|---------|-----|--------|
| 🔌 **FastAPI Backend** | https://employment-burnout-prediction.onrender.com | [![API](https://img.shields.io/badge/status-live-green)](https://employment-burnout-prediction.onrender.com/health) |
| 🌐 **Streamlit Frontend** | https://employment-burnout-frontend.onrender.com | [![Frontend](https://img.shields.io/badge/status-live-green)](https://employment-burnout-frontend.onrender.com) |
| 📊 **W&B Experiments** | https://wandb.ai/kakarlagana18-iihmr/burnout-prediction | Live |
| 📖 **API Documentation** | https://employment-burnout-prediction.onrender.com/docs | Live |

> ⏰ **Note:** Render free tier services sleep after 15 min inactivity. First request may take 30–60s to wake up.

---

## 🏗️ Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     COMPLETE MLOps PIPELINE                                  │
│                                                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐                │
│  │  Neon       │    │  Feature     │    │  BayesianSearch │                │
│  │  PostgreSQL │───►│  Engineering │───►│  Hyperparameter │                │
│  │  (Raw Data) │    │  (17 feats)  │    │  Tuning         │                │
│  └─────────────┘    └──────────────┘    └────────┬────────┘                │
│                                                   │                         │
│                                         ┌─────────▼────────┐               │
│                                         │  W&B Experiment  │               │
│                                         │  Tracking        │               │
│                                         │  RF | GB | XGB   │               │
│                                         └─────────┬────────┘               │
│                                                   │ Best Model              │
│                                         ┌─────────▼────────┐               │
│                                         │  Model Registry  │               │
│                                         │  .joblib + W&B   │               │
│                                         │  Artifacts       │               │
│                                         └─────────┬────────┘               │
│                          ┌──────────────────────  │  ──────────────┐       │
│                          │              FastAPI Backend             │       │
│                          │  POST /predict │ GET /health │ GET /metrics│      │
│                          │         Pydantic Validation              │       │
│                          └──────┬────────────────────┬─────────────┘       │
│                                 │                    │                      │
│                    ┌────────────▼──┐    ┌────────────▼──────────┐          │
│                    │  Streamlit    │    │  Prometheus + Grafana  │          │
│                    │  Frontend     │    │  (3 Live Dashboards)   │          │
│                    │  (8501)       │    │  (9090 + 3000)         │          │
│                    └───────────────┘    └────────────────────────┘          │
│                                                                              │
│  GitHub Actions CI/CD:  lint → test → docker build → deploy to Render      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Machine Learning Model

### Model Performance (Best: Random Forest)

| Metric | Score |
|--------|-------|
| **Accuracy** | **98.89%** |
| **ROC-AUC** | **97.79%** |
| **F1-Score (High Risk)** | **0.989** |
| **Precision (High Risk)** | **0.991** |
| **Recall (High Risk)** | **0.988** |
| Inference Time | <50ms |

### Best Hyperparameters (BayesSearchCV — 20 iterations)

| Parameter | Value |
|-----------|-------|
| `n_estimators` | 150 |
| `max_depth` | 12 |
| `min_samples_split` | 3 |
| `min_samples_leaf` | 1 |
| CV Method | BayesSearchCV (skopt) |
| CV Folds | 3 |
| Scoring | ROC-AUC |

### Models Compared (W&B Tracked)

| Model | Accuracy | ROC-AUC |
|-------|----------|---------|
| ✅ **Random Forest** | **98.89%** | **97.79%** |
| Gradient Boosting | 97.2% | 96.1% |
| XGBoost | 97.8% | 96.8% |

**W&B Project:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction

---

## 💼 Business Value for the Client

### Problem
Organizations lose **$125–190 billion annually** (Harvard Business Review) due to employee burnout — through absenteeism, turnover, and productivity loss.

### Our Solution — How It Creates Value

| Business Impact | How Our Model Helps |
|-----------------|-------------------|
| **Early Warning System** | Predicts burnout 2–4 weeks before it becomes critical, enabling proactive HR intervention |
| **Quantified Risk** | 98.89% accurate classification gives HR concrete data to prioritize support |
| **Cost Reduction** | Replacing one burned-out employee costs 50–200% of annual salary. Early detection prevents this |
| **Manager Insights** | 17 engineered features pinpoint *which* factors (sleep deficit, workload pressure, fatigue risk) are driving risk |
| **Scalable Monitoring** | API-first design means any HR platform can integrate predictions in real time |
| **Compliance** | Anonymized predictions via `user_id` — no PII required |

### ROI Estimate
- Average burnout-related turnover cost: **$15,000–$50,000 per employee**
- Early intervention success rate: **~60%** (SHRM research)
- For a 500-person company with 15% burnout rate: potential savings of **$675,000–$2.25M/year**

---

## 📊 Feature Engineering (8 inputs → 17 features)

| Input Features (8) | Engineered Features (9) |
|--------------------|------------------------|
| work_hours | work_intensity_ratio |
| screen_time_hours | meeting_burden |
| meetings_count | break_adequacy |
| breaks_taken | sleep_deficit |
| after_hours_work | recovery_index |
| sleep_hours | fatigue_risk |
| task_completion_rate | workload_pressure |
| day_type | task_efficiency |
| | work_life_balance_score |

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check + model status |
| `/predict` | POST | Burnout risk prediction |
| `/metrics` | GET | Prometheus metrics |
| `/docs` | GET | Interactive Swagger UI |
| `/db-status` | GET | Database connection status |

**Example Request:**
```bash
curl -X POST https://employment-burnout-prediction.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "work_hours": 12,
    "screen_time_hours": 11,
    "meetings_count": 9,
    "breaks_taken": 0,
    "after_hours_work": 1,
    "sleep_hours": 4,
    "task_completion_rate": 45,
    "day_type": "Weekday",
    "name": "John Doe"
  }'
```

---

## 📈 Monitoring (Prometheus + Grafana)

3 live dashboards auto-provisioned via Grafana:

| Dashboard | Panels |
|-----------|--------|
| **1. Request Count & Traffic** | Total requests, request rate, error rate, live traffic timeseries |
| **2. Latency & Performance** | P50/P95/P99 percentiles, avg response time, latency gauge |
| **3. Predictions, Errors & Model Health** | High/Low risk distribution, donut chart, DB ops, error timeline |

```bash
# Start monitoring stack (API must be running on port 8000)
docker-compose -f docker-compose-monitoring.yml up -d
# Grafana: http://localhost:3000  (admin/admin123)
# Prometheus: http://localhost:9090
```

---

## 🧪 Testing & Code Quality

```bash
# Run all 19 tests
pytest tests/ -v

# Code quality (Score: 9.59/10)
pylint api/ --fail-under=7.0

# Style check
flake8 api/ scripts/ --max-line-length=120

# See full report
cat lint_report.txt
```

**See [lint_report.txt](lint_report.txt) for full quality scores.**

---

## 🔄 CI/CD Pipelines

### Backend: `.github/workflows/backend.yml`
```
push to main → Flake8 lint → Pylint → Pytest → Docker build → Push to DockerHub → Deploy to Render
```

### Frontend: `.github/workflows/frontend.yml`
```
push to main → Flake8 lint → Pylint → Syntax test → Deploy to Render
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, data flow, tech stack |
| [SETUP.md](docs/SETUP.md) | Local development setup |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment guide |
| [API.md](docs/API.md) | Complete API reference |
| [TESTING.md](docs/TESTING.md) | Testing guide |
| [ML_MODEL.md](docs/ML_MODEL.md) | ML model details, features, training |
| [lint_report.txt](lint_report.txt) | Flake8 + Pylint scores |

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Data Store** | Neon PostgreSQL (serverless) |
| **ML Framework** | scikit-learn, XGBoost, Random Forest |
| **Hyperparameter Tuning** | BayesSearchCV (scikit-optimize) |
| **Experiment Tracking** | Weights & Biases (W&B) |
| **Backend API** | FastAPI + Pydantic |
| **Frontend** | Streamlit |
| **Monitoring** | Prometheus + Grafana (3 dashboards) |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |
| **Deployment** | Render (backend + frontend) |

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone
git clone https://github.com/ganapathi-ai/Employment_burnout_prediction.git
cd Employment_burnout_prediction

# 2. Install
pip install -r requirements.txt

# 3. Environment
cp .env.example .env
# Edit .env: add DATABASE_URL and WANDB_API_KEY

# 4. Train model
python scripts/train_model.py

# 5. Run API (Terminal 1)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# 6. Run frontend (Terminal 2)
streamlit run frontend/streamlit_app.py

# 7. Start monitoring (Terminal 3)
docker-compose -f docker-compose-monitoring.yml up -d
```

**Access:**
- 🌐 Frontend: http://localhost:8501
- 🔌 API: http://localhost:8000
- 📖 API Docs: http://localhost:8000/docs
- 📊 Grafana: http://localhost:3000 (admin/admin123)
- 📡 Prometheus: http://localhost:9090

---

## 📝 License

MIT License — see LICENSE file for details.
