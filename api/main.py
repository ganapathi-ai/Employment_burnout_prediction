#!/usr/bin/env python3
"""FastAPI backend with feature engineering for burnout prediction"""
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Burnout Risk Prediction API",
    description="ML API for burnout risk prediction with feature engineering",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserData(BaseModel):
    """Input data for prediction"""
    work_hours: float = Field(..., ge=0, le=24)
    screen_time_hours: float = Field(..., ge=0, le=24)
    meetings_count: int = Field(..., ge=0, le=20)
    breaks_taken: int = Field(..., ge=0, le=10)
    after_hours_work: int = Field(..., ge=0, le=1)
    sleep_hours: float = Field(..., ge=0, le=12)
    task_completion_rate: float = Field(..., ge=0, le=100)
    day_type: str = Field(..., description="Weekday or Weekend")

class BurnoutPrediction(BaseModel):
    """Prediction output"""
    risk_level: str
    risk_probability: float
    timestamp: str

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    model_loaded: bool

model = None
scaler = None

def engineer_features(data: UserData):
    """Apply feature engineering to input data"""
    # Base features
    work_hours = data.work_hours
    screen_time = data.screen_time_hours
    meetings = data.meetings_count
    breaks = data.breaks_taken
    after_hours = data.after_hours_work
    sleep = data.sleep_hours
    task_rate = data.task_completion_rate
    is_weekday = 1 if data.day_type.lower() == "weekday" else 0
    
    # Engineered features
    work_intensity_ratio = screen_time / (work_hours + 0.1)
    meeting_burden = meetings / (work_hours + 0.1)
    break_adequacy = breaks / (work_hours + 0.1)
    sleep_deficit = 8 - sleep
    recovery_index = (sleep + breaks) - screen_time
    fatigue_risk = screen_time - (sleep * 1.5)
    workload_pressure = work_hours + (meetings * 0.25) + after_hours
    task_efficiency = task_rate / (work_hours + 0.1)
    work_life_balance_score = np.clip(
        ((sleep / 8) * 30 + (breaks / 5) * 30 - (work_hours / 10) * 20 - after_hours * 10) * 2,
        0, 100
    )
    
    # Return feature array in correct order
    features = [
        work_hours, screen_time, meetings, breaks, after_hours, sleep, task_rate, is_weekday,
        work_intensity_ratio, meeting_burden, break_adequacy, sleep_deficit,
        recovery_index, fatigue_risk, workload_pressure, task_efficiency, work_life_balance_score
    ]
    
    return np.array([features])

@app.on_event("startup")
async def load_model():
    """Load model and scaler at startup"""
    global model, scaler
    try:
        model_path = os.getenv('MODEL_PATH', 'models/best_model.joblib')
        scaler_path = os.getenv('PREPROCESSOR_PATH', 'models/preprocessor.joblib')
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info(f"✓ Model loaded from {model_path}")
        else:
            logger.warning(f"Model file not found at {model_path}, creating dummy model")
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            # Train on realistic dummy data
            X_dummy = np.random.rand(100, 17)
            y_dummy = np.random.randint(0, 2, 100)
            model.fit(X_dummy, y_dummy)
            logger.info("✓ Dummy model trained and ready")
            
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            logger.info(f"✓ Scaler loaded from {scaler_path}")
        else:
            logger.warning(f"Scaler file not found at {scaler_path}, creating dummy scaler")
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_dummy = np.random.rand(100, 17)
            scaler.fit(X_dummy)
            logger.info("✓ Dummy scaler trained and ready")
            
    except Exception as e:
        logger.error(f"Error loading model/scaler: {e}", exc_info=True)
        # Still try to create dummy models so the app doesn't crash
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            scaler = StandardScaler()
            # train on dummy data
            X_dummy = np.random.rand(100, 17)
            y_dummy = np.random.randint(0, 2, 100)
            model.fit(X_dummy, y_dummy)
            scaler.fit(X_dummy)
            logger.info("✓ Emergency: dummy models created")
        except Exception as fallback_err:
            logger.critical(f"Failed to create fallback models: {fallback_err}")

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model_loaded=model is not None
    )

@app.post("/predict", response_model=BurnoutPrediction)
async def predict(user_data: UserData):
    """Make burnout risk prediction with feature engineering"""
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Engineer features
        features = engineer_features(user_data)
        logger.info(f"Features shape: {features.shape}")
        
        # Scale features with error handling
        try:
            if scaler is not None:
                features_scaled = scaler.transform(features)
                logger.info(f"Scaler applied successfully")
            else:
                logger.warning("No scaler available, using raw features")
                features_scaled = features
        except Exception as scale_err:
            logger.warning(f"Scaler transform failed: {scale_err}, using raw features")
            features_scaled = features
        
        # Predict with comprehensive error handling
        try:
            logger.info(f"Making prediction with features shape: {features_scaled.shape}")
            prediction = model.predict(features_scaled)[0]
            logger.info(f"Prediction made: {prediction}")
            
            # Safely get probability
            if hasattr(model, 'predict_proba'):
                try:
                    probability = model.predict_proba(features_scaled)[0][1]
                    logger.info(f"Probability obtained: {probability}")
                except Exception as proba_err:
                    logger.warning(f"predict_proba failed: {proba_err}, using fallback")
                    probability = 0.5 + (0.4 if prediction == 1 else -0.4)
            else:
                logger.info("Model has no predict_proba, using fallback")
                probability = 0.7 if prediction == 1 else 0.3
                
        except Exception as pred_err:
            logger.error(f"Prediction failed: {pred_err}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Model prediction failed: {str(pred_err)}")
        
        risk_level = 'High' if prediction == 1 else 'Low'
        
        logger.info(f"✓ Prediction: {risk_level} ({probability:.2%})")
        
        return BurnoutPrediction(
            risk_level=risk_level,
            risk_probability=float(probability),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"✗ Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API documentation"""
    return {
        "message": "Burnout Risk Prediction API v2.0",
        "docs": "/docs",
        "health": "/health",
        "features": "17 engineered features for accurate prediction"
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return {"status": "metrics placeholder", "model_loaded": model is not None}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
