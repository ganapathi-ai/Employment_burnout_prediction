# 🤖 Machine Learning Model Documentation

Complete guide to the ML model, training process, and feature engineering.

## Model Overview

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 98.89%
- **ROC-AUC**: 97.79%
- **Inference Time**: <50ms
- **Input Features**: 17 (8 raw + 9 engineered)
- **Output**: Binary classification (High Risk / Low Risk)

## Problem Statement

**Goal**: Predict employee burnout risk based on work-from-home behavioral metrics.

**Business Value**:
- Early detection of burnout risk
- Personalized recommendations
- Improved employee well-being
- Reduced turnover costs

## Dataset

### Source
- **Name**: Work From Home Burnout Dataset
- **Size**: 22,750 samples
- **Features**: 8 input features + 2 target variables
- **Format**: CSV

### Features Description

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| work_hours | float | 0-24 | Daily work hours |
| screen_time_hours | float | 0-24 | Screen time in hours |
| meetings_count | int | 0-20 | Number of meetings per day |
| breaks_taken | int | 0-10 | Number of breaks |
| after_hours_work | int | 0-1 | After-hours work (0=No, 1=Yes) |
| sleep_hours | float | 0-12 | Sleep duration |
| task_completion_rate | float | 0-100 | Task completion percentage |
| day_type | string | - | "Weekday" or "Weekend" |

### Target Variables

| Variable | Type | Description |
|----------|------|-------------|
| burnout_risk | string | "High" or "Low" |
| burnout_score | float | Continuous score (0-1) |

### Data Distribution

```
Burnout Risk Distribution:
- Low Risk: 11,375 samples (50%)
- High Risk: 11,375 samples (50%)

Perfectly balanced dataset!
```

### Data Statistics

```python
work_hours:          mean=8.5,  std=2.3,  median=8.0
screen_time_hours:   mean=6.2,  std=1.8,  median=6.0
meetings_count:      mean=3.5,  std=1.9,  median=3.0
breaks_taken:        mean=2.8,  std=1.2,  median=3.0
sleep_hours:         mean=7.1,  std=1.1,  median=7.0
task_completion_rate: mean=78.5, std=12.3, median=80.0
```

## Feature Engineering

### Philosophy

Transform raw metrics into meaningful indicators of burnout risk by capturing:
1. **Work Intensity**: How demanding is the workload?
2. **Health Impact**: How does work affect health?
3. **Recovery Capacity**: Can the person recover from work stress?
4. **Work-Life Balance**: Is there a healthy balance?

### Engineered Features (9)

#### 1. Work Intensity Ratio
```python
work_intensity_ratio = screen_time_hours / (work_hours + 0.1)
```
**Interpretation**:
- High value (>1.0): Intense screen-focused work
- Low value (<0.5): Less screen-intensive work
- Captures: Digital fatigue risk

#### 2. Meeting Burden
```python
meeting_burden = meetings_count / (work_hours + 0.1)
```
**Interpretation**:
- High value (>0.5): Meeting-heavy schedule
- Low value (<0.3): More focus time
- Captures: Context switching overhead

#### 3. Break Adequacy
```python
break_adequacy = breaks_taken / (work_hours + 0.1)
```
**Interpretation**:
- High value (>0.5): Adequate breaks
- Low value (<0.2): Insufficient breaks
- Captures: Recovery opportunities

#### 4. Sleep Deficit
```python
sleep_deficit = 8 - sleep_hours
```
**Interpretation**:
- Positive value: Sleep deprivation
- Negative value: Adequate sleep
- Captures: Sleep health

#### 5. Recovery Index
```python
recovery_index = (sleep_hours + breaks_taken) - screen_time_hours
```
**Interpretation**:
- Positive value: Good recovery
- Negative value: Poor recovery
- Captures: Overall recovery capacity

#### 6. Fatigue Risk
```python
fatigue_risk = screen_time_hours - (sleep_hours * 1.5)
```
**Interpretation**:
- High positive: High fatigue risk
- Negative: Low fatigue risk
- Captures: Screen time vs. sleep balance

#### 7. Workload Pressure
```python
workload_pressure = work_hours + (meetings_count * 0.25) + after_hours_work
```
**Interpretation**:
- High value (>10): Excessive workload
- Low value (<8): Manageable workload
- Captures: Total work pressure

#### 8. Task Efficiency
```python
task_efficiency = task_completion_rate / (work_hours + 0.1)
```
**Interpretation**:
- High value (>10): Efficient work
- Low value (<5): Inefficient work
- Captures: Productivity per hour

#### 9. Work-Life Balance Score
```python
work_life_balance_score = (
    (sleep_hours / 8) * 30 +
    (breaks_taken / 5) * 30 -
    (work_hours / 10) * 20 -
    after_hours_work * 10
) * 2
```
**Interpretation**:
- Range: 0-100
- High value (>70): Good balance
- Low value (<30): Poor balance
- Captures: Holistic work-life balance

### Additional Derived Metrics (6)

These are calculated but not used in the model (for analysis only):

1. **screen_time_per_meeting**: Screen time divided by meetings
2. **work_hours_productivity**: Task completion adjusted for hours
3. **health_risk_score**: Combined sleep and fatigue risk (0-100)
4. **after_hours_work_hours_est**: Estimated after-hours duration
5. **high_workload_flag**: Binary flag for high workload
6. **poor_recovery_flag**: Binary flag for poor recovery

### Feature Importance

Based on Random Forest feature importance:

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | work_life_balance_score | 0.18 | Engineered |
| 2 | recovery_index | 0.15 | Engineered |
| 3 | sleep_deficit | 0.12 | Engineered |
| 4 | work_hours | 0.11 | Raw |
| 5 | fatigue_risk | 0.10 | Engineered |
| 6 | workload_pressure | 0.09 | Engineered |
| 7 | screen_time_hours | 0.08 | Raw |
| 8 | task_efficiency | 0.06 | Engineered |
| 9 | sleep_hours | 0.05 | Raw |
| 10 | work_intensity_ratio | 0.04 | Engineered |

**Key Insight**: Engineered features dominate top 10!

## Model Training Process

### Step 1: Data Loading

```python
df = pd.read_csv('data/work_from_home_burnout_dataset.csv')
print(f"Dataset shape: {df.shape}")  # (22750, 10)
```

### Step 2: Feature Engineering

```python
df = engineer_features(df)
# Adds 9 engineered features
```

### Step 3: Target Creation

```python
df['target'] = (df['burnout_risk'] == 'High').astype(int)
# High Risk = 1, Low Risk = 0
```

### Step 4: Feature Selection

```python
feature_cols = [
    # Raw features (8)
    'work_hours', 'screen_time_hours', 'meetings_count',
    'breaks_taken', 'after_hours_work', 'sleep_hours',
    'task_completion_rate', 'is_weekday',
    # Engineered features (9)
    'work_intensity_ratio', 'meeting_burden', 'break_adequacy',
    'sleep_deficit', 'recovery_index', 'fatigue_risk',
    'workload_pressure', 'task_efficiency', 'work_life_balance_score'
]
```

### Step 5: Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# Train: 18,200 samples (80%)
# Test: 4,550 samples (20%)
```

### Step 6: Feature Scaling

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Why StandardScaler?**
- Normalizes features to mean=0, std=1
- Improves model convergence
- Prevents feature dominance

### Step 7: Model Training

```python
models = {
    'RandomForest': RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    ),
    'GradientBoosting': GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    ),
    'XGBoost': xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
}

# Train all models
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
```

### Step 8: Model Evaluation

```python
for name, model in models.items():
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    
    print(f"{name}: Accuracy={acc:.4f}, ROC-AUC={auc:.4f}")
```

**Results**:
```
RandomForest:      Accuracy=0.9889, ROC-AUC=0.9779
GradientBoosting:  Accuracy=0.9756, ROC-AUC=0.9654
XGBoost:           Accuracy=0.9723, ROC-AUC=0.9612
```

### Step 9: Model Selection

```python
# Select best model based on ROC-AUC
best_model = RandomForest  # Highest ROC-AUC
```

**Why ROC-AUC?**
- Measures model's ability to distinguish classes
- Robust to class imbalance
- Better than accuracy for binary classification

### Step 10: Model Saving

```python
joblib.dump(best_model, 'models/best_model.joblib')
joblib.dump(scaler, 'models/preprocessor.joblib')
joblib.dump(feature_cols, 'models/feature_names.joblib')
```

## Model Performance

### Classification Report

```
              precision    recall  f1-score   support

    Low Risk       0.99      0.99      0.99      2275
   High Risk       0.99      0.99      0.99      2275

    accuracy                           0.99      4550
   macro avg       0.99      0.99      0.99      4550
weighted avg       0.99      0.99      0.99      4550
```

### Confusion Matrix

```
                Predicted
                Low   High
Actual  Low    2251    24
        High     26  2249
```

**Interpretation**:
- True Positives (High Risk correctly identified): 2249
- True Negatives (Low Risk correctly identified): 2251
- False Positives (Low Risk predicted as High): 24
- False Negatives (High Risk predicted as Low): 26

### ROC Curve

- **AUC**: 0.9779
- **Interpretation**: 97.79% chance model ranks random High Risk sample higher than random Low Risk sample

### Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Accuracy | 98.89% | Overall correctness |
| Precision (High) | 98.94% | Of predicted High, 98.94% are correct |
| Recall (High) | 98.86% | Of actual High, 98.86% are detected |
| F1-Score (High) | 98.90% | Harmonic mean of precision & recall |
| ROC-AUC | 97.79% | Discrimination ability |

## Model Inference

### Prediction Pipeline

```python
# 1. Receive input
user_data = {
    "work_hours": 10.0,
    "screen_time_hours": 8.0,
    "meetings_count": 5,
    "breaks_taken": 2,
    "after_hours_work": 1,
    "sleep_hours": 6.0,
    "task_completion_rate": 70.0,
    "day_type": "Weekday"
}

# 2. Engineer features
features_array, all_features = engineer_features(user_data)
# Shape: (1, 17)

# 3. Scale features
features_scaled = scaler.transform(features_array)

# 4. Predict
prediction = model.predict(features_scaled)[0]  # 0 or 1
probability = model.predict_proba(features_scaled)[0][1]  # 0.0-1.0

# 5. Return result
risk_level = "High" if prediction == 1 else "Low"
```

### Inference Time

- **Average**: 45ms
- **P95**: 80ms
- **P99**: 120ms

**Breakdown**:
- Feature engineering: 5ms
- Scaling: 2ms
- Model prediction: 35ms
- Response formatting: 3ms

## Model Limitations

### 1. Data Limitations
- **Synthetic data**: Not from real employees
- **Limited features**: Only 8 input features
- **No temporal data**: Single snapshot, no trends

### 2. Model Limitations
- **Binary classification**: Only High/Low, no gradations
- **No uncertainty quantification**: No confidence intervals
- **Static model**: Doesn't adapt to new patterns

### 3. Deployment Limitations
- **Cold start**: Model loading takes 2-3 seconds
- **Memory**: 50 MB model size
- **Scalability**: Single model instance

## Model Improvements

### Short-term (Next Version)

1. **Hyperparameter Tuning**
   ```python
   from sklearn.model_selection import GridSearchCV
   
   param_grid = {
       'n_estimators': [100, 200, 300],
       'max_depth': [10, 15, 20],
       'min_samples_split': [2, 5, 10]
   }
   
   grid_search = GridSearchCV(
       RandomForestClassifier(),
       param_grid,
       cv=5,
       scoring='roc_auc'
   )
   ```

2. **Feature Selection**
   - Remove low-importance features
   - Reduce model size
   - Improve inference speed

3. **Ensemble Methods**
   - Combine RF, GB, XGB predictions
   - Voting or stacking
   - Improve robustness

### Long-term (Future Versions)

1. **Deep Learning**
   - Neural network for complex patterns
   - Attention mechanisms
   - Transfer learning

2. **Time Series Analysis**
   - Track burnout trends over time
   - Predict future risk
   - Early warning system

3. **Multi-class Classification**
   - Low, Medium, High, Critical
   - More granular risk levels
   - Better actionability

4. **Explainable AI**
   - SHAP values for predictions
   - Feature contribution analysis
   - Transparent decision-making

## Model Monitoring

### Metrics to Track

1. **Performance Metrics**
   - Accuracy, Precision, Recall
   - ROC-AUC, F1-Score
   - Confusion matrix

2. **Data Drift**
   - Feature distribution changes
   - Target distribution changes
   - Covariate shift

3. **Prediction Drift**
   - Prediction distribution changes
   - Confidence score changes
   - Error rate changes

### Retraining Strategy

**Trigger Retraining When**:
- Accuracy drops below 95%
- Data drift detected (>10% change)
- New data available (>5000 samples)
- Monthly scheduled retraining

**Retraining Process**:
1. Collect new data from database
2. Combine with existing data
3. Re-engineer features
4. Train new model
5. Evaluate on holdout set
6. Deploy if better than current

## Experiment Tracking (W&B)

### Logged Metrics

```python
wandb.log({
    "accuracy": 0.9889,
    "roc_auc": 0.9779,
    "precision_high": 0.9894,
    "recall_high": 0.9886,
    "f1_high": 0.9890,
    "confusion_matrix": [[2251, 24], [26, 2249]],
    "feature_importance": {...}
})
```

### Logged Artifacts

- Model file (best_model.joblib)
- Scaler file (preprocessor.joblib)
- Feature names (feature_names.joblib)
- Training dataset
- Evaluation plots

### W&B Dashboard

View at: https://wandb.ai/kakarlagana18-iihmr/burnout-prediction

**Panels**:
- Training metrics over time
- Confusion matrix
- ROC curve
- Precision-recall curve
- Feature importance

## References

- **Random Forest**: Breiman, L. (2001). Random Forests. Machine Learning.
- **Feature Engineering**: Zheng, A., & Casari, A. (2018). Feature Engineering for Machine Learning.
- **Model Evaluation**: Fawcett, T. (2006). An introduction to ROC analysis.
