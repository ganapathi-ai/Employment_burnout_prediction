#!/usr/bin/env python3
"""Initialize W&B live monitoring project with sample predictions"""
import wandb
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("Initializing W&B Live Monitoring Project...")

# Initialize live monitoring project
run = wandb.init(
    entity=os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr'),
    project="burnout-prediction-live",
    name=f"api_monitoring_{datetime.now().strftime('%Y%m%d_%H%M')}",
    job_type="monitoring",
    tags=["production", "api", "live-monitoring"],
    config={
        "environment": "production",
        "api_version": "2.0.0",
        "monitoring_type": "real-time predictions"
    },
    notes="Live API prediction monitoring - tracks risk levels, response times, and feature distributions"
)

print(f"\n[OK] Project initialized!")
print(f"  Run: {run.name}")
print(f"  URL: {run.url}")

# Log sample prediction data to create the project
print("\nLogging sample predictions...")

sample_predictions = [
    {"risk_level": 0, "risk_probability": 0.23, "work_hours": 8, "sleep_hours": 7, "response_time_ms": 145},
    {"risk_level": 1, "risk_probability": 0.78, "work_hours": 12, "sleep_hours": 5, "response_time_ms": 152},
    {"risk_level": 0, "risk_probability": 0.15, "work_hours": 7, "sleep_hours": 8, "response_time_ms": 138},
    {"risk_level": 1, "risk_probability": 0.82, "work_hours": 11, "sleep_hours": 5.5, "response_time_ms": 160},
    {"risk_level": 0, "risk_probability": 0.31, "work_hours": 9, "sleep_hours": 6.5, "response_time_ms": 142},
]

for i, pred in enumerate(sample_predictions, 1):
    wandb.log({
        "prediction_count": i,
        "risk_level": pred["risk_level"],
        "risk_probability": pred["risk_probability"],
        "work_hours": pred["work_hours"],
        "sleep_hours": pred["sleep_hours"],
        "response_time_ms": pred["response_time_ms"],
        "timestamp": datetime.now().isoformat()
    })

print(f"[OK] Logged {len(sample_predictions)} sample predictions")

# Log summary statistics
wandb.run.summary["total_predictions"] = len(sample_predictions)
wandb.run.summary["high_risk_count"] = sum(1 for p in sample_predictions if p["risk_level"] == 1)
wandb.run.summary["avg_response_time"] = sum(p["response_time_ms"] for p in sample_predictions) / len(sample_predictions)

run.finish()

print("\n[SUCCESS] Live monitoring project created!")
print(f"\nView dashboard at:")
print(f"https://wandb.ai/{os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr')}/burnout-prediction-live")
print("\nThis project will now track:")
print("  - Real-time API predictions")
print("  - Risk level distribution")
print("  - Response times")
print("  - Feature patterns")
print("  - Error rates")
