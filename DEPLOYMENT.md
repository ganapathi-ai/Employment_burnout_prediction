# Complete Deployment Guide - Render & GitHub Actions

## 🎯 Quick Overview

**Backend**: https://employment-burnout-prediction-1.onrender.com ✅ (Already Deployed)
**Frontend**: Deploy following Step 1 below
**GitHub Actions**: Configure following Step 2 below

---

## Step 1: Deploy Frontend on Render (5 minutes)

### 1.1 Create Web Service
- Go to: https://dashboard.render.com
- Click: **New +** → **Web Service**
- Connect your GitHub repository

### 1.2 Configure Service
**IMPORTANT**: Select **Python 3** from Environment dropdown (NOT Docker)

```
Name: burnout-frontend
Environment: Python 3 ⚠️
Root Directory: . (or leave empty)
Build Command: pip install streamlit requests python-dotenv
Start Command: streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
Plan: Free
```

### 1.3 Add Environment Variables
Click "Add Environment Variable" and add these 2:

```
API_URL=https://employment-burnout-prediction-1.onrender.com
ENVIRONMENT=production
```

### 1.4 Deploy
- Click **Create Web Service**
- Wait 2-3 minutes for deployment
- Copy your frontend URL

### 1.5 Get Deploy Hook
- Go to: Settings → Deploy Hook
- Copy the URL
- Save for Step 2

---

## Step 2: Configure GitHub Actions (5 minutes)

### 2.1 Add GitHub Secrets
Go to: Your GitHub Repo → Settings → Secrets and variables → Actions

Click **New repository secret** and add these 4:

**1. DOCKER_USERNAME**
```
Your Docker Hub username
```

**2. DOCKER_PASSWORD**
```
Your Docker Hub password or access token
Get token: https://hub.docker.com/settings/security
```

**3. RENDER_BACKEND_DEPLOY_HOOK**
```
Get from: Render Dashboard → employment-burnout-prediction-1 → Settings → Deploy Hook
Format: https://api.render.com/deploy/srv-xxxxx?key=yyyyy
```

**4. RENDER_FRONTEND_DEPLOY_HOOK**
```
Get from: Render Dashboard → burnout-frontend → Settings → Deploy Hook
Format: https://api.render.com/deploy/srv-xxxxx?key=yyyyy
```

### 2.2 Test CI/CD
```bash
git add .
git commit -m "test: CI/CD pipeline"
git push origin main
```

Check: GitHub → Actions tab (should show green checkmarks)

---

## Step 3: Verify Deployment

### Backend (Already Working)
```bash
curl https://employment-burnout-prediction-1.onrender.com/health
```
Expected: `{"status":"healthy","timestamp":"..."}`

### Frontend
Open your frontend URL in browser and test the prediction form.

### GitHub Actions
- Go to: Repository → Actions tab
- Both workflows should pass ✅

---

## 📋 Backend Configuration (Already Set)

Your backend is already deployed with these environment variables:

```
DATABASE_URL=postgresql://neondb_owner:npg_S3eaGPdmBzn4@ep-rapid-grass-aiuta04r-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
WANDB_API_KEY=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
ENVIRONMENT=production
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib
```

---

## 🧪 Local Testing

```bash
# Backend
python api/main.py
# Visit: http://localhost:8000/health

# Frontend (new terminal)
streamlit run frontend/streamlit_app.py
# Visit: http://localhost:8501
```

---

## 🆘 Troubleshooting

### Frontend shows Docker fields
- Scroll to top
- Change **Environment** dropdown to **Python 3**
- Docker fields will disappear

### Frontend can't connect to backend
- Verify `API_URL` environment variable is correct
- Check backend is running: `curl https://employment-burnout-prediction-1.onrender.com/health`

### GitHub Actions failing
- Verify all 4 secrets are added correctly (case-sensitive)
- Check deploy hook URLs are complete
- Review workflow logs for specific errors

### Service spinning down
- Free tier spins down after 15 minutes inactivity
- First request takes ~30 seconds to wake up
- This is normal behavior

---

## ✅ Success Checklist

- [x] Backend deployed and healthy
- [ ] Frontend deployed
- [ ] Frontend connects to backend
- [ ] GitHub secrets configured (4 secrets)
- [ ] CI/CD pipeline tested
- [ ] Both workflows passing

---

## 🔗 Quick Links

- **Render Dashboard**: https://dashboard.render.com
- **Backend API**: https://employment-burnout-prediction-1.onrender.com
- **API Docs**: https://employment-burnout-prediction-1.onrender.com/docs
- **GitHub Actions**: Your repo → Actions tab

---

**That's it!** Follow Step 1 to deploy frontend, Step 2 to configure GitHub Actions, and you're done! 🚀
