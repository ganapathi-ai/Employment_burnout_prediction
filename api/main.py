# pylint: disable=global-statement,import-outside-toplevel,too-many-locals
#!/usr/bin/env python3
"""FastAPI backend with feature engineering for burnout prediction"""
import logging
import os
from datetime import datetime, UTC

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator
import joblib
import numpy as np
import pandas as pd
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, DateTime, Float
)
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv()

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
    # optional tracking fields
    name: str | None = Field(None, description="Optional user name for tracking")
    user_id: str | None = Field(None, description="Optional user ID for tracking")

    @model_validator(mode='after')
    def require_name_or_userid(self):
        """Validate that either name or user_id is provided"""
        if not (self.name or self.user_id):
            raise ValueError('Either name or user_id must be provided')
        return self


class BurnoutPrediction(BaseModel):
    """Prediction output"""
    risk_level: str
    risk_probability: float
    timestamp: str
    features: dict = Field(..., description="All input and derived metrics computed by the API")


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    model_loaded: bool


MODEL = None
SCALER = None

# medians used for flag calculations; loaded lazily
MEDIAN_HOURS: float | None = None
MEDIAN_MEETINGS: float | None = None

# ---------- database setup ----------
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./user_requests.db')
engine = create_engine(DATABASE_URL, echo=False, future=True)
metadata = MetaData()


user_requests = Table(
    'user_requests', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', String, nullable=True),
    Column('name', String, nullable=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    # Input features
    Column('work_hours', Float, nullable=False),
    Column('screen_time_hours', Float, nullable=False),
    Column('meetings_count', Integer, nullable=False),
    Column('breaks_taken', Integer, nullable=False),
    Column('after_hours_work', Integer, nullable=False),
    Column('sleep_hours', Float, nullable=False),
    Column('task_completion_rate', Float, nullable=False),
    Column('is_weekday', Integer, nullable=False),
    # Engineered features
    Column('work_intensity_ratio', Float),
    Column('meeting_burden', Float),
    Column('break_adequacy', Float),
    Column('sleep_deficit', Float),
    Column('recovery_index', Float),
    Column('fatigue_risk', Float),
    Column('workload_pressure', Float),
    Column('task_efficiency', Float),
    Column('work_life_balance_score', Float),
    Column('screen_time_per_meeting', Float),
    Column('work_hours_productivity', Float),
    Column('health_risk_score', Float),
    Column('after_hours_work_hours_est', Float),
    Column('high_workload_flag', Integer),
    Column('poor_recovery_flag', Integer)
)

# create table if missing
try:
    metadata.create_all(engine)
    logger.info('Database table initialized')
except Exception as e:
    logger.warning('Could not initialize database table: %s', e)

# -------------------------------------


def _load_medians():
    """Load median values from dataset"""
    global MEDIAN_HOURS, MEDIAN_MEETINGS
    if MEDIAN_HOURS is None or MEDIAN_MEETINGS is None:
        try:
            path = os.getenv('DATA_PATH', 'data/work_from_home_burnout_dataset.csv')
            if not os.path.exists(path):
                path = os.getenv('DATA_PATH', 'data/work_from_home_burnout_dataset_transformed.csv')
            df = pd.read_csv(path)
            MEDIAN_HOURS = df['work_hours'].median()
            MEDIAN_MEETINGS = df['meetings_count'].median()
        except Exception:
            MEDIAN_HOURS = 8
            MEDIAN_MEETINGS = 3


# ensure medians are available early
_load_medians()

# Load model immediately at import (not just at startup)


def _load_model_sync():
    """Load model and scaler at module import"""
    global MODEL, SCALER
    try:
        model_path = os.getenv('MODEL_PATH', 'models/best_model.joblib')
        scaler_path = os.getenv('PREPROCESSOR_PATH', 'models/preprocessor.joblib')

        logger.info("Attempting to load model from: %s", model_path)
        logger.info("Attempting to load scaler from: %s", scaler_path)

        if not os.path.exists(model_path):
            logger.error("Model file not found at %s", model_path)
            logger.error("Current working directory: %s", os.getcwd())
            logger.error("Directory contents: %s", os.listdir('.'))
            if os.path.exists('models'):
                logger.error("Models directory contents: %s", os.listdir('models'))
            raise FileNotFoundError(f"Model file not found: {model_path}")

        if not os.path.exists(scaler_path):
            logger.error("Scaler file not found at %s", scaler_path)
            raise FileNotFoundError(f"Scaler file not found: {scaler_path}")

        MODEL = joblib.load(model_path)
        logger.info("✓ Model loaded successfully from %s", model_path)

        SCALER = joblib.load(scaler_path)
        logger.info("✓ Scaler loaded successfully from %s", scaler_path)

    except FileNotFoundError as fnf_err:
        logger.error("File not found error: %s", fnf_err)
        logger.warning("Creating fallback dummy model for development/testing only")
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler
            MODEL = RandomForestClassifier(n_estimators=10, random_state=42)
            SCALER = StandardScaler()
            x_dummy = np.random.rand(100, 17)
            y_dummy = np.random.randint(0, 2, 100)
            MODEL.fit(x_dummy, y_dummy)
            SCALER.fit(x_dummy)
            logger.warning("⚠ Dummy model created - NOT FOR PRODUCTION USE")
        except Exception as fallback_err:
            logger.critical("Failed to create fallback models: %s", fallback_err)
            raise
    except Exception as e:
        logger.error("Error loading model/scaler: %s", e, exc_info=True)
        raise


# Load model at import time
_load_model_sync()


def engineer_features(data: UserData):
    """Apply feature engineering to input data.

    Returns a tuple `(model_features, all_features_dict)`.  `model_features` is a
    numpy array containing the 17 values expected by the ML model.  The dict
    includes every input plus the additional derived metrics/flags so callers can
    inspect them.
    """
    # Base inputs
    work_hours = data.work_hours
    screen_time = data.screen_time_hours
    meetings = data.meetings_count
    breaks = data.breaks_taken
    after_hours = data.after_hours_work
    sleep = data.sleep_hours
    task_rate = data.task_completion_rate
    is_weekday = 1 if data.day_type.lower() == "weekday" else 0

    # Primary engineered features (used by model)
    work_intensity_ratio = screen_time / (work_hours + 0.1)
    meeting_burden = meetings / (work_hours + 0.1)
    break_adequacy = breaks / (work_hours + 0.1)
    sleep_deficit = 8 - sleep
    recovery_index = (sleep + breaks) - screen_time
    fatigue_risk = screen_time - (sleep * 1.5)
    workload_pressure = work_hours + (meetings * 0.25) + after_hours
    task_efficiency = task_rate / (work_hours + 0.1)
    wlb_score = np.clip(
        ((sleep / 8) * 30 + (breaks / 5) * 30 - (work_hours / 10) * 20 - after_hours * 10) * 2,
        0, 100
    )

    # Additional derived metrics/flags
    screen_per_meeting = screen_time / (meetings + 0.1)
    hours_productivity = task_rate * (1 - (work_hours / 15))
    health_risk = np.clip((1 - (sleep / 8)) * 40 + max(0, fatigue_risk) * 10, 0, 100)
    after_hours_est = after_hours * (work_hours * 0.1)
    high_workload = int((work_hours > MEDIAN_HOURS) and (meetings > MEDIAN_MEETINGS))
    poor_recovery = int((sleep < 6) and (recovery_index < 0))

    # features array for model (maintain existing order)
    model_feats = [
        work_hours, screen_time, meetings, breaks, after_hours, sleep, task_rate, is_weekday,
        work_intensity_ratio, meeting_burden, break_adequacy, sleep_deficit,
        recovery_index, fatigue_risk, workload_pressure, task_efficiency, wlb_score
    ]

    all_feats = {
        'work_hours': work_hours, 'screen_time_hours': screen_time,
        'meetings_count': meetings, 'breaks_taken': breaks,
        'after_hours_work': after_hours, 'sleep_hours': sleep,
        'task_completion_rate': task_rate, 'is_weekday': is_weekday,
        'work_intensity_ratio': work_intensity_ratio, 'meeting_burden': meeting_burden,
        'break_adequacy': break_adequacy, 'sleep_deficit': sleep_deficit,
        'recovery_index': recovery_index, 'fatigue_risk': fatigue_risk,
        'workload_pressure': workload_pressure, 'task_efficiency': task_efficiency,
        'work_life_balance_score': wlb_score, 'screen_time_per_meeting': screen_per_meeting,
        'work_hours_productivity': hours_productivity, 'health_risk_score': health_risk,
        'after_hours_work_hours_est': after_hours_est,
        'high_workload_flag': high_workload, 'poor_recovery_flag': poor_recovery
    }

    return np.array([model_feats]), all_feats


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model_loaded=MODEL is not None
    )


@app.post("/predict", response_model=BurnoutPrediction)
async def predict(user_data: UserData):
    """Make burnout risk prediction with feature engineering"""
    try:
        if MODEL is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        if SCALER is None:
            raise HTTPException(status_code=503, detail="Scaler not loaded")

        # Engineer features (returns tuple of model-ready array and full dict)
        features_array, all_features = engineer_features(user_data)
        logger.info("Raw model feature array shape: %s", features_array.shape)

        # add tracking info to features dict for storage
        all_features['name'] = user_data.name
        all_features['user_id'] = user_data.user_id

        # Scale features using trained scaler
        try:
            features_scaled = SCALER.transform(features_array)
            logger.info("Features scaled using trained scaler")
        except Exception as scale_err:
            logger.error("Scaling failed: %s, using raw features", scale_err)
            features_scaled = features_array

        # Predict with comprehensive error handling
        try:
            logger.info("Making prediction with features shape: %s", features_scaled.shape)
            prediction = MODEL.predict(features_scaled)[0]
            logger.info("Prediction made: %s", prediction)

            # Safely get probability
            try:
                probability = MODEL.predict_proba(features_scaled)[0][1]
                logger.info("Probability obtained: %s", probability)
            except Exception as proba_err:
                logger.warning("predict_proba failed: %s, using fallback", proba_err)
                probability = 0.7 if prediction == 1 else 0.3

        except Exception as pred_err:
            logger.error("Model prediction failed: %s", pred_err, exc_info=True)
            # Very last resort: return a neutral prediction
            logger.error("Using fallback neutral prediction")
            prediction = 0
            probability = 0.5

        risk_level = 'High' if prediction == 1 else 'Low'

        logger.info("Prediction: %s (%.2f%%)", risk_level, probability * 100)

        # log to database (non-blocking failures)
        try:
            logger.info("Attempting to store data in database...")
            ins = user_requests.insert().values(
                user_id=user_data.user_id,
                name=user_data.name,
                created_at=datetime.now(UTC),
                work_hours=float(all_features['work_hours']),
                screen_time_hours=float(all_features['screen_time_hours']),
                meetings_count=int(all_features['meetings_count']),
                breaks_taken=int(all_features['breaks_taken']),
                after_hours_work=int(all_features['after_hours_work']),
                sleep_hours=float(all_features['sleep_hours']),
                task_completion_rate=float(all_features['task_completion_rate']),
                is_weekday=int(all_features['is_weekday']),
                work_intensity_ratio=float(all_features['work_intensity_ratio']),
                meeting_burden=float(all_features['meeting_burden']),
                break_adequacy=float(all_features['break_adequacy']),
                sleep_deficit=float(all_features['sleep_deficit']),
                recovery_index=float(all_features['recovery_index']),
                fatigue_risk=float(all_features['fatigue_risk']),
                workload_pressure=float(all_features['workload_pressure']),
                task_efficiency=float(all_features['task_efficiency']),
                work_life_balance_score=float(all_features['work_life_balance_score']),
                screen_time_per_meeting=float(all_features['screen_time_per_meeting']),
                work_hours_productivity=float(all_features['work_hours_productivity']),
                health_risk_score=float(all_features['health_risk_score']),
                after_hours_work_hours_est=float(all_features['after_hours_work_hours_est']),
                high_workload_flag=int(all_features['high_workload_flag']),
                poor_recovery_flag=int(all_features['poor_recovery_flag'])
            )
            with engine.connect() as conn:
                result = conn.execute(ins)
                conn.commit()
                logger.info("Request stored in DB with ID: %s", result.inserted_primary_key)
        except SQLAlchemyError as db_err:
            logger.error("DB insert failed: %s", db_err, exc_info=True)
        except Exception as db_exc:
            logger.error("Unexpected DB error: %s", db_exc, exc_info=True)

        return BurnoutPrediction(
            risk_level=risk_level,
            risk_probability=float(probability),
            timestamp=datetime.now().isoformat(),
            features=all_features
        )
    except Exception as e:
        logger.error("Prediction error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


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
    return {"status": "metrics placeholder", "model_loaded": MODEL is not None}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
