#!/usr/bin/env python3
"""W&B monitoring for live API predictions"""
import wandb
import os
from datetime import datetime

class WandBMonitor:
    """Monitor API predictions and system metrics with W&B"""
    
    def __init__(self, enabled=True):
        self.enabled = enabled and os.getenv('WANDB_API_KEY')
        self.run = None
        
        if self.enabled:
            try:
                self.run = wandb.init(
                    entity=os.getenv('WANDB_ENTITY', 'kakarlagana18-iihmr'),
                    project="burnout-prediction-live",
                    job_type="inference",
                    tags=["production", "api", "monitoring"],
                    config={
                        "environment": os.getenv('ENVIRONMENT', 'production'),
                        "api_version": "2.0.0"
                    }
                )
            except Exception as e:
                print(f"W&B init failed: {e}")
                self.enabled = False
    
    def log_prediction(self, user_data, prediction_result, response_time_ms):
        """Log individual prediction to W&B"""
        if not self.enabled:
            return
        
        try:
            features = prediction_result.get('features', {})
            
            wandb.log({
                # Prediction results
                "risk_level": 1 if prediction_result['risk_level'] == 'High' else 0,
                "risk_probability": prediction_result['risk_probability'],
                "response_time_ms": response_time_ms,
                
                # Input features
                "work_hours": features.get('work_hours', 0),
                "screen_time_hours": features.get('screen_time_hours', 0),
                "meetings_count": features.get('meetings_count', 0),
                "breaks_taken": features.get('breaks_taken', 0),
                "sleep_hours": features.get('sleep_hours', 0),
                "task_completion_rate": features.get('task_completion_rate', 0),
                
                # Key engineered features
                "work_intensity_ratio": features.get('work_intensity_ratio', 0),
                "meeting_burden": features.get('meeting_burden', 0),
                "recovery_index": features.get('recovery_index', 0),
                "fatigue_risk": features.get('fatigue_risk', 0),
                "work_life_balance_score": features.get('work_life_balance_score', 0),
                
                # Flags
                "high_workload_flag": features.get('high_workload_flag', 0),
                "poor_recovery_flag": features.get('poor_recovery_flag', 0),
                
                # Timestamp
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"W&B log failed: {e}")
    
    def log_error(self, error_type, error_message):
        """Log API errors"""
        if not self.enabled:
            return
        
        try:
            wandb.log({
                "error_count": 1,
                "error_type": error_type,
                "timestamp": datetime.now().isoformat()
            })
        except Exception:
            pass
    
    def log_health_check(self, status, model_loaded):
        """Log health check status"""
        if not self.enabled:
            return
        
        try:
            wandb.log({
                "health_status": 1 if status == "healthy" else 0,
                "model_loaded": 1 if model_loaded else 0,
                "timestamp": datetime.now().isoformat()
            })
        except Exception:
            pass
    
    def finish(self):
        """Finish W&B run"""
        if self.enabled and self.run:
            self.run.finish()

# Global monitor instance
monitor = WandBMonitor(enabled=os.getenv('ENABLE_WANDB', 'false').lower() == 'true')
