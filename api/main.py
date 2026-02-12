#!/usr/bin/env python3
# File: api/main.py
# Version: 1.0 - Production Ready

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
    description="ML API for burnout risk prediction",
    version="1.0.0"
)

# CORS middleware
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


model = None
preprocessor = None


@app.on_event("startup")
async def load_model():
    """Load model and preprocessor at startup"""
    global model, preprocessor
    try:
        model_path = os.getenv('MODEL_PATH', 'models/best_model.joblib')
        preprocessor_path = (os.getenv('PREPROCESSOR_PATH',
                             'models/preprocessor.joblib'))
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info("✓ Model loaded")
        if os.path.exists(preprocessor_path):
            preprocessor = joblib.load(preprocessor_path)
            logger.info("✓ Preprocessor loaded")
    except Exception as e:
        logger.warning(f"Could not load model/preprocessor: {e}")


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )


@app.post("/predict", response_model=BurnoutPrediction)
async def predict(user_data: UserData):
    """Make burnout risk prediction"""
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        # Prepare data (simplified - without preprocessor)
        input_dict = user_data.model_dump()
        input_array = np.array([[input_dict[key]
                                 for key in input_dict.keys()]])
        # Predict
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][1]
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


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint (placeholder)"""
    return {"status": "metrics placeholder"}


@app.get("/")
async def root():
    """API documentation"""
    return {
        "message": "Burnout Risk Prediction API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Handle browser favicon requests without 404 noise."""
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
