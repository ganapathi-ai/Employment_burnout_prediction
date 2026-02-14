# 🚢 Deployment Guide

Complete guide to deploy the Employee Burnout Prediction System to production.

## Deployment Options

1. **Render** (Recommended - Free tier available)
2. **AWS** (EC2, ECS, Lambda)
3. **Google Cloud** (Cloud Run, App Engine)
4. **Azure** (App Service)
5. **Docker** (Self-hosted)

---

## Option 1: Render (Recommended)

### Why Render?
- ✅ Free tier available
- ✅ Auto-deployment from GitHub
- ✅ Built-in SSL certificates
- ✅ Easy environment variable management
- ✅ Auto-scaling
- ✅ Health checks

### Prerequisites
- GitHub account
- Render account (free)
- Neon database (free)
- W&B account (optional)

### Step 1: Prepare Repository

```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**Required Files**:
- `requirements.txt` ✅
- `render.yaml` ✅
- `.env.example` ✅
- `Procfile` ✅ (optional)
- `runtime.txt` ✅ (optional)

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Deploy Backend

#### Using render.yaml (Automatic)

1. In Render dashboard, click "New +" → "Blueprint"
2. Connect your GitHub repository
3. Render will detect `render.yaml`
4. Click "Apply"

#### Manual Deployment

1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Configure:
   - **Name**: `burnout-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. Add Environment Variables:
   ```
   DATABASE_URL=postgresql://...
   WANDB_API_KEY=wandb_v1_...
   ENVIRONMENT=production
   MODEL_PATH=models/best_model.joblib
   PREPROCESSOR_PATH=models/preprocessor.joblib
   ```

5. Click "Create Web Service"

### Step 4: Deploy Frontend

1. Click "New +" → "Web Service"
2. Connect same GitHub repository
3. Configure:
   - **Name**: `burnout-frontend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
   - **Instance Type**: Free

4. Add Environment Variables:
   ```
   API_URL=https://burnout-api.onrender.com
   ENVIRONMENT=production
   ```

5. Click "Create Web Service"

### Step 5: Verify Deployment

1. **Backend**: Visit `https://burnout-api.onrender.com/health`
   - Should return: `{"status": "healthy", "model_loaded": true}`

2. **Frontend**: Visit `https://burnout-frontend.onrender.com`
   - Should load Streamlit dashboard

3. **Test Prediction**:
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
       "name": "Test",
       "user_id": "test"
     }'
   ```

### Step 6: Setup Auto-Deployment

1. In Render dashboard, go to service settings
2. Enable "Auto-Deploy": Yes
3. Now every push to `main` branch will auto-deploy

### Render Free Tier Limitations

- **Spin down after 15 minutes** of inactivity
- **First request after spin down**: 30-60 seconds
- **750 hours/month** free (enough for 1 service 24/7)
- **100 GB bandwidth/month**

**Solution**: Use cron job to ping every 10 minutes:
```bash
# Use cron-job.org or similar
curl https://burnout-api.onrender.com/health
```

---

## Option 2: AWS Deployment

### AWS EC2

#### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. Choose:
   - **AMI**: Ubuntu 22.04 LTS
   - **Instance Type**: t2.micro (free tier)
   - **Key Pair**: Create new or use existing
   - **Security Group**: Allow ports 22, 80, 443, 8000, 8501

#### Step 2: Connect to Instance

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
sudo apt install python3.9 python3-pip git -y
```

#### Step 3: Clone and Setup

```bash
# Clone repository
git clone https://github.com/ganapathi-ai/Employment_burnout_prediction.git
cd Employment_burnout_prediction

# Install dependencies
pip3 install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Edit with your credentials
```

#### Step 4: Run with Systemd

Create backend service:
```bash
sudo nano /etc/systemd/system/burnout-api.service
```

```ini
[Unit]
Description=Burnout API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Employment_burnout_prediction
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Create frontend service:
```bash
sudo nano /etc/systemd/system/burnout-frontend.service
```

```ini
[Unit]
Description=Burnout Frontend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Employment_burnout_prediction
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 -m streamlit run frontend/streamlit_app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

Start services:
```bash
sudo systemctl daemon-reload
sudo systemctl start burnout-api
sudo systemctl start burnout-frontend
sudo systemctl enable burnout-api
sudo systemctl enable burnout-frontend
```

#### Step 5: Setup Nginx (Optional)

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/burnout
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/burnout /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Option 3: Docker Deployment

### Step 1: Build Docker Image

```bash
# Build backend image
docker build -t burnout-api:latest .

# Test locally
docker run -p 8000:8000 --env-file .env burnout-api:latest
```

### Step 2: Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 3: Push to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag burnout-api:latest your-username/burnout-api:latest

# Push
docker push your-username/burnout-api:latest
```

---

## Option 4: Google Cloud Run

### Step 1: Install gcloud CLI

```bash
# Install gcloud
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

### Step 2: Deploy Backend

```bash
# Build and deploy
gcloud run deploy burnout-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=$DATABASE_URL,WANDB_API_KEY=$WANDB_API_KEY
```

### Step 3: Deploy Frontend

```bash
gcloud run deploy burnout-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_URL=https://burnout-api-xxx.run.app
```

---

## Environment Variables

### Required Variables

```env
# Database (Neon)
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# ML Tracking (Optional)
WANDB_API_KEY=wandb_v1_...
WANDB_ENTITY=your-username
ENABLE_WANDB=true

# Model Paths
MODEL_PATH=models/best_model.joblib
PREPROCESSOR_PATH=models/preprocessor.joblib

# Environment
ENVIRONMENT=production
DEBUG=False
```

### Frontend Variables

```env
API_URL=https://your-backend-url.com
ENVIRONMENT=production
```

---

## CI/CD with GitHub Actions

### Backend Workflow

File: `.github/workflows/backend.yml`

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      - run: pylint api/ --fail-under=7.0

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

### Setup Secrets

1. Go to GitHub repository → Settings → Secrets
2. Add secrets:
   - `RENDER_DEPLOY_HOOK`: Render deploy webhook URL
   - `DATABASE_URL`: Database connection string
   - `WANDB_API_KEY`: W&B API key

---

## Monitoring & Logging

### Render Logs

```bash
# View logs in Render dashboard
# Or use Render CLI
render logs -s burnout-api
```

### AWS CloudWatch

```bash
# Install CloudWatch agent
sudo apt install amazon-cloudwatch-agent

# Configure logging
sudo nano /opt/aws/amazon-cloudwatch-agent/etc/config.json
```

### Prometheus + Grafana

```bash
# Start monitoring stack
docker-compose -f docker-compose-monitoring.yml up -d

# Access Grafana: http://localhost:3000
# Default: admin/admin
```

---

## SSL/TLS Certificates

### Render
- Automatic SSL certificates
- No configuration needed

### AWS EC2 with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Database Migration

### Backup Neon Database

```bash
# Export data
pg_dump $DATABASE_URL > backup.sql

# Import to new database
psql $NEW_DATABASE_URL < backup.sql
```

---

## Performance Optimization

### 1. Enable Caching

```python
# Add Redis caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def predict_cached(features_hash):
    return model.predict(features)
```

### 2. Use Gunicorn

```bash
# Install
pip install gunicorn

# Run with workers
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. Database Connection Pooling

```python
# In api/main.py
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

---

## Troubleshooting Deployment

### Issue: Model Not Found

**Solution**: Ensure model files are in repository
```bash
git add models/*.joblib
git commit -m "Add model files"
git push
```

### Issue: Database Connection Failed

**Solution**: Check DATABASE_URL format
```
postgresql://user:pass@host:5432/db?sslmode=require
```

### Issue: Port Already in Use

**Solution**: Use $PORT environment variable
```python
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## Post-Deployment Checklist

- [ ] Backend health check returns 200
- [ ] Frontend loads successfully
- [ ] Prediction endpoint works
- [ ] Database connection successful
- [ ] Environment variables set
- [ ] SSL certificate active
- [ ] Monitoring enabled
- [ ] Logs accessible
- [ ] Auto-deployment configured
- [ ] Backup strategy in place

---

## Cost Estimation

### Render (Free Tier)
- **Backend**: Free (with spin down)
- **Frontend**: Free (with spin down)
- **Total**: $0/month

### Render (Paid)
- **Backend**: $7/month (always on)
- **Frontend**: $7/month (always on)
- **Total**: $14/month

### AWS
- **EC2 t2.micro**: Free tier (1 year), then $8/month
- **RDS**: $15/month (if not using Neon)
- **Total**: $8-23/month

### Google Cloud
- **Cloud Run**: Pay per request (~$5-10/month)
- **Total**: $5-10/month

---

## Support

- **Render Docs**: https://render.com/docs
- **AWS Docs**: https://docs.aws.amazon.com
- **GitHub Issues**: [Report Issue](https://github.com/ganapathi-ai/Employment_burnout_prediction/issues)
