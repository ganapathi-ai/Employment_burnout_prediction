#!/usr/bin/env python3
"""Verify database insertion is working"""
import os
os.environ['DATABASE_URL'] = 'sqlite:///./test_neon.db'

from fastapi.testclient import TestClient
from api.main import app
import sqlite3

client = TestClient(app)

# Clean start
try:
    if os.path.exists('test_neon.db'):
        os.remove('test_neon.db')
except:
    pass

print("=" * 60)
print("DATABASE INSERTION VERIFICATION")
print("=" * 60)

# Test payload
payload = {
    "work_hours": 9.5,
    "screen_time_hours": 8.0,
    "meetings_count": 5,
    "breaks_taken": 2,
    "after_hours_work": 1,
    "sleep_hours": 6.5,
    "task_completion_rate": 85.0,
    "day_type": "Weekday",
    "name": "John Doe",
    "user_id": "EMP001"
}

print("\n1. Sending prediction request...")
response = client.post("/predict", json=payload)

if response.status_code == 200:
    print("   Status: 200 OK")
    result = response.json()
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Probability: {result['risk_probability']:.2%}")
else:
    print(f"   ERROR: {response.status_code}")
    print(f"   {response.text}")
    exit(1)

# Check database
print("\n2. Checking database...")
conn = sqlite3.connect('test_neon.db')
cursor = conn.cursor()

# Get table info
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"   Tables: {[t[0] for t in tables]}")

# Get column count
cursor.execute("PRAGMA table_info(user_requests)")
columns = cursor.fetchall()
print(f"   Columns: {len(columns)}")

# Get data
cursor.execute("SELECT * FROM user_requests")
rows = cursor.fetchall()
print(f"   Records: {len(rows)}")

if rows:
    print("\n3. Verifying data...")
    row = rows[0]
    
    # Check all columns have data
    print(f"   ID: {row[0]}")
    print(f"   User ID: {row[1]}")
    print(f"   Name: {row[2]}")
    print(f"   Created At: {row[3]}")
    
    # Input features
    print(f"\n   Input Features:")
    print(f"   - work_hours: {row[4]}")
    print(f"   - screen_time_hours: {row[5]}")
    print(f"   - meetings_count: {row[6]}")
    print(f"   - breaks_taken: {row[7]}")
    print(f"   - after_hours_work: {row[8]}")
    print(f"   - sleep_hours: {row[9]}")
    print(f"   - task_completion_rate: {row[10]}")
    print(f"   - is_weekday: {row[11]}")
    
    # Engineered features
    print(f"\n   Engineered Features:")
    print(f"   - work_intensity_ratio: {row[12]}")
    print(f"   - meeting_burden: {row[13]}")
    print(f"   - break_adequacy: {row[14]}")
    print(f"   - sleep_deficit: {row[15]}")
    print(f"   - recovery_index: {row[16]}")
    print(f"   - fatigue_risk: {row[17]}")
    print(f"   - workload_pressure: {row[18]}")
    print(f"   - task_efficiency: {row[19]}")
    print(f"   - work_life_balance_score: {row[20]}")
    print(f"   - screen_time_per_meeting: {row[21]}")
    print(f"   - work_hours_productivity: {row[22]}")
    print(f"   - health_risk_score: {row[23]}")
    print(f"   - after_hours_work_hours_est: {row[24]}")
    print(f"   - high_workload_flag: {row[25]}")
    print(f"   - poor_recovery_flag: {row[26]}")
    
    # Verify no NULL values in critical columns
    null_count = sum(1 for val in row[4:] if val is None)
    print(f"\n   NULL values in data columns: {null_count}")
    
    if null_count == 0:
        print("\n" + "=" * 60)
        print("SUCCESS: All columns populated correctly!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("WARNING: Some columns have NULL values")
        print("=" * 60)
else:
    print("\n" + "=" * 60)
    print("ERROR: No data inserted!")
    print("=" * 60)

conn.close()

# Cleanup
if os.path.exists('test_neon.db'):
    os.remove('test_neon.db')
