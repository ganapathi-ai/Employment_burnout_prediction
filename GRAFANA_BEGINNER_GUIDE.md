# Grafana Complete Beginner's Guide

## 📚 What is Grafana?

**Grafana** is a visualization tool that creates beautiful dashboards to monitor your API in real-time.

**Think of it as:** A TV screen showing live stats of your API (like how many requests, how fast, any errors)

---

## 🎯 What You'll Monitor

1. **Request Count** - How many people are using your API
2. **Response Time** - How fast your API responds
3. **Errors** - If anything goes wrong

---

## 🚀 Step-by-Step Setup (Windows)

### Step 1: Install Docker Desktop

**Why?** Grafana runs in Docker (a container)

1. Download Docker Desktop:
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - Install and restart computer

2. Verify Docker is running:
   ```cmd
   docker --version
   ```
   Should show: `Docker version 24.x.x`

---

### Step 2: Start Monitoring Stack

**What this does:** Starts Prometheus (collects metrics) + Grafana (shows dashboards)

```cmd
# Navigate to your project
cd c:\Users\lenovo\Documents\Employers_Burnout_prediction

# Start everything
docker-compose up -d
```

**Expected output:**
```
Creating network "burnout_monitoring"
Creating prometheus ... done
Creating grafana    ... done
```

**Check if running:**
```cmd
docker ps
```

Should show 2 containers running:
- `prometheus`
- `grafana`

---

### Step 3: Access Grafana

1. **Open browser**
2. **Go to:** http://localhost:3000
3. **Login:**
   - Username: `admin`
   - Password: `admin`
4. **Skip password change** (or set new password)

**You're in!** 🎉

---

### Step 4: Add Prometheus Data Source

**What this does:** Connects Grafana to Prometheus (where metrics are stored)

1. **Click** left sidebar → ⚙️ **Configuration** → **Data Sources**
2. **Click** "Add data source"
3. **Select** "Prometheus"
4. **Configure:**
   - Name: `Prometheus`
   - URL: `http://prometheus:9090`
5. **Click** "Save & Test"
6. **Should see:** ✅ "Data source is working"

---

### Step 5: Import Dashboards

**Option A: Import from File (Recommended)**

1. **Click** left sidebar → ➕ **Create** → **Import**
2. **Click** "Upload JSON file"
3. **Select:** `monitoring/grafana_dashboards.json`
4. **Click** "Load"
5. **Select** Data Source: `Prometheus`
6. **Click** "Import"

**Option B: Create Manually (See below)**

---

### Step 6: View Your Dashboards

1. **Click** left sidebar → 📊 **Dashboards**
2. **You'll see 3 dashboards:**
   - Burnout API - Request Count
   - Burnout API - Latency & Performance
   - Burnout API - Errors & Health

3. **Click any dashboard** to view

---

## 📊 Understanding Your Dashboards

### Dashboard 1: Request Count

**What it shows:**
- Total requests per second
- Requests by endpoint (/predict, /health)
- Request rate over time

**How to read:**
- Higher numbers = More people using your API ✅
- Sudden drops = Something might be wrong ⚠️

**Example:**
```
Total Requests: 150/sec
/predict: 120/sec
/health: 30/sec
```

---

### Dashboard 2: Latency & Performance

**What it shows:**
- Average response time (how fast)
- P95 response time (95% of requests faster than this)
- P99 response time (99% of requests faster than this)

**How to read:**
- Lower is better (faster API)
- Average < 200ms = Excellent ✅
- Average > 1000ms = Slow ⚠️

**Example:**
```
Average: 145ms ✅ (Good!)
P95: 250ms ✅ (Good!)
P99: 500ms ⚠️ (Some slow requests)
```

---

### Dashboard 3: Errors & Health

**What it shows:**
- Error rate (% of failed requests)
- 4xx errors (client errors - bad requests)
- 5xx errors (server errors - your API crashed)
- API health status (UP/DOWN)

**How to read:**
- Error rate < 1% = Excellent ✅
- Error rate > 5% = Problem ⚠️
- API Status UP = Working ✅

**Example:**
```
Error Rate: 0.5% ✅ (Excellent!)
4xx Errors: 2/sec (Users sending bad data)
5xx Errors: 0/sec ✅ (No crashes!)
API Status: UP ✅
```

---

## 🎨 Creating Your First Dashboard (Manual)

### Step 1: Create New Dashboard

1. **Click** ➕ **Create** → **Dashboard**
2. **Click** "Add new panel"

### Step 2: Add Request Count Panel

1. **In Query section:**
   - Data source: `Prometheus`
   - Metric: `rate(http_requests_total[5m])`
   - Legend: `{{endpoint}}`

2. **In Panel options:**
   - Title: "API Requests"
   - Description: "Requests per second"

3. **Click** "Apply"

### Step 3: Add Response Time Panel

1. **Click** "Add panel"
2. **In Query section:**
   - Metric: `avg(http_request_duration_seconds)`
   - Legend: "Average Response Time"

3. **In Panel options:**
   - Title: "Response Time"
   - Unit: "seconds (s)"

4. **Click** "Apply"

### Step 4: Save Dashboard

1. **Click** 💾 **Save dashboard** (top right)
2. **Name:** "My First Dashboard"
3. **Click** "Save"

---

## 🔧 Common Tasks

### View Live Data

1. **Open any dashboard**
2. **Top right:** Set refresh to "5s" (refreshes every 5 seconds)
3. **Watch numbers update in real-time!**

### Change Time Range

1. **Top right:** Click time range (e.g., "Last 6 hours")
2. **Select:** "Last 15 minutes" or "Last 1 hour"
3. **Click** "Apply"

### Zoom In on Graph

1. **Click and drag** on any graph
2. **Zooms to selected time range**
3. **Click** "Zoom out" to reset

### Export Dashboard

1. **Open dashboard**
2. **Click** ⚙️ (top right) → **JSON Model**
3. **Copy JSON**
4. **Save to file**

---

## 🐛 Troubleshooting

### Problem: Can't access http://localhost:3000

**Solution:**
```cmd
# Check if Grafana is running
docker ps

# If not running, start it
docker-compose up -d

# Check logs
docker logs grafana
```

### Problem: "Data source is not working"

**Solution:**
1. Check Prometheus URL: `http://prometheus:9090`
2. Verify Prometheus is running:
   ```cmd
   docker ps | findstr prometheus
   ```
3. Test Prometheus directly: http://localhost:9090

### Problem: No data in dashboards

**Solution:**
1. **Make API requests** to generate data:
   ```cmd
   python verify_api.py
   ```
2. **Wait 30 seconds** for metrics to appear
3. **Refresh dashboard**

### Problem: Dashboard shows "No data"

**Solution:**
1. Check time range (top right)
2. Change to "Last 5 minutes"
3. Make sure API is running:
   ```cmd
   python api/main.py
   ```

---

## 📱 Mobile Access

### Access from Phone/Tablet

1. **Find your computer's IP:**
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. **On mobile browser:**
   ```
   http://192.168.1.100:3000
   ```

3. **Login** with same credentials

---

## 🎓 Advanced Features

### Set Up Alerts

1. **Open dashboard panel**
2. **Click** panel title → **Edit**
3. **Click** 🔔 **Alert** tab
4. **Create alert rule:**
   - Name: "High Error Rate"
   - Condition: `WHEN avg() OF query(A, 5m) IS ABOVE 0.05`
   - Send to: Email/Slack

5. **Save**

### Create Variables

**Use case:** Switch between different APIs

1. **Dashboard settings** → **Variables**
2. **Add variable:**
   - Name: `api`
   - Type: `Query`
   - Query: `label_values(http_requests_total, job)`

3. **Use in queries:** `http_requests_total{job="$api"}`

### Share Dashboard

1. **Click** 🔗 **Share** (top right)
2. **Options:**
   - **Link:** Copy URL
   - **Snapshot:** Create public snapshot
   - **Export:** Download JSON

---

## 📊 Sample Queries

### Total Requests
```
sum(rate(http_requests_total[5m]))
```

### Requests by Endpoint
```
sum by (endpoint) (rate(http_requests_total[5m]))
```

### Average Response Time
```
avg(http_request_duration_seconds)
```

### Error Rate
```
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
```

### P95 Latency
```
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## 🎯 Quick Reference

### URLs
- **Grafana:** http://localhost:3000
- **Prometheus:** http://localhost:9090
- **API:** http://localhost:8000

### Default Credentials
- **Username:** admin
- **Password:** admin

### Docker Commands
```cmd
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker logs grafana
docker logs prometheus

# Restart
docker-compose restart
```

---

## 📚 Next Steps

1. ✅ **Setup complete** - You have Grafana running
2. ✅ **Import dashboards** - Use provided JSON
3. ✅ **View metrics** - See your API stats
4. 📖 **Learn more** - Explore Grafana docs
5. 🎨 **Customize** - Create your own panels

---

## 🔗 Resources

- **Grafana Docs:** https://grafana.com/docs/
- **Prometheus Docs:** https://prometheus.io/docs/
- **Dashboard Examples:** https://grafana.com/grafana/dashboards/

---

## ✅ Checklist

- [ ] Docker Desktop installed
- [ ] `docker-compose up -d` executed
- [ ] Grafana accessible at http://localhost:3000
- [ ] Prometheus data source added
- [ ] Dashboards imported
- [ ] Can see metrics in dashboards
- [ ] API is running and generating data

---

**Need Help?** Check troubleshooting section or ask!

**Last Updated:** 2024-02-14
