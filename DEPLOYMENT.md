# Complete Deployment Guide

## 🎯 Overview

**Backend**: FastAPI with ML model
**Frontend**: Advanced Streamlit dashboard
**Deployment**: Render (Free tier)
**CI/CD**: GitHub Actions

---

## Step 1: Setup Environment Variables

### 1.1 Copy .env.example to .env
```bash
cp .env.example .env
```

### 1.2 Update .env with your credentials
Edit `.env` file with your actual values:
- Database URL (Neon)
- WandB API Key
- Other configurations

**⚠️ Never commit .env file to Git!**

---

## Step 2: Deploy Backend on Render

### 2.1 Create Web Service
1. Go to: https://dashboard.render.com
2. Click: **New +** → **Web Service**
3. Connect your GitHub repository
4. Select **Python 3** environment

### 2.2 Configure
```
Name: burnout-api
Environment: Python 3
Build Command: pip install -r requirements.txt && python scripts/train_model.py
Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### 2.3 Add Environment Variables
In Render dashboard, add these from your `.env` file:
```
DATABASE_URL=<your_database_url>
WANDB_API_KEY=<your_wandb_key>
ENVIRONMENT=production
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib
```

### 2.4 Deploy
- Click **Create Web Service**
- Wait 3-5 minutes (model training included)
- Copy your backend URL

---

## Step 3: Deploy Frontend on Render

### 3.1 Create Web Service
1. Click: **New +** → **Web Service**
2. Connect same repository
3. Select **Python 3** environment

### 3.2 Configure
```
Name: burnout-frontend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

### 3.3 Add Environment Variables
```
API_URL=<your_backend_url_from_step_2>
ENVIRONMENT=production
```

### 3.4 Deploy
- Click **Create Web Service**
- Wait 2-3 minutes
- Copy your frontend URL

---

## Step 4: Configure GitHub Actions

### 4.1 Add GitHub Secrets
Go to: Repository → Settings → Secrets and variables → Actions

Add these 4 secrets:

1. **DOCKER_USERNAME**: Your Docker Hub username
2. **DOCKER_PASSWORD**: Docker Hub access token
3. **RENDER_BACKEND_DEPLOY_HOOK**: From backend Settings → Deploy Hook
4. **RENDER_FRONTEND_DEPLOY_HOOK**: From frontend Settings → Deploy Hook

### 4.2 Test CI/CD
```bash
git add .
git commit -m "test: CI/CD"
git push origin main
```

<!-- another push intended to trigger workflows with a different commit name -->

---

## Step 5: Verify Deployment

### Backend
```bash
curl <your_backend_url>/health
```
Expected: `{"status":"healthy",...}`

### Frontend
Open your frontend URL in browser

### GitHub Actions
Check: Repository → Actions tab

---

## 🧪 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python scripts/train_model.py

# Run backend
python api/main.py

# Run frontend (new terminal)
streamlit run frontend/streamlit_app.py
```

---

## 📊 Features

### Backend
- FastAPI REST API
- ML model with 17 engineered features
- Real-time predictions
- Health monitoring

### Frontend
- Interactive dashboard
- Gauge charts for risk scores
- Bar charts for risk factors
- Personalized recommendations
- Analytics tab with dataset insights
- Correlation heatmaps

---

## 🔒 Security

- ✅ Credentials in environment variables only
- ✅ .env file in .gitignore
- ✅ No hardcoded secrets
- ✅ CORS configured

---

## 🆘 Troubleshooting

### Backend not starting
- Check Render logs
- Verify environment variables
- Ensure CSV data file exists

### Frontend can't connect
- Verify API_URL is correct
- Check backend is running
- Test backend health endpoint

### GitHub Actions failing
- Verify all 4 secrets are added
- Check deploy hook URLs
- Review workflow logs

---

## ✅ Success Checklist

- [ ] .env file configured locally
- [ ] Backend deployed on Render
- [ ] Frontend deployed on Render
- [ ] Environment variables set on Render
- [ ] GitHub secrets configured
- [ ] CI/CD pipeline passing
- [ ] Backend health check works
- [ ] Frontend loads and connects

---

**Your ML system is now live!** 🚀
