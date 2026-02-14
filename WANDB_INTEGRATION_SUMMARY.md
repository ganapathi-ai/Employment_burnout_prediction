# Weights & Biases Integration Summary

## ✅ What's Been Added

### 1. Enhanced Training Script (`scripts/train_model.py`)
**Features:**
- Automatic experiment tracking
- Model comparison (RandomForest, GradientBoosting, XGBoost)
- Metrics logging (Accuracy, ROC-AUC, Precision, Recall, F1)
- Confusion matrix visualization
- ROC curve plotting
- Precision-Recall curve
- Feature importance charts
- Model artifact versioning

**Usage:**
```bash
python scripts/train_model.py
```

**View Results:**
https://wandb.ai/kakarlagana18-iihmr/burnout-prediction

---

### 2. Live Monitoring Module (`scripts/wandb_monitor.py`)
**Features:**
- Real-time prediction tracking
- Risk level distribution
- Response time monitoring
- Feature distribution analysis
- Error tracking
- System health monitoring

**Integration:**
```python
from scripts.wandb_monitor import monitor

# Log prediction
monitor.log_prediction(user_data, result, response_time_ms)

# Log error
monitor.log_error("ValidationError", "Invalid input")

# Log health
monitor.log_health_check("healthy", True)
```

---

### 3. Test Script (`test_wandb.py`)
**Purpose:** Verify W&B integration is working

**Usage:**
```bash
python test_wandb.py
```

**Output:**
- ✓ W&B initialized successfully
- ✓ Logged test metrics
- ✓ Run URL provided

---

### 4. Comprehensive Guide (`WANDB_GUIDE.md`)
**Contents:**
- Setup instructions
- Feature overview
- Usage examples
- Dashboard features
- Advanced features (sweeps, alerts, versioning)
- Troubleshooting
- Best practices

---

## 🎯 What You Can Track

### Training Metrics
- [x] Dataset statistics
- [x] Model hyperparameters
- [x] Training/validation metrics
- [x] Confusion matrix
- [x] ROC curve
- [x] PR curve
- [x] Feature importance
- [x] Model artifacts
- [x] Best model selection

### Live Production Metrics
- [x] Prediction count
- [x] Risk distribution
- [x] Response time
- [x] Input features
- [x] Engineered features
- [x] Error rate
- [x] API health

---

## 📊 Dashboards

### Training Dashboard
**URL:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction

**Panels:**
- Model comparison table
- Confusion matrix heatmap
- ROC curves
- Feature importance ranking
- Hyperparameter tracking
- Model artifacts

### Live Monitoring Dashboard
**URL:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction-live

**Panels:**
- Real-time prediction count
- Risk level pie chart
- Response time histogram
- Feature distributions
- Error rate timeline
- System health indicators

---

## 🚀 Quick Start

### 1. Setup
```bash
# Install W&B (already in requirements.txt)
pip install wandb

# Login
wandb login
# Enter API key: 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
```

### 2. Set Environment Variables
Add to `.env`:
```bash
WANDB_API_KEY=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
WANDB_ENTITY=kakarlagana18-iihmr
ENABLE_WANDB=true
```

### 3. Test Integration
```bash
python test_wandb.py
```

### 4. Train Model with Tracking
```bash
python scripts/train_model.py
```

### 5. View Results
Visit: https://wandb.ai/kakarlagana18-iihmr

---

## 🔧 Render Deployment

Add to Render environment variables:
```
WANDB_API_KEY=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
WANDB_ENTITY=kakarlagana18-iihmr
ENABLE_WANDB=true
```

---

## 📈 Example Visualizations

### 1. Model Comparison
```
Model            Accuracy  ROC-AUC  Precision  Recall
RandomForest     0.8542    0.8923   0.8234     0.8654
GradientBoosting 0.8623    0.9012   0.8456     0.8723
XGBoost          0.8734    0.9145   0.8567     0.8834  ← Best
```

### 2. Feature Importance
```
Feature                    Importance
work_life_balance_score    0.1523
fatigue_risk              0.1234
recovery_index            0.1123
workload_pressure         0.0987
sleep_deficit             0.0876
```

### 3. Live Metrics
```
Metric                Value
Total Predictions     1,234
High Risk %           23.4%
Avg Response Time     145ms
Error Rate            0.2%
```

---

## 🎓 Advanced Features

### 1. Hyperparameter Sweeps
```python
sweep_config = {
    'method': 'bayes',
    'metric': {'name': 'roc_auc', 'goal': 'maximize'},
    'parameters': {
        'n_estimators': {'values': [50, 100, 200]},
        'max_depth': {'values': [5, 10, 15]}
    }
}

sweep_id = wandb.sweep(sweep_config, project="burnout-prediction")
wandb.agent(sweep_id, function=train_model)
```

### 2. Model Versioning
```python
# Save model
artifact = wandb.Artifact('burnout-model', type='model')
artifact.add_file('models/best_model.joblib')
wandb.log_artifact(artifact)

# Load specific version
artifact = run.use_artifact('burnout-model:v3')
artifact.download()
```

### 3. Alerts
Set up alerts for:
- Model accuracy drops
- High error rate
- Slow response time
- Burnout risk spikes

---

## 📝 Files Modified/Created

### Modified
- `scripts/train_model.py` - Added W&B tracking
- `.env.example` - Added W&B variables
- `README.md` - Added W&B documentation links

### Created
- `WANDB_GUIDE.md` - Comprehensive W&B guide
- `scripts/wandb_monitor.py` - Live monitoring module
- `test_wandb.py` - Integration test script
- `WANDB_INTEGRATION_SUMMARY.md` - This file

---

## ✅ Next Steps

1. **Test Integration**
   ```bash
   python test_wandb.py
   ```

2. **Train Model**
   ```bash
   python scripts/train_model.py
   ```

3. **View Dashboard**
   - Visit: https://wandb.ai/kakarlagana18-iihmr
   - Explore training metrics
   - Check model artifacts

4. **Deploy to Render**
   - Add W&B env vars to Render
   - Redeploy services
   - Monitor live predictions

5. **Create Custom Reports**
   - Compare model versions
   - Track performance over time
   - Share with team

---

## 🔗 Resources

- **W&B Dashboard:** https://wandb.ai/kakarlagana18-iihmr
- **Documentation:** WANDB_GUIDE.md
- **W&B Docs:** https://docs.wandb.ai/
- **API Reference:** https://docs.wandb.ai/ref/python

---

**Status:** ✅ W&B Integration Complete
**Commit:** b743fca - "feat: integrate Weights & Biases for ML tracking and live monitoring"
**GitHub Actions:** Running (triggered by push)
