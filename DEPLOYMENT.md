# Complete Deployment Guide - Render & GitHub Actions

## 🎯 Deploy Both Services Fresh

---

## Step 1: Deploy Backend on Render (5 minutes)

### 1.1 Create Backend Service
- Go to: https://dashboard.render.com
- Click: **New +** → **Web Service**
- Connect your GitHub repository

### 1.2 Configure Backend
**IMPORTANT**: Select **Python 3** from Environment dropdown (NOT Docker)

```
Name: burnout-api
Environment: Python 3 ⚠️
Root Directory: . (or leave empty)
Build Command: pip install -r requirements.txt && python scripts/init_models.py
Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

### 1.3 Add Backend Environment Variables
Click "Add Environment Variable" and add these 5:

```
DATABASE_URL=postgresql://neondb_owner:npg_S3eaGPdmBzn4@ep-rapid-grass-aiuta04r-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
WANDB_API_KEY=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
ENVIRONMENT=production
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib
```

### 1.4 Deploy Backend
- Click **Create Web Service**
- Wait 2-3 minutes for deployment
- **Copy your backend URL** (e.g., https://burnout-api-xxxx.onrender.com)
- Test: `curl https://your-backend-url.onrender.com/health`

### 1.5 Get Backend Deploy Hook
- Go to: Settings → Deploy Hook
- Copy the URL
- Save for Step 3

---

## Step 2: Deploy Frontend on Render (5 minutes)

### 2.1 Create Frontend Service
- Click: **New +** → **Web Service**
- Connect your GitHub repository

### 2.2 Configure Frontend
**IMPORTANT**: Select **Python 3** from Environment dropdown (NOT Docker)

```
Name: burnout-frontend
Environment: Python 3 ⚠️
Root Directory: . (or leave empty)
Build Command: pip install streamlit requests python-dotenv
Start Command: streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0
Plan: Free
```

### 2.3 Add Frontend Environment Variables
Click "Add Environment Variable" and add these 2:

```
API_URL=https://your-backend-url.onrender.com
ENVIRONMENT=production
```
**Replace with YOUR actual backend URL from Step 1.4**

### 2.4 Deploy Frontend
- Click **Create Web Service**
- Wait 2-3 minutes for deployment
- Copy your frontend URL

### 2.5 Get Frontend Deploy Hook
- Go to: Settings → Deploy Hook
- Copy the URL
- Save for Step 3

---

## Step 3: Configure GitHub Actions (5 minutes)

### 3.1 Add GitHub Secrets
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
From Step 1.5 - Backend deploy hook
Format: https://api.render.com/deploy/srv-xxxxx?key=yyyyy
```

**4. RENDER_FRONTEND_DEPLOY_HOOK**
```
From Step 2.5 - Frontend deploy hook
Format: https://api.render.com/deploy/srv-xxxxx?key=yyyyy
```

### 3.2 Test CI/CD
```bash
git add .
git commit -m "test: CI/CD pipeline"
git push origin main
```

Check: GitHub → Actions tab (should show green checkmarks)

---

## Step 4: Verify Deployment

### Backend Health Check
```bash
curl https://your-backend-url.onrender.com/health
```
Expected: `{"status":"healthy","timestamp":"..."}`

### Frontend
Open your frontend URL in browser and test the prediction form.

### GitHub Actions
- Go to: Repository → Actions tab
- Both workflows should pass ✅

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
- Verify `API_URL` environment variable matches your backend URL
- Check backend is running: `curl https://your-backend-url.onrender.com/health`

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

- [ ] Backend deployed and healthy
- [ ] Frontend deployed
- [ ] Frontend connects to backend
- [ ] GitHub secrets configured (4 secrets)
- [ ] CI/CD pipeline tested
- [ ] Both workflows passing

---

## 🔗 Quick Links

- **Render Dashboard**: https://dashboard.render.com
- **GitHub Actions**: https://github.com/ganapathi-ai/Employment_burnout_prediction/actions

---

**Follow Steps 1-4 to complete deployment!** 🚀
