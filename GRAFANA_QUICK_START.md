# 🚀 Quick Start - Grafana Setup

## ⚠️ Docker Desktop Not Running

You have Docker installed, but Docker Desktop needs to be started first.

---

## ✅ Step-by-Step (5 Minutes)

### Step 1: Start Docker Desktop

1. **Press Windows Key**
2. **Type:** "Docker Desktop"
3. **Click** Docker Desktop app
4. **Wait** for Docker to start (whale icon in system tray will stop animating)

**OR**

1. **Go to:** `C:\Program Files\Docker\Docker\Docker Desktop.exe`
2. **Double-click** to start

---

### Step 2: Verify Docker is Running

```cmd
docker ps
```

**Should show:** Empty list or running containers (not an error)

---

### Step 3: Start Grafana

**Option A: Double-click** `start_grafana.bat`

**Option B: Run in CMD:**
```cmd
cd c:\Users\lenovo\Documents\Employers_Burnout_prediction
docker-compose up -d
```

**Expected output:**
```
[+] Running 3/3
 ✔ Network employers_burnout_prediction_ml-network  Created
 ✔ Container burnout_prometheus                     Started
 ✔ Container burnout_grafana                        Started
```

---

### Step 4: Access Grafana

1. **Open browser:** http://localhost:3000
2. **Login:**
   - Username: `admin`
   - Password: `admin`
3. **Click "Skip"** on password change

**You're in!** 🎉

---

### Step 5: Add Data Source

1. **Click** ⚙️ (left sidebar) → **Data Sources**
2. **Click** "Add data source"
3. **Select** "Prometheus"
4. **URL:** `http://prometheus:9090`
5. **Click** "Save & Test"
6. **Should see:** ✅ "Data source is working"

---

### Step 6: Import Dashboards

1. **Click** ➕ (left sidebar) → **Import**
2. **Click** "Upload JSON file"
3. **Browse to:** `monitoring/grafana_dashboards.json`
4. **Click** "Load"
5. **Select** Prometheus data source
6. **Click** "Import"

**Done! You have 3 dashboards!** 📊

---

## 🎯 What You'll See

### Dashboard 1: Request Count
- Total API requests
- Requests per endpoint
- Request rate over time

### Dashboard 2: Latency
- Average response time
- P95 latency
- P99 latency

### Dashboard 3: Errors
- Error rate
- 4xx/5xx errors
- API health status

---

## 🔧 Common Commands

### Check if running:
```cmd
docker ps
```

### Stop Grafana:
```cmd
docker-compose down
```

### Restart:
```cmd
docker-compose restart
```

### View logs:
```cmd
docker logs grafana
docker logs prometheus
```

---

## 🐛 Troubleshooting

### Problem: "Docker Desktop is not running"

**Solution:**
1. Start Docker Desktop app
2. Wait for whale icon to stop animating
3. Try again

### Problem: "Port 3000 already in use"

**Solution:**
```cmd
# Stop any existing containers
docker-compose down

# Start again
docker-compose up -d
```

### Problem: Can't access localhost:3000

**Solution:**
```cmd
# Check if Grafana is running
docker ps | findstr grafana

# If not running, check logs
docker logs grafana

# Restart
docker-compose restart grafana
```

---

## ✅ Quick Checklist

- [ ] Docker Desktop started (whale icon in system tray)
- [ ] Run `docker ps` (no errors)
- [ ] Run `docker-compose up -d`
- [ ] Open http://localhost:3000
- [ ] Login (admin/admin)
- [ ] Add Prometheus data source
- [ ] Import dashboards
- [ ] View your metrics!

---

## 📊 URLs

- **Grafana:** http://localhost:3000
- **Prometheus:** http://localhost:9090
- **API:** http://localhost:8000

---

## 🎓 Next Steps

1. ✅ Start Docker Desktop
2. ✅ Run `docker-compose up -d`
3. ✅ Access Grafana
4. ✅ Import dashboards
5. 📊 View your API metrics!

---

**Need help?** See full guide: `GRAFANA_BEGINNER_GUIDE.md`
