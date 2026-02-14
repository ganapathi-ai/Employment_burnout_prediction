# Weights & Biases Integration Guide

## Overview
This project uses **Weights & Biases (W&B)** for ML experiment tracking, live monitoring, and model versioning.

---

## Setup

### 1. Install W&B
```bash
pip install wandb
```

### 2. Login to W&B
```bash
wandb login
```
Enter your API key from: https://wandb.ai/authorize

### 3. Set Environment Variables
Add to `.env`:
```bash
WANDB_API_KEY=your_api_key_here
WANDB_ENTITY=kakarlagana18-iihmr
ENABLE_WANDB=true
```

---

## Features Tracked

### 🎯 Model Training (`scripts/train_model.py`)

**Metrics Logged:**
- Model comparison (RandomForest, GradientBoosting, XGBoost)
- Accuracy, ROC-AUC for each model
- Confusion matrix (TP, FP, TN, FN)
- Precision, Recall, F1-score
- Best model selection

**Visualizations:**
- Confusion Matrix heatmap
- ROC Curve
- Precision-Recall Curve
- Feature Importance bar chart

**Artifacts:**
- Trained model (`best_model.joblib`)
- Preprocessor/Scaler (`preprocessor.joblib`)
- Feature names (`feature_names.joblib`)

**Run Training:**
```bash
python scripts/train_model.py
```

**View Results:**
- Project: `burnout-prediction`
- Dashboard: https://wandb.ai/kakarlagana18-iihmr/burnout-prediction

---

### 📊 Live API Monitoring (`scripts/wandb_monitor.py`)

**Real-time Metrics:**
- Prediction count
- Risk level distribution (High/Low)
- Risk probability distribution
- Response time (ms)
- Error rate

**Input Features Tracked:**
- work_hours, screen_time_hours, meetings_count
- breaks_taken, sleep_hours, task_completion_rate

**Engineered Features Tracked:**
- work_intensity_ratio, meeting_burden
- recovery_index, fatigue_risk
- work_life_balance_score
- high_workload_flag, poor_recovery_flag

**System Health:**
- API health status
- Model loaded status
- Error types and counts

**View Live Dashboard:**
- Project: `burnout-prediction-live`
- Dashboard: https://wandb.ai/kakarlagana18-iihmr/burnout-prediction-live

---

## Usage Examples

### Example 1: Track Model Training
```python
import wandb
from scripts.train_model import train_model

# Train with W&B tracking
model, scaler, features = train_model()

# View results at:
# https://wandb.ai/kakarlagana18-iihmr/burnout-prediction
```

### Example 2: Monitor Live Predictions
```python
from scripts.wandb_monitor import monitor
import time

# Log prediction
start = time.time()
result = api_predict(user_data)
response_time = (time.time() - start) * 1000

monitor.log_prediction(user_data, result, response_time)
```

### Example 3: Custom Experiment
```python
import wandb

run = wandb.init(
    entity="kakarlagana18-iihmr",
    project="burnout-prediction",
    config={
        "learning_rate": 0.01,
        "n_estimators": 200,
        "max_depth": 15
    }
)

# Train model
for epoch in range(10):
    # Your training code
    wandb.log({"loss": loss, "accuracy": acc})

run.finish()
```

---

## W&B Dashboard Features

### 1. Training Dashboard
**URL:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction

**Panels:**
- Model comparison table (Accuracy, ROC-AUC)
- Confusion matrix visualization
- ROC curve comparison
- Feature importance ranking
- Training hyperparameters
- Model artifacts download

### 2. Live Monitoring Dashboard
**URL:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction-live

**Panels:**
- Real-time prediction count
- Risk level distribution (pie chart)
- Average risk probability (line chart)
- Response time histogram
- Error rate over time
- Feature distribution heatmaps
- System health indicators

### 3. Custom Reports
Create custom reports with:
- Model performance comparison
- Feature correlation analysis
- Prediction trends over time
- A/B testing results

---

## What You Can Track

### ✅ Model Training
- [x] Dataset statistics (size, class distribution)
- [x] Model hyperparameters
- [x] Training metrics (accuracy, loss, ROC-AUC)
- [x] Validation metrics
- [x] Confusion matrix
- [x] ROC curve
- [x] Precision-Recall curve
- [x] Feature importance
- [x] Model artifacts (saved models)
- [x] Training time
- [x] Best model selection

### ✅ Live Predictions
- [x] Prediction count
- [x] Risk level distribution
- [x] Risk probability distribution
- [x] Response time
- [x] Input feature distributions
- [x] Engineered feature values
- [x] Error rate and types
- [x] API health status

### ✅ System Monitoring
- [x] API uptime
- [x] Model load status
- [x] Database connection status
- [x] Request rate
- [x] Error logs

---

## Advanced Features

### 1. Model Versioning
```python
# Save model as artifact
artifact = wandb.Artifact('burnout-model', type='model')
artifact.add_file('models/best_model.joblib')
wandb.log_artifact(artifact)

# Load specific version
artifact = run.use_artifact('burnout-model:v3')
artifact.download()
```

### 2. Hyperparameter Sweeps
```python
sweep_config = {
    'method': 'bayes',
    'metric': {'name': 'roc_auc', 'goal': 'maximize'},
    'parameters': {
        'n_estimators': {'values': [50, 100, 200]},
        'max_depth': {'values': [5, 10, 15]},
        'learning_rate': {'min': 0.01, 'max': 0.3}
    }
}

sweep_id = wandb.sweep(sweep_config, project="burnout-prediction")
wandb.agent(sweep_id, function=train_model)
```

### 3. Alerts
Set up alerts for:
- Model accuracy drops below threshold
- Error rate exceeds limit
- Response time too high
- High burnout risk spike

### 4. Team Collaboration
- Share dashboards with team
- Comment on runs
- Compare experiments
- Track model lineage

---

## Environment Variables

```bash
# Required
WANDB_API_KEY=your_api_key_here
WANDB_ENTITY=kakarlagana18-iihmr

# Optional
ENABLE_WANDB=true                    # Enable/disable W&B
WANDB_MODE=online                    # online/offline/disabled
WANDB_PROJECT=burnout-prediction     # Project name
WANDB_TAGS=production,v2             # Custom tags
```

---

## Render Deployment

Add to Render environment variables:
```
WANDB_API_KEY=your_api_key_here
WANDB_ENTITY=kakarlagana18-iihmr
ENABLE_WANDB=true
```

---

## Troubleshooting

### Issue: W&B not logging
**Solution:**
```bash
# Check API key
echo $WANDB_API_KEY

# Re-login
wandb login --relogin

# Test connection
python -c "import wandb; wandb.init(project='test')"
```

### Issue: Offline mode
**Solution:**
```bash
# Sync offline runs
wandb sync wandb/offline-run-*
```

### Issue: Too many logs
**Solution:**
```python
# Log less frequently
if step % 10 == 0:
    wandb.log({"metric": value})
```

---

## Best Practices

1. **Use meaningful run names**
   ```python
   wandb.init(name=f"rf-{n_estimators}-{datetime.now()}")
   ```

2. **Tag runs appropriately**
   ```python
   wandb.init(tags=["production", "v2", "optimized"])
   ```

3. **Log hyperparameters**
   ```python
   wandb.config.update({"lr": 0.01, "batch_size": 32})
   ```

4. **Save artifacts**
   ```python
   wandb.save("models/*.joblib")
   ```

5. **Create reports**
   - Document experiments
   - Share findings
   - Track progress

---

## Resources

- **W&B Docs:** https://docs.wandb.ai/
- **Your Dashboard:** https://wandb.ai/kakarlagana18-iihmr
- **API Reference:** https://docs.wandb.ai/ref/python
- **Examples:** https://github.com/wandb/examples

---

## Quick Commands

```bash
# Login
wandb login

# List projects
wandb projects

# List runs
wandb runs kakarlagana18-iihmr/burnout-prediction

# Pull artifact
wandb artifact get kakarlagana18-iihmr/burnout-prediction/burnout-model:latest

# Sync offline runs
wandb sync wandb/offline-run-*

# Disable W&B
export WANDB_MODE=disabled
```

---

**Built with ❤️ using Weights & Biases for ML tracking**
