# 🔧 Troubleshooting Guide

Common issues and solutions for the Employee Burnout Prediction System.

## Quick Diagnostics

### System Health Check

```bash
# 1. Check Python version
python --version  # Should be 3.9+

# 2. Check virtual environment
which python  # Should point to venv

# 3. Check dependencies
pip list | grep fastapi
pip list | grep streamlit

# 4. Check environment variables
cat .env  # Verify DATABASE_URL, WANDB_API_KEY

# 5. Check model files
ls -lh models/  # Should see 3 .joblib files

# 6. Test database connection
python check_db_data.py

# 7. Test API
curl http://localhost:8000/health
```

---

## Installation Issues

### Issue 1: pip install fails

**Error**:
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions**:

```bash
# Solution 1: Upgrade pip
pip install --upgrade pip

# Solution 2: Use specific Python version
python3.9 -m pip install -r requirements.txt

# Solution 3: Install one by one
pip install fastapi uvicorn streamlit pandas numpy scikit-learn

# Solution 4: Clear cache
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

### Issue 2: psycopg2-binary installation fails (Windows)

**Error**:
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solutions**:

```bash
# Solution 1: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Solution 2: Use conda
conda install psycopg2

# Solution 3: Use pre-built wheel
pip install psycopg2-binary --only-binary :all:
```

### Issue 3: XGBoost installation fails

**Error**:
```
ERROR: Failed building wheel for xgboost
```

**Solutions**:

```bash
# Solution 1: Install from conda
conda install -c conda-forge xgboost

# Solution 2: Install pre-built wheel
pip install xgboost --no-cache-dir

# Solution 3: Skip XGBoost (use RF only)
# Comment out xgboost in requirements.txt
```

---

## Environment Issues

### Issue 4: Virtual environment not activating

**Error**:
```
'venv' is not recognized as an internal or external command
```

**Solutions**:

```bash
# Windows
# Solution 1: Use full path
.\venv\Scripts\activate

# Solution 2: Use PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# Solution 3: Use Command Prompt (not PowerShell)
venv\Scripts\activate.bat

# macOS/Linux
# Solution 1: Use source
source venv/bin/activate

# Solution 2: Use dot
. venv/bin/activate
```

### Issue 5: .env file not loading

**Error**:
```
KeyError: 'DATABASE_URL'
```

**Solutions**:

```bash
# Solution 1: Verify .env exists
ls -la .env

# Solution 2: Check .env format (no spaces around =)
# Wrong: DATABASE_URL = postgresql://...
# Right: DATABASE_URL=postgresql://...

# Solution 3: Load manually
export $(cat .env | xargs)  # Linux/Mac
# Or set in terminal:
export DATABASE_URL="postgresql://..."

# Solution 4: Check python-dotenv installed
pip install python-dotenv
```

---

## Database Issues

### Issue 6: Database connection failed

**Error**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions**:

```bash
# Solution 1: Check DATABASE_URL format
# Correct format:
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

# Solution 2: Test connection with psql
psql "postgresql://user:pass@host/db?sslmode=require"

# Solution 3: Check Neon database status
# Go to neon.tech dashboard
# Ensure database is not sleeping

# Solution 4: Verify SSL mode
# Add to DATABASE_URL: ?sslmode=require

# Solution 5: Check firewall
# Ensure port 5432 is not blocked
```

### Issue 7: SSL connection error

**Error**:
```
SSL SYSCALL error: EOF detected
```

**Solutions**:

```bash
# Solution 1: Add SSL parameters
DATABASE_URL=postgresql://...?sslmode=require&channel_binding=require

# Solution 2: Update psycopg2
pip install --upgrade psycopg2-binary

# Solution 3: Disable SSL (development only)
DATABASE_URL=postgresql://...?sslmode=disable
```

### Issue 8: Table does not exist

**Error**:
```
relation "user_requests" does not exist
```

**Solutions**:

```bash
# Solution 1: Run data ingestion script
python scripts/data_ingestion.py

# Solution 2: Create table manually
# In Neon SQL Editor, run:
CREATE TABLE user_requests (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR,
    name VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    -- ... other columns
);

# Solution 3: Check table name
# Verify in api/main.py: Table('user_requests', ...)
```

---

## Model Issues

### Issue 9: Model not found

**Error**:
```
FileNotFoundError: models/best_model.joblib
```

**Solutions**:

```bash
# Solution 1: Train model
python scripts/train_model.py

# Solution 2: Check current directory
pwd  # Should be in project root
cd Employment_burnout_prediction

# Solution 3: Verify model files
ls models/
# Should see: best_model.joblib, preprocessor.joblib, feature_names.joblib

# Solution 4: Check MODEL_PATH in .env
MODEL_PATH=models/best_model.joblib
```

### Issue 10: Model loading error

**Error**:
```
ValueError: could not convert string to float
```

**Solutions**:

```bash
# Solution 1: Retrain model with correct scikit-learn version
pip install scikit-learn==1.3.0
python scripts/train_model.py

# Solution 2: Check joblib version
pip install joblib==1.3.0

# Solution 3: Clear old model files
rm models/*.joblib
python scripts/train_model.py
```

### Issue 11: Feature mismatch

**Error**:
```
ValueError: X has 8 features, but model expects 17
```

**Solutions**:

```python
# Solution 1: Ensure feature engineering is applied
features_array, all_features = engineer_features(user_data)

# Solution 2: Check feature order
feature_names = joblib.load('models/feature_names.joblib')
print(feature_names)  # Should have 17 features

# Solution 3: Retrain model
python scripts/train_model.py
```

---

## API Issues

### Issue 12: Port already in use

**Error**:
```
OSError: [Errno 48] Address already in use
```

**Solutions**:

```bash
# Solution 1: Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Solution 2: Use different port
uvicorn api.main:app --port 8001

# Solution 3: Find and stop uvicorn
ps aux | grep uvicorn
kill <PID>
```

### Issue 13: API returns 503

**Error**:
```
{"detail": "Model not loaded"}
```

**Solutions**:

```bash
# Solution 1: Check model files exist
ls models/

# Solution 2: Check API logs
# Look for "Model loaded successfully" message

# Solution 3: Restart API
# Stop (Ctrl+C) and restart:
python api/main.py

# Solution 4: Check MODEL_LOADED metric
curl http://localhost:8000/metrics | grep model_loaded
# Should show: model_loaded 1.0
```

### Issue 14: CORS error

**Error**:
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Solutions**:

```python
# Solution 1: Check CORS middleware in api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be "*" for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Solution 2: Restart API after changes

# Solution 3: Use proxy (production)
# Configure nginx or similar
```

---

## Frontend Issues

### Issue 15: Streamlit not starting

**Error**:
```
streamlit: command not found
```

**Solutions**:

```bash
# Solution 1: Ensure virtual environment activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Solution 2: Install streamlit
pip install streamlit

# Solution 3: Use python -m
python -m streamlit run frontend/streamlit_app.py

# Solution 4: Check PATH
which streamlit  # Should point to venv
```

### Issue 16: Frontend can't connect to API

**Error**:
```
ConnectionError: Cannot connect to API at http://localhost:8000
```

**Solutions**:

```bash
# Solution 1: Ensure backend is running
curl http://localhost:8000/health

# Solution 2: Check API_URL in .env
API_URL=http://localhost:8000

# Solution 3: Check firewall
# Ensure localhost connections allowed

# Solution 4: Use 127.0.0.1 instead of localhost
API_URL=http://127.0.0.1:8000
```

### Issue 17: Streamlit shows "Connection error"

**Error**:
```
Unable to connect to Streamlit server
```

**Solutions**:

```bash
# Solution 1: Clear Streamlit cache
streamlit cache clear

# Solution 2: Use different port
streamlit run frontend/streamlit_app.py --server.port 8502

# Solution 3: Check .streamlit/config.toml
[server]
port = 8501
address = "0.0.0.0"

# Solution 4: Restart Streamlit
# Stop (Ctrl+C) and restart
```

---

## Testing Issues

### Issue 18: Tests failing

**Error**:
```
FAILED tests/test_comprehensive.py::test_predict_endpoint
```

**Solutions**:

```bash
# Solution 1: Ensure model is trained
python scripts/train_model.py

# Solution 2: Check test database
# Use separate test database or mock

# Solution 3: Run tests with verbose output
pytest tests/ -vv -s

# Solution 4: Run single test
pytest tests/test_comprehensive.py::test_health_check -v

# Solution 5: Check test fixtures
# Verify conftest.py is correct
```

### Issue 19: Import errors in tests

**Error**:
```
ModuleNotFoundError: No module named 'api'
```

**Solutions**:

```bash
# Solution 1: Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Solution 2: Install in editable mode
pip install -e .

# Solution 3: Run from project root
cd Employment_burnout_prediction
pytest tests/

# Solution 4: Add __init__.py files
touch api/__init__.py
touch frontend/__init__.py
```

---

## Deployment Issues

### Issue 20: Render deployment fails

**Error**:
```
Build failed: requirements.txt not found
```

**Solutions**:

```bash
# Solution 1: Ensure requirements.txt in root
ls requirements.txt

# Solution 2: Check render.yaml
# Verify buildCommand: pip install -r requirements.txt

# Solution 3: Check branch
# Ensure deploying from correct branch (main)

# Solution 4: Check Render logs
# Go to Render dashboard → Logs
```

### Issue 21: Environment variables not set

**Error**:
```
KeyError: 'DATABASE_URL' in production
```

**Solutions**:

```bash
# Solution 1: Add env vars in Render dashboard
# Go to Environment → Add Environment Variable

# Solution 2: Check render.yaml
envVars:
  - key: DATABASE_URL
    sync: false

# Solution 3: Use Render secrets
# Store sensitive data in Render secrets

# Solution 4: Verify env vars loaded
# Add logging: print(os.getenv('DATABASE_URL'))
```

---

## Performance Issues

### Issue 22: Slow predictions

**Symptom**: Predictions take >1 second

**Solutions**:

```python
# Solution 1: Profile code
import cProfile
cProfile.run('predict(user_data)')

# Solution 2: Cache model
# Model should be loaded once at startup, not per request

# Solution 3: Optimize feature engineering
# Use numpy operations instead of loops

# Solution 4: Use connection pooling
engine = create_engine(DATABASE_URL, pool_size=10)

# Solution 5: Add caching
from functools import lru_cache
@lru_cache(maxsize=1000)
def predict_cached(features_hash):
    return model.predict(features)
```

### Issue 23: High memory usage

**Symptom**: API uses >500 MB RAM

**Solutions**:

```python
# Solution 1: Use smaller model
# Train with fewer trees: n_estimators=50

# Solution 2: Reduce batch size
# Process predictions one at a time

# Solution 3: Clear cache periodically
import gc
gc.collect()

# Solution 4: Use model compression
# Quantize model weights
```

---

## W&B Issues

### Issue 24: W&B login fails

**Error**:
```
wandb: ERROR Unable to authenticate
```

**Solutions**:

```bash
# Solution 1: Re-login
wandb login --relogin

# Solution 2: Set API key manually
export WANDB_API_KEY=your_key

# Solution 3: Disable W&B
# In .env: ENABLE_WANDB=false

# Solution 4: Check API key
# Go to wandb.ai → Settings → API Keys
```

### Issue 25: W&B not logging

**Symptom**: No data in W&B dashboard

**Solutions**:

```python
# Solution 1: Check wandb.init()
run = wandb.init(project="burnout-prediction")

# Solution 2: Verify logging
wandb.log({"accuracy": 0.98})

# Solution 3: Check internet connection
# W&B requires internet to sync

# Solution 4: Force sync
wandb.finish()
```

---

## Docker Issues

### Issue 26: Docker build fails

**Error**:
```
ERROR: failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete successfully
```

**Solutions**:

```bash
# Solution 1: Clear Docker cache
docker system prune -a

# Solution 2: Build with no cache
docker build --no-cache -t burnout-api .

# Solution 3: Check Dockerfile
# Ensure COPY requirements.txt before RUN pip install

# Solution 4: Use multi-stage build
# Separate build and runtime stages
```

### Issue 27: Docker container exits immediately

**Error**:
```
Container exited with code 1
```

**Solutions**:

```bash
# Solution 1: Check logs
docker logs <container_id>

# Solution 2: Run interactively
docker run -it burnout-api /bin/bash

# Solution 3: Check CMD in Dockerfile
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Solution 4: Verify model files in image
docker run burnout-api ls models/
```

---

## General Debugging Tips

### Enable Debug Logging

```python
# In api/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check System Resources

```bash
# CPU usage
top

# Memory usage
free -h

# Disk space
df -h

# Network connections
netstat -an | grep 8000
```

### Use Python Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use ipdb
import ipdb; ipdb.set_trace()
```

### Check Logs

```bash
# API logs
tail -f logs/api.log

# Streamlit logs
tail -f ~/.streamlit/logs/

# System logs
journalctl -u burnout-api -f
```

---

## Getting Help

### Before Asking for Help

1. ✅ Check this troubleshooting guide
2. ✅ Search GitHub issues
3. ✅ Check API logs
4. ✅ Verify environment variables
5. ✅ Test with minimal example

### Where to Get Help

- **GitHub Issues**: [Report Bug](https://github.com/ganapathi-ai/Employment_burnout_prediction/issues)
- **Documentation**: Check other docs in `docs/` folder
- **API Docs**: http://localhost:8000/docs
- **Stack Overflow**: Tag with `fastapi`, `streamlit`, `scikit-learn`

### Information to Include

When reporting issues, include:
- Operating system and version
- Python version
- Error message (full traceback)
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs
- Environment variables (redact secrets)

---

## Preventive Measures

### Regular Maintenance

```bash
# Update dependencies monthly
pip list --outdated
pip install --upgrade <package>

# Clean up
pip cache purge
docker system prune

# Backup database
pg_dump $DATABASE_URL > backup.sql

# Monitor logs
tail -f logs/*.log
```

### Best Practices

1. **Use virtual environments** (always)
2. **Pin dependency versions** (requirements.txt)
3. **Test before deploying** (run tests)
4. **Monitor metrics** (Prometheus)
5. **Keep backups** (database, models)
6. **Document changes** (CHANGELOG.md)
7. **Use version control** (git)
8. **Review logs regularly** (daily)
