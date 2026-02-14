# 🚀 Setup Guide

Complete step-by-step guide to set up the Employee Burnout Prediction System locally.

## Prerequisites

### Required Software
- **Python**: 3.9 or higher
- **Git**: Latest version
- **pip**: Python package manager
- **Text Editor**: VS Code (recommended) or any IDE

### Required Accounts
- **Neon**: Free PostgreSQL database ([neon.tech](https://neon.tech))
- **Weights & Biases**: ML tracking (optional) ([wandb.ai](https://wandb.ai))
- **GitHub**: For cloning repository

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space
- **Internet**: Required for API calls and database

## Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/ganapathi-ai/Employment_burnout_prediction.git

# Navigate to project directory
cd Employment_burnout_prediction

# Verify files
ls -la  # Linux/Mac
dir     # Windows
```

**Expected Output**: You should see folders like `api/`, `frontend/`, `scripts/`, `models/`, etc.

## Step 2: Create Virtual Environment

### On Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show (venv) prefix)
```

### On macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) prefix)
```

## Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected Packages**:
- fastapi, uvicorn
- streamlit
- pandas, numpy, scikit-learn, xgboost
- sqlalchemy, psycopg2-binary
- pytest, pylint
- wandb, prometheus-client

**Troubleshooting**:
- If `psycopg2-binary` fails on Windows, install Visual C++ Build Tools
- If `xgboost` fails, try: `pip install xgboost --no-cache-dir`

## Step 4: Setup Database (Neon)

### Create Neon Account
1. Go to [neon.tech](https://neon.tech)
2. Sign up with GitHub/Google
3. Create new project: "burnout-prediction"
4. Select region: US East (or closest to you)

### Get Database Credentials
1. In Neon dashboard, go to "Connection Details"
2. Copy the connection string (starts with `postgresql://`)
3. Note down individual credentials:
   - Host: `ep-xxxxx.aws.neon.tech`
   - Database: `neondb`
   - User: `neondb_owner`
   - Password: `npg_xxxxx`

### Test Connection
```bash
# Install psql (optional)
# Windows: Download from PostgreSQL website
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql-client

# Test connection
psql "postgresql://neondb_owner:YOUR_PASSWORD@YOUR_HOST/neondb?sslmode=require"

# If successful, you'll see: neondb=>
# Type \q to exit
```

## Step 5: Setup Weights & Biases (Optional)

### Create W&B Account
1. Go to [wandb.ai](https://wandb.ai)
2. Sign up with GitHub/Google
3. Go to Settings → API Keys
4. Copy your API key (starts with `wandb_v1_`)

### Test W&B
```bash
# Login to W&B
wandb login

# Paste your API key when prompted
# You should see: "Successfully logged in"
```

## Step 6: Configure Environment Variables

### Create .env File
```bash
# Copy example file
cp .env.example .env

# On Windows
copy .env.example .env
```

### Edit .env File
Open `.env` in your text editor and update:

```env
# Database Configuration (from Neon)
PGHOST=your-neon-host.aws.neon.tech
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=your-neon-password
PGSSLMODE=require
PGCHANNELBINDING=require
DATABASE_URL=postgresql://neondb_owner:your-password@your-host/neondb?sslmode=require

# Weights & Biases (Optional)
WANDB_API_KEY=your-wandb-api-key
WANDB_ENTITY=your-wandb-username
ENABLE_WANDB=true

# Model Paths (Leave as is)
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib

# API Configuration (Leave as is)
API_HOST=0.0.0.0
API_PORT=8000
API_LOG_LEVEL=info

# Frontend Configuration (Leave as is)
STREAMLIT_SERVER_PORT=8501
API_URL=http://localhost:8000

# Environment
ENVIRONMENT=development
DEBUG=False
```

**Important**: Replace `your-neon-host`, `your-password`, and `your-wandb-api-key` with actual values.

## Step 7: Initialize Database

```bash
# Run database initialization script
python scripts/data_ingestion.py

# Expected output:
# ✓ Database connected
# ✓ Table created
# ✓ Data loaded
```

**Verify in Neon Dashboard**:
1. Go to Neon dashboard
2. Click "SQL Editor"
3. Run: `SELECT COUNT(*) FROM user_requests;`
4. Should return 0 (empty table)

## Step 8: Train ML Model

```bash
# Train the model
python scripts/train_model.py

# Expected output:
# Loading data...
# Dataset shape: (22750, 10)
# Engineering features...
# Training models...
# RandomForest: Accuracy: 0.9889, ROC-AUC: 0.9779
# [BEST] Best model: RandomForest
# [OK] Model saved: models/best_model.joblib
```

**Training Time**: 2-5 minutes

**Output Files**:
- `models/best_model.joblib` (trained model)
- `models/preprocessor.joblib` (scaler)
- `models/feature_names.joblib` (feature list)

**W&B Dashboard**:
- If W&B is enabled, check your dashboard at wandb.ai
- You'll see training metrics, confusion matrix, ROC curve

## Step 9: Run Backend API

### Start Backend Server
```bash
# Run backend
python api/main.py

# Or using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output**:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test Backend
Open browser and visit:
- **API Info**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

### Test Prediction Endpoint
```bash
# Using curl
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

**Expected Response**:
```json
{
  "risk_level": "Low",
  "risk_probability": 0.15,
  "timestamp": "2024-02-14T10:30:00",
  "features": {...}
}
```

## Step 10: Run Frontend

### Open New Terminal
Keep backend running, open a new terminal window.

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Start Frontend
```bash
# Run Streamlit app
streamlit run frontend/streamlit_app.py

# Expected output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501
```

### Access Frontend
Open browser and visit: http://localhost:8501

**You should see**:
- Employee Burnout Risk Analyzer dashboard
- Input sliders for work metrics
- "Analyze Burnout Risk" button

## Step 11: Test Complete System

### Test Prediction Flow
1. In frontend (http://localhost:8501):
   - Enter Name: "John Doe"
   - Set Work Hours: 10
   - Set Screen Time: 8
   - Set Meetings: 5
   - Set Breaks: 2
   - Set Sleep: 6
   - Set Task Completion: 70%
   - Check "After-Hours Work"
   - Click "Analyze Burnout Risk"

2. **Expected Result**:
   - Risk Level: High
   - Risk Score: ~75%
   - Personalized recommendations
   - Visualizations

3. **Verify Database**:
   ```sql
   -- In Neon SQL Editor
   SELECT * FROM user_requests ORDER BY created_at DESC LIMIT 1;
   ```

## Step 12: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=api --cov-report=html

# Expected output:
# tests/test_comprehensive.py::test_health_check PASSED
# tests/test_comprehensive.py::test_predict_endpoint PASSED
# ... (10 tests total)
# ========== 10 passed in 5.23s ==========
```

### View Coverage Report
```bash
# Open coverage report
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

## Step 13: Code Quality Checks

```bash
# Run Pylint
pylint api/ --fail-under=7.0

# Run Flake8
flake8 api/ --max-line-length=120

# Format code with Black
black api/ frontend/ scripts/

# Sort imports
isort api/ frontend/ scripts/
```

## Common Issues & Solutions

### Issue 1: Port Already in Use
**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue 2: Database Connection Failed
**Error**: `could not connect to server`

**Solution**:
- Verify DATABASE_URL in `.env`
- Check Neon dashboard (database might be sleeping)
- Test connection with psql
- Ensure SSL mode is `require`

### Issue 3: Model Not Found
**Error**: `FileNotFoundError: models/best_model.joblib`

**Solution**:
```bash
# Train model again
python scripts/train_model.py

# Verify model files exist
ls models/
```

### Issue 4: W&B Login Failed
**Error**: `wandb: ERROR Unable to authenticate`

**Solution**:
```bash
# Re-login
wandb login --relogin

# Or disable W&B
# In .env, set: ENABLE_WANDB=false
```

### Issue 5: Import Errors
**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Database connected (Neon)
- [ ] W&B configured (optional)
- [ ] .env file configured
- [ ] Model trained successfully
- [ ] Backend running (http://localhost:8000)
- [ ] Frontend running (http://localhost:8501)
- [ ] Prediction works end-to-end
- [ ] Tests passing (10/10)
- [ ] Code quality checks pass

## Next Steps

1. **Explore API**: Visit http://localhost:8000/docs
2. **Test Predictions**: Try different input combinations
3. **View Analytics**: Check Analytics tab in frontend
4. **Monitor Metrics**: Setup Prometheus/Grafana (optional)
5. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) for production

## Quick Commands Reference

```bash
# Start backend
python api/main.py

# Start frontend
streamlit run frontend/streamlit_app.py

# Train model
python scripts/train_model.py

# Run tests
pytest tests/ -v

# Code quality
pylint api/ --fail-under=7.0
flake8 api/

# Database check
python check_db_data.py
```

## Getting Help

- **Documentation**: Check other docs in `docs/` folder
- **Issues**: [GitHub Issues](https://github.com/ganapathi-ai/Employment_burnout_prediction/issues)
- **API Docs**: http://localhost:8000/docs
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
