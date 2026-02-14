# W&B Run Names Explained

## ❓ What Are Those Random Names?

### Before (Random Names)
- `honest-carnation-3`
- `darling-quiver-2`
- `attentive-ring-1`

These are **W&B's auto-generated run names** - random but not meaningful.

### After (Meaningful Names) ✅
- `training_3models_20260214_1149`
- `api_monitoring_20260214_1149`

Now names are **descriptive and include timestamps**!

---

## 🎯 Run Name Format

### Training Runs
```
Format: training_3models_YYYYMMDD_HHMM
Example: training_3models_20260214_1149

Meaning:
- training = Type of run
- 3models = Comparing 3 models (RF, GB, XGB)
- 20260214 = Date (Feb 14, 2026)
- 1149 = Time (11:49 AM)
```

### Monitoring Runs
```
Format: api_monitoring_YYYYMMDD_HHMM
Example: api_monitoring_20260214_1149

Meaning:
- api_monitoring = Live API tracking
- 20260214 = Date
- 1149 = Time
```

---

## 📊 Your Active Dashboards

### 1. Training Dashboard ✅
**URL:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction

**Latest Run:** `training_3models_20260214_1149`

**What It Shows:**
- Model comparison (RandomForest, GradientBoosting, XGBoost)
- Best model: RandomForest (98.89% accuracy)
- Feature importance ranking
- Confusion matrix
- Training metrics
- Model artifacts (downloadable)

**When It Updates:**
- Every time you run: `python scripts/train_model.py`

---

### 2. Live Monitoring Dashboard ✅
**URL:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction-live

**Latest Run:** `api_monitoring_20260214_1149`

**What It Shows:**
- Real-time prediction count
- Risk level distribution (High vs Low)
- Response times
- Feature patterns
- Error tracking

**When It Updates:**
- When API makes predictions (after enabling `ENABLE_WANDB=true`)
- Currently has sample data to demonstrate

---

## 🔍 Understanding Run Details

### Run Components

Each run has:
1. **Name** - Descriptive identifier (e.g., `training_3models_20260214_1149`)
2. **ID** - Unique hash (e.g., `q9zya8vv`)
3. **URL** - Direct link to run
4. **Tags** - Categories (e.g., `production`, `classification`)
5. **Notes** - Description of what the run does
6. **Config** - Hyperparameters and settings
7. **Metrics** - Logged values (accuracy, loss, etc.)
8. **Artifacts** - Saved files (models, data)

### Example Run Breakdown

```
Name: training_3models_20260214_1149
ID: q9zya8vv
URL: https://wandb.ai/kakarlagana18-iihmr/burnout-prediction/runs/q9zya8vv

Tags:
- burnout
- classification
- ensemble
- production

Notes:
"Training 3 models and selecting best based on ROC-AUC"

Config:
- dataset: work_from_home_burnout
- test_size: 0.2
- models: [RandomForest, GradientBoosting, XGBoost]
- n_estimators: 100
- features: 17

Metrics:
- RandomForest_accuracy: 0.9889
- RandomForest_roc_auc: 0.9779
- GradientBoosting_accuracy: 0.9750
- XGBoost_accuracy: 0.9833

Artifacts:
- burnout-model (best_model.joblib)
- preprocessor.joblib
- feature_names.joblib
```

---

## 🎓 How to Read Dashboard

### Training Dashboard

**Overview Tab:**
- See all training runs
- Compare metrics side-by-side
- Filter by tags, dates

**Run Page:**
- Detailed metrics for one run
- Charts and visualizations
- Logs and console output
- Downloadable artifacts

**Charts Tab:**
- Custom visualizations
- Compare multiple runs
- Track progress over time

### Live Monitoring Dashboard

**Overview:**
- Real-time prediction count
- Risk distribution pie chart
- Response time trends

**Metrics:**
- Average risk probability
- High risk percentage
- API performance

**Logs:**
- Individual predictions
- Error messages
- System health

---

## 🚀 Quick Actions

### View Latest Training
```
https://wandb.ai/kakarlagana18-iihmr/burnout-prediction
```
Click on: `training_3models_20260214_1149`

### View Live Monitoring
```
https://wandb.ai/kakarlagana18-iihmr/burnout-prediction-live
```
Click on: `api_monitoring_20260214_1149`

### Run New Training
```bash
python scripts/train_model.py
```
New run will appear with current timestamp

### Initialize Live Monitoring
```bash
python init_wandb_live.py
```
Creates project with sample data

---

## 📝 Customization

### Change Run Name Format

Edit `scripts/train_model.py`:
```python
name=f"training_3models_{timestamp}"  # Current

# Change to:
name=f"experiment_v2_{timestamp}"
name=f"rf_gb_xgb_{timestamp}"
name=f"burnout_model_{timestamp}"
```

### Add Custom Tags

```python
tags=["burnout", "classification", "ensemble", "production"]

# Add more:
tags=["v2.0", "optimized", "final"]
```

### Add Notes

```python
notes="Training 3 models and selecting best based on ROC-AUC"

# Make more detailed:
notes="Comparing RandomForest, GradientBoosting, and XGBoost on 1800 samples with 17 engineered features. Selecting best model based on ROC-AUC score."
```

---

## ✅ Summary

### Problem Solved
- ❌ Random names like "honest-carnation-3"
- ✅ Meaningful names like "training_3models_20260214_1149"

### 404 Error Fixed
- ❌ `burnout-prediction-live` didn't exist
- ✅ Created with sample data

### What You Get
- Clear, descriptive run names
- Timestamp for tracking
- Easy to find specific runs
- Professional dashboard

---

## 🔗 Quick Links

- **Training:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction
- **Monitoring:** https://wandb.ai/kakarlagana18-iihmr/burnout-prediction-live
- **Your Profile:** https://wandb.ai/kakarlagana18-iihmr

---

**Last Updated:** 2024-02-14
**Status:** All dashboards active with meaningful names ✅
