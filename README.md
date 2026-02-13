# Employee Burnout Prediction System

ML-powered system to predict employee burnout risk based on work-from-home metrics.

## 🚀 Quick Start

### Deploy to Render
Follow **DEPLOYMENT.md** for complete deployment guide.

**Backend**: https://employment-burnout-prediction-1.onrender.com ✅

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize models
python scripts/init_models.py

# Start backend
python api/main.py

# Start frontend (new terminal)
streamlit run frontend/streamlit_app.py
```

## 📁 Project Structure

```
├── api/                    # FastAPI backend
├── frontend/               # Streamlit frontend
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── .github/workflows/      # CI/CD pipelines
├── render.yaml            # Render deployment config
└── DEPLOYMENT.md          # Deployment guide
```

## 🔧 Tech Stack

- **Backend**: FastAPI, scikit-learn, PostgreSQL
- **Frontend**: Streamlit
- **Deployment**: Render
- **CI/CD**: GitHub Actions
- **ML Tracking**: Weights & Biases

## 📚 Documentation

- **DEPLOYMENT.md** - Complete deployment guide
- **COMPLETE_GUIDE.md** - Full project documentation

## ✅ Features

- Real-time burnout risk prediction
- RESTful API with FastAPI
- Interactive Streamlit dashboard
- Automated CI/CD pipeline
- Health monitoring endpoints
- PostgreSQL database integration

---

**Live Backend**: https://employment-burnout-prediction-1.onrender.com
