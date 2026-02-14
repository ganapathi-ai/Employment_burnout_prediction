#!/usr/bin/env python3
"""Verify logic consistency across all files"""
import pandas as pd
import numpy as np
from api.main import engineer_features, UserData

print("=" * 60)
print("LOGIC CONSISTENCY VERIFICATION")
print("=" * 60)

# Test data
test_data = {
    "work_hours": 9.0,
    "screen_time_hours": 8.0,
    "meetings_count": 5,
    "breaks_taken": 2,
    "after_hours_work": 1,
    "sleep_hours": 6.5,
    "task_completion_rate": 85.0,
    "day_type": "Weekday",
    "name": "Test",
    "user_id": "test001"
}

# Get API features
user_data = UserData(**test_data)
_, api_features = engineer_features(user_data)

# Calculate manually using transform_data.py logic
work_hours = test_data["work_hours"]
screen_time = test_data["screen_time_hours"]
meetings = test_data["meetings_count"]
breaks = test_data["breaks_taken"]
after_hours = test_data["after_hours_work"]
sleep = test_data["sleep_hours"]
task_rate = test_data["task_completion_rate"]
is_weekday = 1 if test_data["day_type"] == "Weekday" else 0

# Calculate features manually
manual_features = {
    'work_hours': work_hours,
    'screen_time_hours': screen_time,
    'meetings_count': meetings,
    'breaks_taken': breaks,
    'after_hours_work': after_hours,
    'sleep_hours': sleep,
    'task_completion_rate': task_rate,
    'is_weekday': is_weekday,
    'work_intensity_ratio': screen_time / (work_hours + 0.1),
    'meeting_burden': meetings / (work_hours + 0.1),
    'break_adequacy': breaks / (work_hours + 0.1),
    'sleep_deficit': 8 - sleep,
    'recovery_index': (sleep + breaks) - screen_time,
    'fatigue_risk': screen_time - (sleep * 1.5),
    'workload_pressure': work_hours + (meetings * 0.25) + after_hours,
    'task_efficiency': task_rate / (work_hours + 0.1),
    'work_life_balance_score': np.clip(
        ((sleep / 8) * 30 + (breaks / 5) * 30 - (work_hours / 10) * 20 - after_hours * 10) * 2,
        0, 100
    ),
    'screen_time_per_meeting': screen_time / (meetings + 0.1),
    'work_hours_productivity': task_rate * (1 - (work_hours / 15)) * 100,
    'health_risk_score': np.clip(
        (1 - (sleep / 8)) * 40 + max(0, screen_time - (sleep * 1.5)) * 10,
        0, 100
    ),
    'after_hours_work_hours_est': after_hours * (work_hours * 0.1)
}

# Load medians for flags
try:
    df = pd.read_csv('data/work_from_home_burnout_dataset.csv')
    median_hours = df['work_hours'].median()
    median_meetings = df['meetings_count'].median()
except:
    median_hours = 8
    median_meetings = 3

manual_features['high_workload_flag'] = int((work_hours > median_hours) and (meetings > median_meetings))
manual_features['poor_recovery_flag'] = int((sleep < 6) and (manual_features['recovery_index'] < 0))

# Compare
print("\nFeature Comparison:")
print("-" * 60)

all_match = True
for key in manual_features.keys():
    api_val = api_features.get(key)
    manual_val = manual_features[key]
    
    # Check if values match (with tolerance for floats)
    if isinstance(api_val, (int, float)) and isinstance(manual_val, (int, float)):
        match = abs(api_val - manual_val) < 0.0001
    else:
        match = api_val == manual_val
    
    status = "PASS" if match else "FAIL"
    
    if not match:
        all_match = False
        print(f"{status} {key:30s} API: {api_val:10.4f}  Manual: {manual_val:10.4f}")
    else:
        print(f"{status} {key:30s} MATCH")

print("-" * 60)

if all_match:
    print("\nALL FEATURES MATCH - Logic is consistent!")
else:
    print("\nMISMATCH FOUND - Check formulas!")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
