# 🚀 Production Deployment Guide

Complete guide to deploy the Employee Burnout Prediction System to production.

## Deployment Options

1. **Render** (Recommended - Free tier available)
2. **AWS** (EC2, ECS, Lambda)
3. **Google Cloud** (Cloud Run, App Engine)
4. **Azure** (App Service, Container Instances)
5. **Heroku** (Deprecated free tier)

This guide focuses on **Render** deployment.

## Prerequisites

### Required Accounts
- ✅ GitHub account (code repository)
- ✅ Render account ([Sign up](https://render.com))
- ✅ Neon account ([Sign up](https://neon.tech)) - Postgres database
- ✅ Weights & Biases account ([Sign up](https://wandb.ai))
- ✅ Docker Hub account (optional - for custom images)

### Required Files (Already in repo)
- ✅ `render.yaml` - Render configuration
- ✅ `Dockerfile` - Container definition
- ✅ `requirements.txt` - Python dependencies
- ✅ `.github/workflows/backend.yml` - CI/CD pipeline
- ✅ `models/` - Trained model artifacts

## Deployment Architecture

```
GitHub Repository
       ↓
GitHub Actions (CI/CD)
       ↓
Docker Hub (Optional)
       ↓
Render Platform
       ├── Backend Service (FastAPI)
       └── Frontend Service (Streamlit)
       ↓
Neon Postgres Database
```

## Step-by-Step Deployment

### Phase 1: Prepare Repository

#### 1. Ensure all files are committed
```bash
git status
git add -A
git commit -m "Prepare for deployment"
git push origin main
```

#### 2. Verify model files exist
```bash
ls models/
# Should show:
# - best_model.joblib
# - preprocessor.joblib
# - feature_names.joblib
```

If missing, train model:
```bash
python scripts/train_model.py
git add models/
git commit -m "Add trained model artifacts"
git push origin main
```

### Phase 2: Setup Neon Database

#### 1. Create Neon Project
- Go to [neon.tech](https://neon.tech)
- Click "Create Project"
- Name: `burnout-prediction-db`
- Region: Choose closest to your users

#### 2. Get Connection String
- Click "Connection Details"
- Copy "Connection string"
- Format: `postgresql://user:password@host/database?sslmode=require`

#### 3. Test Connection (Optional)
```bash
# Add to .env temporarily
DATABASE_URL=postgresql://...

# Test
python -c "from scripts.data_ingestion import PostgresDataStore; PostgresDataStore().test_connection()"
```

### Phase 3: Setup Render Services

#### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Authorize Render to access your repositories

#### 2. Deploy Backend (FastAPI)

**Option A: Using render.yaml (Recommended)**

1. Go to Render Dashboard
2. Click "New" → "Blueprint"
3. Connect repository: `Employment_burnout_prediction`
4. Render will detect `render.yaml`
5. Click "Apply"

**Option B: Manual Setup**

1. Click "New" → "Web Service"
2. Connect repository
3. Configure:
   - **Name**: `burnout-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free` (or `Starter` for better performance)

#### 3. Add Environment Variables (Backend)

In Render dashboard → Service → Environment:

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
WANDB_API_KEY=your_wandb_api_key
WANDB_ENTITY=your_wandb_username
ENVIRONMENT=production
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib
DATA_PATH=data/work_from_home_burnout_dataset.csv
PYTHON_VERSION=3.9.18
```

#### 4. Deploy Frontend (Streamlit)

1. Click "New" → "Web Service"
2. Connect same repository
3. Configure:
   - **Name**: `burnout-frontend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run frontend/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Instance Type**: `Free`

#### 5. Add Environment Variables (Frontend)

```env
API_URL=https://burnout-api.onrender.com
ENVIRONMENT=production
```

**Important**: Replace `burnout-api` with your actual backend service name.

### Phase 4: Configure CI/CD (GitHub Actions)

#### 1. Add GitHub Secrets

Go to GitHub repo → Settings → Secrets and variables → Actions

Add these secrets:

| Secret Name | Value | Where to get |
|------------|-------|--------------|
| `DOCKER_USERNAME` | Your Docker Hub username | docker.com |
| `DOCKER_PASSWORD` | Docker Hub access token | docker.com/settings/security |
| `RENDER_BACKEND_DEPLOY_HOOK` | Backend deploy hook URL | Render service settings |
| `RENDER_FRONTEND_DEPLOY_HOOK` | Frontend deploy hook URL | Render service settings |

#### 2. Get Render Deploy Hooks

For each service:
1. Go to Render Dashboard → Service
2. Settings → Deploy Hook
3. Copy URL
4. Add to GitHub Secrets

#### 3. Verify Workflows

Check `.github/workflows/backend.yml`:
- ✅ Runs on push to main
- ✅ Lints code (Pylint, Flake8)
- ✅ Runs tests (Pytest)
- ✅ Builds Docker image
- ✅ Deploys to Render

### Phase 5: Verify Deployment

#### 1. Check Backend Health

```bash
curl https://burnout-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-02-14T10:30:00",
  "model_loaded": true
}
```

#### 2. Test Prediction Endpoint

```bash
curl -X POST https://burnout-api.onrender.com/predict \
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

#### 3. Test Frontend

Open: `https://burnout-frontend.onrender.com`

- ✅ Page loads
- ✅ Input form works
- ✅ Prediction returns results
- ✅ Recommendations display

#### 4. Check Database

```bash
# Connect to Neon
psql $DATABASE_URL

# Check predictions
SELECT COUNT(*) FROM user_requests;
SELECT * FROM user_requests LIMIT 5;
```

### Phase 6: Monitor Deployment

#### 1. Render Logs

- Go to Render Dashboard → Service → Logs
- Monitor for errors
- Check startup logs

#### 2. Weights & Biases

- Go to [wandb.ai](https://wandb.ai)
- Check project: `burnout-prediction`
- Verify training runs logged

#### 3. GitHub Actions

- Go to GitHub repo → Actions
- Check workflow runs
- Verify all steps pass

## Production Configuration

### render.yaml

```yaml
services:
  - type: web
    name: burnout-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: WANDB_API_KEY
        sync: false
      - key: ENVIRONMENT
        value: production

  - type: web
    name: burnout-frontend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run frontend/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: API_URL
        value: https://burnout-api.onrender.com
```

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Performance Optimization

### 1. Enable Caching

Add to `api/main.py`:
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
```

### 2. Use Gunicorn (Production ASGI server)

Update start command:
```bash
gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 3. Optimize Model Loading

Models are loaded once at startup (already implemented).

### 4. Database Connection Pooling

Already configured in `api/main.py` with SQLAlchemy.

## Scaling

### Free Tier Limits (Render)
- 750 hours/month
- 512 MB RAM
- Sleeps after 15 min inactivity
- Cold start: ~30-60 seconds

### Upgrade to Paid Tier
- **Starter**: $7/month
  - Always on
  - 512 MB RAM
  - No cold starts
- **Standard**: $25/month
  - 2 GB RAM
  - Better performance

### Horizontal Scaling
- Deploy multiple instances
- Add load balancer
- Use Redis for session management

## Security Checklist

- ✅ All secrets in environment variables
- ✅ No hardcoded credentials
- ✅ HTTPS enabled (Render default)
- ✅ CORS configured
- ✅ Input validation (Pydantic)
- ✅ Database connection encrypted
- ✅ .env file in .gitignore

## Monitoring & Alerts

### 1. Render Monitoring
- CPU usage
- Memory usage
- Request count
- Response time

### 2. Custom Monitoring (Optional)

Add Sentry for error tracking:
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

### 3. Uptime Monitoring

Use services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

## Rollback Strategy

### If deployment fails:

1. **Check logs**: Render Dashboard → Logs
2. **Revert commit**:
   ```bash
   git revert HEAD
   git push origin main
   ```
3. **Manual rollback**: Render Dashboard → Deployments → Redeploy previous version

## Cost Estimation

### Free Tier (Render + Neon)
- Backend: Free (with sleep)
- Frontend: Free (with sleep)
- Database: Free (0.5 GB)
- **Total**: $0/month

### Paid Tier
- Backend: $7/month (Starter)
- Frontend: $7/month (Starter)
- Database: $19/month (Neon Pro)
- **Total**: $33/month

## Troubleshooting

### Issue: Service won't start
- Check logs for errors
- Verify environment variables
- Ensure model files are in repo

### Issue: Database connection failed
- Verify DATABASE_URL format
- Check Neon database is active
- Ensure SSL mode is enabled

### Issue: Cold start timeout
- Upgrade to paid tier
- Optimize model loading
- Use health check endpoint

### Issue: Out of memory
- Reduce model size
- Upgrade instance type
- Optimize feature engineering

## Post-Deployment

### 1. Update README
Add deployment URLs:
```markdown
## Live Demo
- API: https://burnout-api.onrender.com
- Frontend: https://burnout-frontend.onrender.com
```

### 2. Setup Custom Domain (Optional)
- Buy domain (Namecheap, GoDaddy)
- Add CNAME record
- Configure in Render settings

### 3. Enable Analytics
- Google Analytics
- Mixpanel
- PostHog

## Maintenance

### Regular Tasks
- Monitor logs weekly
- Check database size monthly
- Update dependencies quarterly
- Retrain model quarterly

### Updates
```bash
# Make changes
git add -A
git commit -m "Update: description"
git push origin main
# GitHub Actions will auto-deploy
```

---

**Deployment Time**: ~30-45 minutes for first-time deployment

**Next Steps**: 
- 📊 Monitor performance
- 🔍 Collect user feedback
- 🚀 Plan feature enhancements
