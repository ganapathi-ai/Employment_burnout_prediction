# 🚀 COMPLETE END-TO-END GUIDE: Burnout Prediction ML System

## What You're Building

A **production-grade Machine Learning system** that:
- ✅ Predicts employee burnout risk using ML models
- ✅ Provides REST API (FastAPI backend)
- ✅ Has web interface (Streamlit frontend)
- ✅ Stores data in PostgreSQL (Neon)
- ✅ Deploys automatically to cloud (Render)
- ✅ Tracks experiments (Weights & Biases)
- ✅ Monitors performance (Prometheus/Grafana)

**Tech Stack:**
- **Backend:** FastAPI + Python 3.13
- **Frontend:** Streamlit
- **Database:** PostgreSQL (Neon)
- **ML Models:** scikit-learn, XGBoost, RandomForest
- **Deployment:** Docker + Render
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana

---

## 📁 PROJECT STRUCTURE

```
Employers_Burnout_prediction/
├── api/
│   └── main.py                    # FastAPI server (backend)
├── frontend/
│   └── streamlit_app.py           # Web interface
├── scripts/
│   ├── preprocessing.py           # Data preprocessing
│   ├── train_models.py            # Model training
│   └── data_ingestion.py          # Database pipeline
├── tests/
│   └── test_api.py                # API tests
├── .github/
│   └── workflows/
│       └── backend.yml            # CI/CD automation
├── docker-compose.yml             # Local containerization
├── requirements.txt               # Python dependencies
├── .env                          # Local credentials (never commit)
├── .env.example                  # Template for .env
└── data/
    ├── work_from_home_burnout_dataset.csv (raw)
    └── work_from_home_burnout_dataset_transformed.csv (processed)
```

---

## PHASE 1: LOCAL SETUP (One Time Only)

### Step 1.1: Check Python Version

```powershell
cd c:\Users\lenovo\Documents\Employers_Burnout_prediction

# Verify Python 3.13 is installed
python --version
# Should show: Python 3.13.x
```

### Step 1.2: Create Virtual Environment

```powershell
# Create isolated Python environment
python -m venv venv

# Activate it (Windows PowerShell)
venv\Scripts\Activate.ps1

# You should see (venv) in your prompt
# (venv) PS C:\Users\lenovo\Documents\Employers_Burnout_prediction>
```

### Step 1.3: Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all packages from requirements.txt
pip install -r requirements.txt --prefer-binary
```

**What Gets Installed:**
- pandas, numpy, scipy (data science)
- scikit-learn, xgboost (ML models)
- fastapi, uvicorn (web API)
- streamlit (web UI)
- psycopg2-binary (PostgreSQL driver)
- pytest (testing)
- wandb (experiment tracking)
- prometheus-client (monitoring)

### Step 1.4: Create `.env` File (For Local Development)

**Copy contents of `.env.example`:**

```powershell
# In PowerShell, create .env by copying example
Copy-Item .env.example .env

# Edit .env with your credentials (NOT committed to git)
notepad .env
```

**What to Add:**

```env
# Database (can be empty for local development)
DATABASE_URL=

# ML Tracking
WANDB_API_KEY=

# Debugging
DEBUG=True
ENVIRONMENT=development
```

---

## PHASE 2: RUN LOCALLY (Development)

### Step 2.1: Start Backend API

**Terminal 1 (Backend):**

```powershell
# Make sure venv is activated
venv\Scripts\Activate.ps1

# Start FastAPI server on port 8000
python -m uvicorn api.main:app --reload

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Test Backend:**
```powershell
# In another terminal, test health endpoint
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","timestamp":"2024-01-15T10:30:00"}
```

### Step 2.2: Start Frontend

**Terminal 2 (Frontend):**

```powershell
# Activate venv in new terminal
venv\Scripts\Activate.ps1

# Start Streamlit on port 8501
streamlit run frontend/streamlit_app.py

# Expected output:
#   You can now view your Streamlit app in your browser.
#   Local URL: http://localhost:8501
```

**Visit in Browser:**
```
http://localhost:8501
```

You should see:
- Title: "🔥 Employee Burnout Risk Prediction System"
- 8 sliders for input values
- Predict button
- Risk prediction output

### Step 2.3: Test the API

**Use Swagger UI:**
```
http://localhost:8000/docs
```

**Or curl to make prediction:**

```powershell
curl -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d '{
    "work_hours": 10,
    "screen_time": 8,
    "meetings": 6,
    "breaks": 2,
    "after_hours": 3,
    "sleep": 6,
    "task_completion": 75,
    "day_type": 1
  }'

# Should return:
# {
#   "risk_probability": 0.72,
#   "risk_level": "High Risk",
#   "timestamp": "2024-01-15T10:30:00.123456",
#   "recommendations": [...]
# }
```

---

## PHASE 3: RUN TESTS

### Step 3.1: Unit Tests

```powershell
# Activate venv
venv\Scripts\Activate.ps1

# Run all tests
pytest tests/ -v

# Expected output shows:
# test_api.py::TestHealthEndpoint::test_health_check PASSED
# test_api.py::TestPredictEndpoint::test_predict_valid_input PASSED
# ... (10+ tests)
# ======================== 10 passed in 1.23s ========================
```

### Step 3.2: Check Code Quality

```powershell
# Lint code
flake8 api/ scripts/ tests/

# Should return: No output (no errors)
```

---

## PHASE 4: DEVELOPMENT WORKFLOW

### Every Time You Make Changes:

#### 4.1 Edit Code

**Example: Fix a bug in [api/main.py](api/main.py)**

```python
# Before (buggy):
risk_level = "High Risk" if probability > 0.5 else "Low Risk"

# After (fixed):
risk_level = "Critical" if probability > 0.8 else "High Risk" if probability > 0.5 else "Low Risk"
```

#### 4.2 Test Locally

```powershell
# Run tests to verify fix
pytest tests/test_api.py::TestPredictEndpoint -v

# Should show: PASSED
```

#### 4.3 Frontend Still Running?

**Browser:** Visit `http://localhost:8501` and test prediction

```
Input values → Click "Predict" → Should work correctly
```

#### 4.4 Commit Changes

```powershell
# Check what changed
git status

# Output shows: modified: api/main.py

# Stage the file
git add api/main.py

# Commit with descriptive message
git commit -m "Fix: Improve burnout risk level categorization"
```

---

## PHASE 5: GITHUB & DEPLOYMENT SETUP

### Step 5.1: Initialize Git (First Time Only)

```powershell
# Setup git with your identity
git config --global user.name "Your Name"
git config --global user.email "your-github-email@gmail.com"

# Check if git initialized (look for .git folder)
ls -la | findstr ".git"

# If no .git, initialize:
git init
```

### Step 5.2: Connect to GitHub Repository

```powershell
# Create repository on github.com first!
# Then connect local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/Employers_Burnout_prediction.git

# Verify connection
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/Employers_Burnout_prediction.git (fetch)
# origin  https://github.com/YOUR_USERNAME/Employers_Burnout_prediction.git (push)
```

### Step 5.3: First Push to GitHub

```powershell
# Stage all files
git add .

# Commit
git commit -m "Initial commit: ML system with FastAPI, Streamlit, and Render deployment"

# Set branch to main
git branch -M main

# Push to GitHub
git push -u origin main

# Expected output:
# * [new branch]      main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### Step 5.4: Add GitHub Secrets (For CI/CD)

**Go to GitHub:**
1. Your repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add these secrets:

| Name | Value | How to Get |
|------|-------|-----------|
| `DOCKER_USERNAME` | Your Docker Hub username | hub.docker.com |
| `DOCKER_PASSWORD` | Docker Hub password/token | hub.docker.com |
| `RENDER_API_KEY` | Render API key | render.com/account |
| `RENDER_SERVICE_ID` | Render service ID | (after creating service) |

### Step 5.5: Create Render Services

**Go to https://render.com and create 2 services:**

#### Service 1: Backend (FastAPI)
```
Name: burnout-api-backend
Branch: main
Build command: pip install -r requirements.txt
Start command: python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT

Environment Variables:
  DATABASE_URL=postgresql://...neon...
  WANDB_API_KEY=your_key
  ENVIRONMENT=production
```

#### Service 2: Frontend (Streamlit)
```
Name: burnout-app-frontend
Branch: main
Build command: pip install -r requirements.txt
Start command: streamlit run frontend/streamlit_app.py

Environment Variables:
  API_URL=https://burnout-api-backend.onrender.com
  ENVIRONMENT=production
```

---

## PHASE 6: AUTOMATIC DEPLOYMENT (CI/CD)

### How It Works:

```
You push code to GitHub
         ↓
GitHub Actions detected ✓
         ↓
Runs tests (pytest) ✓
         ↓
Checks code quality (flake8) ✓
         ↓
Builds Docker image ✓
         ↓
Pushes to Docker Hub ✓
         ↓
Tells Render to deploy ✓
         ↓
Your App is LIVE in 2-3 minutes!
```

### Step 6.1: Make a Code Change

```powershell
# Edit code
notepad api/main.py

# Test locally
pytest tests/ -v

# Commit
git add api/main.py
git commit -m "Fix: Handle edge cases in prediction"

# Push
git push origin main
```

### Step 6.2: Watch GitHub Actions

**Go to GitHub:**
```
Your repo → Actions tab → See workflow running
```

**Workflow file:** [.github/workflows/backend.yml](.github/workflows/backend.yml)

**What it does:**
1. ✅ Checkout code (10 seconds)
2. ✅ Setup Python (5 seconds)
3. ✅ Install dependencies (30 seconds)
4. ✅ Lint code with flake8 (10 seconds)
5. ✅ Run tests with pytest (20 seconds)
6. ✅ Build Docker image (30 seconds)
7. ✅ Push to Docker Hub (20 seconds)
8. ✅ Call Render API to deploy (10 seconds)

**Total time:** ~2-3 minutes

### Step 6.3: Verify Deployment

**Check Render dashboard:** https://dashboard.render.com

**Endpoints live after deployment:**
- Backend: `https://burnout-api-backend.onrender.com`
- Frontend: `https://burnout-app-frontend.onrender.com`

**Test health check:**
```powershell
curl https://burnout-api-backend.onrender.com/health

# Should return:
# {"status":"healthy","timestamp":"..."}
```

---

## PHASE 7: THE COMPLETE CODE FLOW

### Backend API Code ([api/main.py](api/main.py))

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

# Initialize FastAPI app
app = FastAPI(title="Burnout Risk Prediction API")

# Enable CORS (allow requests from frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input validation model
class UserData(BaseModel):
    work_hours: int
    screen_time: int
    meetings: int
    breaks: int
    after_hours: int
    sleep: int
    task_completion: int
    day_type: int

# Load model on startup
@app.on_event("startup")
async def load_model():
    global model, preprocessor
    model = joblib.load("models/model.joblib")
    preprocessor = joblib.load("models/preprocessor.joblib")

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Prediction endpoint
@app.post("/predict")
async def predict(data: UserData):
    # Convert input to array
    X = np.array([[
        data.work_hours, data.screen_time, data.meetings,
        data.breaks, data.after_hours, data.sleep,
        data.task_completion, data.day_type
    ]])
    
    # Preprocess
    X_processed = preprocessor.transform(X)
    
    # Predict
    probability = model.predict_proba(X_processed)[0][1]
    risk_level = "High Risk" if probability > 0.5 else "Low Risk"
    
    return {
        "risk_probability": round(probability, 2),
        "risk_level": risk_level,
        "recommendations": ["Take breaks", "Reduce workload"]
    }
```

### Frontend Code ([frontend/streamlit_app.py](frontend/streamlit_app.py))

```python
import streamlit as st
import requests
import os

# Page config
st.set_page_config(page_title="Burnout Predictor", layout="wide")

# Get API URL from environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
if ENVIRONMENT == "production":
    API_URL = os.getenv("API_URL")
else:
    API_URL = "http://localhost:8000"

# Title
st.title("🔥 Employee Burnout Risk Prediction System")

# Create form
col1, col2 = st.columns(2)

with col1:
    work_hours = st.slider("Work Hours Per Day", 0, 24, 8)
    screen_time = st.slider("Screen Time (hours)", 0, 12, 6)
    meetings = st.slider("Meetings Per Day", 0, 10, 3)
    breaks = st.slider("Breaks Per Day", 0, 10, 2)

with col2:
    after_hours = st.slider("After Hours Work (hours)", 0, 8, 2)
    sleep = st.slider("Sleep (hours)", 0, 12, 7)
    task_completion = st.slider("Task Completion (%)", 0, 100, 80)
    day_type = st.selectbox("Day Type", [0, 1], format_func=lambda x: "Weekend" if x == 0 else "Weekday")

# Predict button
if st.button("🎯 Predict Burnout Risk"):
    payload = {
        "work_hours": work_hours,
        "screen_time": screen_time,
        "meetings": meetings,
        "breaks": breaks,
        "after_hours": after_hours,
        "sleep": sleep,
        "task_completion": task_completion,
        "day_type": day_type
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        result = response.json()
        
        # Display results
        st.success(f"Prediction: **{result['risk_level']}**")
        st.metric("Risk Probability", f"{result['risk_probability']*100:.1f}%")
        
        # Show recommendations
        st.info("💡 Recommendations:\n" + "\n".join(result['recommendations']))
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

### Test Code ([tests/test_api.py](tests/test_api.py))

```python
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

class TestPredictEndpoint:
    def test_predict_valid_input(self):
        payload = {
            "work_hours": 10,
            "screen_time": 8,
            "meetings": 6,
            "breaks": 2,
            "after_hours": 3,
            "sleep": 6,
            "task_completion": 75,
            "day_type": 1
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        result = response.json()
        assert "risk_level" in result
        assert "risk_probability" in result

    def test_predict_invalid_input(self):
        payload = {"work_hours": 100}  # Invalid
        response = client.post("/predict", json=payload)
        assert response.status_code == 422  # Validation error
```

---

## PHASE 8: DOCKER (Optional Local)

### Run Everything with Docker

```powershell
# Start all services (MySQL, API, Streamlit, Prometheus, Grafana)
docker-compose up

# Expected output:
# postgres_1     | database system is ready to accept connections
# api_1          | Uvicorn running on 0.0.0.0:8000
# streamlit_1    | Session state initialized
# prometheus_1   | Server is ready to receive web requests
# grafana_1      | Listening on 0.0.0.0:3000
```

**Services available:**
- Backend: http://localhost:8000
- Frontend: http://localhost:8501
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

---

## DAILY WORKFLOW

### Every Time You Work:

```powershell
# 1. Activate venv
venv\Scripts\Activate.ps1

# 2. Edit code in VS Code
code .

# 3. Test locally
pytest tests/ -v

# 4. Commit changes
git add .
git commit -m "Feature: Add X"

# 5. Push to GitHub
git push origin main

# 6. Watch GitHub Actions
# https://github.com/YOUR_USERNAME/Employers_Burnout_prediction/actions

# 7. Check Render
# https://dashboard.render.com

# 8. App is LIVE within 2-3 minutes! ✅
```

---

## TROUBLESHOOTING

### Backend Won't Start

```powershell
# Check if port 8000 is already used
netstat -ano | findstr :8000

# Use different port
python -m uvicorn api.main:app --port 8001 --reload
```

### Frontend Can't Reach Backend

```powershell
# Check API is running
curl http://localhost:8000/health

# Check frontend pointing to correct URL
# In frontend/streamlit_app.py: API_URL = "http://localhost:8000"
```

### Tests Fail

```powershell
# Run with verbose output
pytest tests/ -v -s

# Run specific test
pytest tests/test_api.py::TestHealthEndpoint::test_health_check -v
```

### GitHub Actions Failed

```
GitHub → Your repo → Actions tab → Click failed workflow
See detailed error log
Fix locally, test, commit, push again
```

---

## SUCCESS INDICATORS

### Development is Working When:
- ✅ Backend starts: `http://localhost:8000/docs` shows Swagger UI
- ✅ Frontend starts: `http://localhost:8501` loads Streamlit app
- ✅ Tests pass: `pytest tests/ -v` shows all green
- ✅ Prediction works: Frontend slider → Predict button → Result appears

### Deployment is Working When:
- ✅ GitHub Actions runs on push: Green checkmark on repo
- ✅ Render deploys: Status changes to "Live"
- ✅ App accessible: `https://your-app.onrender.com` loads
- ✅ Prediction works in cloud: Fill form → Get result

---

## SUMMARY

| Phase | Action | Command | Time |
|-------|--------|---------|------|
| **1** | Setup | `python -m venv venv && pip install -r requirements.txt` | 2 min |
| **2** | Run Backend | `python -m uvicorn api.main:app --reload` | 5 sec |
| **2** | Run Frontend | `streamlit run frontend/streamlit_app.py` | 5 sec |
| **3** | Test | `pytest tests/ -v` | 10 sec |
| **4** | Work | Edit → Test → Commit | 5 min |
| **5** | Push | `git push origin main` | 10 sec |
| **6** | Deploy | GitHub Actions → Render (automatic) | 2-3 min |
| **Result** | **APP LIVE** | Visit `https://your-app.onrender.com` | ✅ |

---

## YOU ARE NOW READY!

```
Local Development: ✅ Working
Testing: ✅ Working
GitHub: ✅ Connected
CI/CD: ✅ Automated
Deployment: ✅ Live
Monitoring: ✅ Ready

START HERE:
1. Choose a feature to build
2. Edit code
3. Run tests
4. Push to GitHub
5. Watch it deploy live!

Next: Open VS Code and start coding! 🚀
```

