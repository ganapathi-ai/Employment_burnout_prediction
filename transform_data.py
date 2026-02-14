import pandas as pd
import numpy as np

# Read the dataset
df = pd.read_csv('data/work_from_home_burnout_dataset.csv')

# Create meaningful transformations

# 1. Work Intensity Ratio - screen time vs actual work hours
df['work_intensity_ratio'] = df['screen_time_hours'] / (df['work_hours'] + 0.1)

# 2. Meeting Burden - meetings per work hour (measures meeting overhead)
df['meeting_burden'] = df['meetings_count'] / (df['work_hours'] + 0.1)

# 3. Break Adequacy - breaks relative to work duration (measures rest frequency)
df['break_adequacy'] = df['breaks_taken'] / (df['work_hours'] + 0.1)

# 4. Sleep Deficit - how far from recommended 8 hours
df['sleep_deficit'] = 8 - df['sleep_hours']

# 5. Recovery Index - total recovery time vs work intensity
df['recovery_index'] = (df['sleep_hours'] + df['breaks_taken']) - df['screen_time_hours']

# 6. Workload Pressure - combined work demand metric
df['workload_pressure'] = df['work_hours'] + (df['meetings_count'] * 0.25) + df['after_hours_work']

# 7. Task Efficiency - completion rate per work hour
df['task_efficiency'] = df['task_completion_rate'] / (df['work_hours'] + 0.1)

# 8. Work-Life Balance Score (0-100)
df['work_life_balance_score'] = np.clip(
    ((df['sleep_hours'] / 8) * 30 + (df['breaks_taken'] / 5) * 30 - (df['work_hours'] / 10) * 20 - df['after_hours_work'] * 10) * 2,
    0, 100
)

# 9. Fatigue Risk - cumulative screen exposure vs recovery
df['fatigue_risk'] = df['screen_time_hours'] - (df['sleep_hours'] * 1.5)

# 10. High Workload Flag - 1 if work_hours > median and meetings > median
median_hours = df['work_hours'].median()
median_meetings = df['meetings_count'].median()
df['high_workload_flag'] = ((df['work_hours'] > median_hours) & 
                             (df['meetings_count'] > median_meetings)).astype(int)

# 11. Poor Recovery Flag - 1 if sleep < 6 hours and recovery_index < 0
df['poor_recovery_flag'] = ((df['sleep_hours'] < 6) & (df['recovery_index'] < 0)).astype(int)

# 12. Burnout Risk Binary - 1 if High risk, 0 otherwise
df['high_burnout_risk_flag'] = (df['burnout_risk'] == 'High').astype(int)
df['medium_high_burnout_risk_flag'] = ((df['burnout_risk'] == 'High') | 
                                        (df['burnout_risk'] == 'Medium')).astype(int)

# 13. After-hours work intensity (absolute presence of after-hours work)
df['after_hours_work_hours_est'] = df['after_hours_work'] * (df['work_hours'] * 0.1)

# 14. Day type numeric (1 = Weekday, 0 = Weekend)
df['is_weekday'] = (df['day_type'] == 'Weekday').astype(int)

# 15. Normalized Burnout Score (0-100 scale)
min_burnout = df['burnout_score'].min()
max_burnout = df['burnout_score'].max()
df['burnout_score_normalized'] = ((df['burnout_score'] - min_burnout) / (max_burnout - min_burnout)) * 100

# 16. Screen Time per Meeting
df['screen_time_per_meeting'] = df['screen_time_hours'] / (df['meetings_count'] + 0.1)

# 17. Work-Hours Productivity 
df['work_hours_productivity'] = df['task_completion_rate'] * (1 - (df['work_hours'] / 15))

# 18. Health Risk Score - combined sleep and fatigue metric (0-100)
df['health_risk_score'] = np.clip(
    (1 - (df['sleep_hours'] / 8)) * 40 + np.maximum(0, df['fatigue_risk']) * 10,
    0, 100
)

# Reorder columns logically
column_order = [
    'user_id', 'day_type', 'is_weekday',
    # Original metrics
    'work_hours', 'screen_time_hours', 'meetings_count', 'breaks_taken', 
    'after_hours_work', 'sleep_hours', 'task_completion_rate',
    # Work Intensity Metrics
    'work_intensity_ratio', 'meeting_burden', 'break_adequacy', 'screen_time_per_meeting',
    # Workload & Pressure Metrics
    'workload_pressure', 'high_workload_flag',
    # Recovery & Health Metrics
    'sleep_deficit', 'recovery_index', 'fatigue_risk', 'health_risk_score',
    'poor_recovery_flag',
    # Productivity Metrics
    'task_efficiency', 'work_hours_productivity',
    # Balance & Wellness
    'work_life_balance_score',
    # Burnout Related
    'burnout_score', 'burnout_score_normalized', 'burnout_risk',
    'high_burnout_risk_flag', 'medium_high_burnout_risk_flag',
    # After-Hours
    'after_hours_work_hours_est'
]

df = df[column_order]

# Round numeric columns to 2 decimal places for cleaner output
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].round(2)

# Save to CSV
df.to_csv('data/work_from_home_burnout_dataset_transformed.csv', index=False)

print(f"Transformation complete!")
print(f"Original columns: 11")
print(f"New columns added: {len(column_order) - 11}")
print(f"Total columns: {len(column_order)}")
print(f"\nFile saved: data/work_from_home_burnout_dataset_transformed.csv")
