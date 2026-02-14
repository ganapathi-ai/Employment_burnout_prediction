# 🔧 Troubleshooting Guide

Common issues and solutions for the Employee Burnout Prediction System.

## Installation Issues

### Issue: pip install fails
**Error**: `Could not find a version that satisfies the requirement`

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

### Issue: Python version mismatch
**Error**: `Python 3.9+ required`

**Solution**:
```bash
# Check version
python --version

# Install Python 3.9+
# Download from python.org
```

## Database Issues

### Issue: Database connection failed
**Error**: `could not connect to server`

**Solutions**:
1. Check DATABASE_URL in .env
2. Verify Neon database is active
3. Test connection:
```bash
python -c "from scripts.data_ingestion import PostgresDataStore; PostgresDataStore().test_connection()"
```

### Issue: SSL connection error
**Error**: `SSL SYSCALL error`

**Solution**:
Add `?sslmode=require` to DATABASE_URL:
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

## Model Issues

### Issue: Model file not found
**Error**: `FileNotFoundError: models/best_model.joblib`

**Solution**:
```bash
# Train model
python scripts/train_model.py

# Verify files exist
ls models/
```

### Issue: Model prediction fails
**Error**: `ValueError: X has 8 features but model expects 17`

**Solution**:
- Ensure feature engineering is applied
- Check engineer_features() function
- Retrain model if needed

## API Issues

### Issue: Port already in use
**Error**: `Address already in use: 8000`

**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue: CORS error
**Error**: `Access-Control-Allow-Origin`

**Solution**:
Check CORS configuration in api/main.py:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: 422 Validation Error
**Error**: `field required` or `value_error`

**Solution**:
- Check all required fields are provided
- Verify field types and ranges
- See [API.md](API.md) for field constraints

## Frontend Issues

### Issue: Streamlit won't start
**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install streamlit
```

### Issue: API connection timeout
**Error**: `Connection timeout`

**Solutions**:
1. Increase timeout in streamlit_app.py:
```python
response = requests.post(url, json=payload, timeout=120)
```

2. Check API is running:
```bash
curl http://localhost:8000/health
```

### Issue: Frontend shows wrong API URL
**Solution**:
Update .env:
```env
API_URL=http://localhost:8000
```

## Testing Issues

### Issue: Tests fail
**Error**: `AttributeError: module 'api.main' has no attribute 'model'`

**Solution**:
Update tests/conftest.py to use correct variable names (MODEL instead of model).

### Issue: Import errors in tests
**Solution**:
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # macOS/Linux
set PYTHONPATH=%PYTHONPATH%;%CD%          # Windows
```

## Deployment Issues

### Issue: Render deployment fails
**Error**: `Build failed`

**Solutions**:
1. Check Render logs
2. Verify requirements.txt
3. Ensure model files are in repo
4. Check environment variables

### Issue: Cold start timeout
**Error**: `Service unavailable`

**Solutions**:
1. Upgrade to paid tier (no cold starts)
2. Keep service warm with health checks
3. Optimize model loading

### Issue: Out of memory
**Error**: `MemoryError`

**Solutions**:
1. Upgrade instance type
2. Optimize model size
3. Use model compression

## W&B Issues

### Issue: W&B login fails
**Error**: `wandb: ERROR Unable to authenticate`

**Solution**:
```bash
# Login
wandb login

# Or set API key
export WANDB_API_KEY=your_key
```

### Issue: W&B run not logging
**Solution**:
Check WANDB_MODE in .env:
```env
WANDB_MODE=online  # not 'disabled'
```

## Performance Issues

### Issue: Slow predictions
**Solutions**:
1. Check model size
2. Optimize feature engineering
3. Use caching
4. Profile code:
```bash
python -m cProfile api/main.py
```

### Issue: High memory usage
**Solutions**:
1. Use model compression
2. Implement batch processing
3. Clear unused variables

## Git Issues

### Issue: Large files rejected
**Error**: `file exceeds GitHub's file size limit`

**Solution**:
```bash
# Add to .gitignore
echo "*.db" >> .gitignore
echo "wandb/" >> .gitignore

# Remove from git
git rm --cached file.db
git commit -m "Remove large files"
```

## Environment Issues

### Issue: .env file not loaded
**Solution**:
Ensure python-dotenv is installed and loaded:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Issue: Environment variables not set
**Solution**:
```bash
# Check if loaded
python -c "import os; print(os.getenv('DATABASE_URL'))"

# Set manually
export DATABASE_URL=postgresql://...  # macOS/Linux
set DATABASE_URL=postgresql://...     # Windows
```

## Docker Issues

### Issue: Docker build fails
**Solution**:
```bash
# Clean build
docker build --no-cache -t burnout-api .

# Check logs
docker logs <container_id>
```

### Issue: Container can't connect to host
**Solution**:
Use `host.docker.internal` instead of `localhost`:
```env
DATABASE_URL=postgresql://host.docker.internal:5432/db
```

## Common Error Messages

### "Model not loaded"
- Train model: `python scripts/train_model.py`
- Check model path in .env

### "Database table not found"
- Table is auto-created on first run
- Check database permissions

### "Feature mismatch"
- Retrain model
- Check feature engineering logic

### "Validation error"
- Check input data format
- See API.md for constraints

## Getting Help

1. **Check Documentation**:
   - [README.md](README.md)
   - [SETUP.md](SETUP.md)
   - [API.md](API.md)
   - [ARCHITECTURE.md](ARCHITECTURE.md)

2. **Search Issues**:
   - [GitHub Issues](https://github.com/ganapathi-ai/Employment_burnout_prediction/issues)

3. **Create New Issue**:
   - Provide error message
   - Include steps to reproduce
   - Share environment details

4. **Debug Mode**:
```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
python api/main.py
```

## Still Having Issues?

Open an issue on GitHub with:
- Error message
- Steps to reproduce
- Environment (OS, Python version)
- Relevant logs

---

**Most issues can be resolved by**:
1. Checking .env configuration
2. Retraining the model
3. Verifying dependencies
4. Reading error messages carefully
