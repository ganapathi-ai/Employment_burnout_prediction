# 🚀 Local Development Setup

Complete guide to set up the project on your local machine.

## Prerequisites

### Required Software
- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **PostgreSQL** (Optional - for local DB)
- **Docker** (Optional - for containerized setup)

### Required Accounts
- **GitHub** (for code access)
- **Neon** ([Sign up](https://neon.tech)) - Free Postgres database
- **Weights & Biases** ([Sign up](https://wandb.ai)) - ML experiment tracking

## Step-by-Step Setup

### 1. Clone Repository

```bash
git clone https://github.com/ganapathi-ai/Employment_burnout_prediction.git
cd Employment_burnout_prediction
```

### 2. Create Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected time**: 2-3 minutes

### 4. Setup Environment Variables

Create `.env` file in project root:

```bash
# Copy example file
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Database (Get from Neon.tech)
DATABASE_URL=postgresql://user:password@host/database

# Weights & Biases (Get from wandb.ai/settings)
WANDB_API_KEY=your_wandb_api_key
WANDB_ENTITY=your_wandb_username

# API Configuration
API_URL=http://localhost:8000
ENVIRONMENT=development

# Model Paths (default)
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib
DATA_PATH=data/work_from_home_burnout_dataset.csv
```

### 5. Setup Neon Database

1. Go to [neon.tech](https://neon.tech)
2. Create new project
3. Copy connection string
4. Paste in `.env` as `DATABASE_URL`

**Test connection**:
```bash
python -c "from scripts.data_ingestion import PostgresDataStore; PostgresDataStore().test_connection()"
```

Expected output: `✓ Database connection successful`

### 6. Setup Weights & Biases

```bash
wandb login
```

Or set `WANDB_API_KEY` in `.env`

### 7. Train ML Model

```bash
python scripts/train_model.py
```

**What happens**:
- Loads dataset (1800 samples)
- Engineers 17 features
- Trains 3 models (RF, GB, XGBoost)
- Selects best model (ROC-AUC)
- Saves to `models/` directory
- Logs to W&B

**Expected time**: 1-2 minutes

**Output files**:
- `models/best_model.joblib`
- `models/preprocessor.joblib`
- `models/feature_names.joblib`

### 8. Run Backend API

**Terminal 1**:
```bash
python api/main.py
```

**Expected output**:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Model loaded from models/best_model.joblib
INFO:     Database table initialized
```

**Test API**:
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy","timestamp":"...","model_loaded":true}`

### 9. Run Frontend

**Terminal 2** (keep backend running):
```bash
streamlit run frontend/streamlit_app.py
```

**Expected output**:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 10. Test the System

1. Open browser: http://localhost:8501
2. Enter test data:
   - Work Hours: 8
   - Screen Time: 6
   - Meetings: 3
   - Breaks: 4
   - Sleep: 7.5
   - Task Completion: 85%
3. Click "Analyze Burnout Risk"
4. View results and recommendations

## Verify Installation

Run all tests:
```bash
pytest tests/ -v
```

Expected: `10 passed in ~2s`

Check code quality:
```bash
pylint api/ --fail-under=7.0
```

Expected: `Your code has been rated at 10.00/10`

## Project Structure

```
Employment_burnout_prediction/
├── api/
│   └── main.py              # FastAPI backend
├── frontend/
│   └── streamlit_app.py     # Streamlit UI
├── scripts/
│   ├── train_model.py       # Model training
│   ├── preprocessing.py     # Data preprocessing
│   └── data_ingestion.py    # Database operations
├── tests/
│   ├── test_comprehensive.py
│   └── conftest.py
├── models/                  # Generated after training
│   ├── best_model.joblib
│   ├── preprocessor.joblib
│   └── feature_names.joblib
├── data/
│   ├── work_from_home_burnout_dataset.csv
│   └── work_from_home_burnout_dataset_transformed.csv
├── .env                     # Your credentials (create this)
├── .env.example             # Template
├── requirements.txt         # Dependencies
└── README.md
```

## Common Commands

### Development
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run backend
python api/main.py

# Run frontend
streamlit run frontend/streamlit_app.py

# Run tests
pytest tests/ -v

# Check code quality
pylint api/
flake8 api/
```

### Training
```bash
# Train model
python scripts/train_model.py

# Train with hyperparameter tuning
python scripts/train_model_with_tuning.py

# Preprocess data
python scripts/preprocessing.py
```

### Database
```bash
# Test connection
python -c "from scripts.data_ingestion import PostgresDataStore; PostgresDataStore().test_connection()"

# View stored predictions (requires psql)
psql $DATABASE_URL -c "SELECT * FROM user_requests LIMIT 5;"
```

## Troubleshooting

### Issue: Module not found
```bash
pip install -r requirements.txt
```

### Issue: Database connection failed
- Check `DATABASE_URL` in `.env`
- Verify Neon database is active
- Check internet connection

### Issue: Model files not found
```bash
python scripts/train_model.py
```

### Issue: Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows (find PID, then kill)
```

### Issue: W&B login failed
```bash
wandb login
# Or set WANDB_API_KEY in .env
```

## Optional: Docker Setup

### Build and run with Docker:
```bash
# Build image
docker build -t burnout-api .

# Run container
docker run -p 8000:8000 --env-file .env burnout-api
```

### Run with docker-compose:
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Optional: Monitoring Setup

### Start Prometheus + Grafana:
```bash
docker-compose -f docker-compose-monitoring.yml up -d
```

**Access**:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Development Workflow

1. **Make changes** to code
2. **Run tests**: `pytest tests/ -v`
3. **Check quality**: `pylint api/`
4. **Test locally**: Run API + Frontend
5. **Commit**: `git commit -m "description"`
6. **Push**: `git push origin main`
7. **CI/CD**: GitHub Actions runs automatically

## Next Steps

- ✅ Local setup complete
- 📖 Read [API.md](API.md) for API documentation
- 🧪 Read [TESTING.md](TESTING.md) for testing guide
- 🚀 Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment

## Need Help?

- 📧 Open an issue on GitHub
- 📚 Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 💬 Review existing issues

---

**Setup Time**: ~15-20 minutes for first-time setup
