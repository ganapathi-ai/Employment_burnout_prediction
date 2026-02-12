#!/usr/bin/env python3
# File: frontend/streamlit_app.py

import streamlit as st
import requests
import os
from datetime import datetime

st.set_page_config(
    page_title="Burnout Risk Predictor",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Employee Burnout Risk Predictor")
st.markdown("Predict burnout risk based on work-from-home metrics")

# API Configuration - Works for both local and Render deployment
# For Render: Set API_URL environment variable to your backend URL
# For local: Defaults to http://localhost:8000
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
if ENVIRONMENT == "production":
    API_URL = os.getenv("API_URL")  # Must be set in Render dashboard
    if not API_URL:
        st.error("❌ API_URL environment variable not set in production!")
        st.stop()
else:
    API_URL = os.getenv("API_URL", "http://localhost:8000")

# Display environment info in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("**System Info**")
    st.caption(f"Environment: {ENVIRONMENT}")
    st.caption(f"API: {API_URL}")
    st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    work_hours = st.slider("Work Hours per Day", 0.0, 24.0, 8.0, 0.5)
    screen_time = st.slider("Screen Time (hours)", 0.0, 24.0, 10.0, 0.5)
    meetings = st.slider("Number of Meetings", 0, 20, 4)
    breaks = st.slider("Breaks Taken", 0, 10, 3)

with col2:
    after_hours = st.checkbox("After-Hours Work?")
    sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.5, 0.5)
    task_completion = st.slider("Task Completion Rate (%)", 0, 100, 85)
    day_type = st.selectbox("Day Type", ["Weekday", "Weekend"])

if st.button("🔮 Predict Burnout Risk", use_container_width=True):
    try:
        payload = {
            "work_hours": work_hours,
            "screen_time_hours": screen_time,
            "meetings_count": meetings,
            "breaks_taken": breaks,
            "after_hours_work": int(after_hours),
            "sleep_hours": sleep_hours,
            "task_completion_rate": task_completion,
            "day_type": day_type
        }
        
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            st.success("✓ Prediction Complete")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Risk Level", result["risk_level"])
            with col2:
                prob = result["risk_probability"] * 100
                st.metric("Risk Probability", f"{prob:.1f}%")
            with col3:
                st.metric("Time", datetime.now().strftime("%H:%M:%S"))
            
            if result["risk_level"] == "High":
                st.warning("""
                **⚠️ High Burnout Risk Detected**
                - Reduce work hours or meetings
                - Increase breaks
                - Improve sleep schedule
                - Discuss workload with manager
                """)
            else:
                st.info("✓ Low Burnout Risk - Keep up the good balance!")
        else:
            st.error(f"API Error: {response.status_code}")
    
    except requests.ConnectionError:
        st.error(f"❌ Cannot connect to API at {API_URL}")
        st.info("Make sure FastAPI is running: `python api/main.py`")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("Built with Streamlit | ML Model v1.0")
