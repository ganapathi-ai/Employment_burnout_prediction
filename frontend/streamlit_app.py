#!/usr/bin/env python3
"""Advanced Streamlit Dashboard for Burnout Risk Prediction"""
import streamlit as st
import requests
import os
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Burnout Risk Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: bold; color: #1f77b4;}
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;}
    .risk-high {color: #ff4b4b; font-weight: bold;}
    .risk-low {color: #00cc00; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# API Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
if ENVIRONMENT == "production":
    API_URL = os.getenv("API_URL")
    if not API_URL:
        st.error("API_URL not set!")
        st.stop()
else:
    API_URL = os.getenv("API_URL", "http://localhost:8000")

# Header
st.markdown('<p class="main-header">Employee Burnout Risk Analyzer</p>', unsafe_allow_html=True)
st.markdown("**AI-powered burnout prediction with comprehensive health insights**")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/mental-health.png", width=80)
    st.markdown("### System Info")
    st.caption(f"Environment: {ENVIRONMENT}")
    st.caption(f"API: {API_URL}")
    st.markdown("---")
    st.markdown("### How to Use")
    st.info("""
    1. Enter your work metrics
    2. Click 'Analyze Burnout Risk'
    3. Review personalized insights
    4. Follow recommendations
    """)
    st.markdown("---")
    st.markdown("### Risk Levels")
    st.markdown("Low: Healthy balance")
    st.markdown("Medium: Monitor closely")
    st.markdown("High: Take action now")

# Main content
tab1, tab2, tab3 = st.tabs(["Input Data", "Analytics", "About"])

with tab1:
    st.markdown("### Enter Your Work Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Work Schedule & Identity**")
        name = st.text_input("Name (optional)", "", help="Provide a name for tracking")
        user_id_input = st.text_input("User ID (optional)", "", help="Provide a user identifier")
        work_hours = st.slider("Work Hours/Day", 0.0, 24.0, 8.0, 0.5, help="Total hours worked per day")
        screen_time = st.slider("Screen Time (hrs)", 0.0, 24.0, 6.0, 0.5, help="Hours spent on computer/devices")
        day_type = st.selectbox("Day Type", ["Weekday", "Weekend"])
    
    with col2:
        st.markdown("**Meetings & Tasks**")
        meetings = st.slider("Meetings Count", 0, 20, 3, help="Number of meetings per day")
        task_completion = st.slider("Task Completion %", 0, 100, 80, help="Percentage of tasks completed")
        after_hours = st.checkbox("After-Hours Work?", help="Do you work after regular hours?")
    
    with col3:
        st.markdown("**Health & Recovery**")
        sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.0, 0.5, help="Hours of sleep per night")
        breaks = st.slider("Breaks Taken", 0, 10, 2, help="Number of breaks during work")
    
    st.markdown("---")
    
    if not name and not user_id_input:
        st.warning("Please provide either a Name or User ID for tracking.")
    
    # Load dataset medians
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'work_from_home_burnout_dataset.csv')
    try:
        df_all = pd.read_csv(dataset_path)
        median_hours = df_all['work_hours'].median()
        median_meetings = df_all['meetings_count'].median()
    except Exception:
        median_hours = 8
        median_meetings = 3

    # Calculate derived metrics
    work_intensity = screen_time / (work_hours + 0.1)
    meeting_burden = meetings / (work_hours + 0.1)
    break_adequacy = breaks / (work_hours + 0.1)
    sleep_deficit = 8 - sleep_hours
    recovery_index = (sleep_hours + breaks) - screen_time
    after_hours_num = int(after_hours)
    workload_pressure = work_hours + (meetings * 0.25) + after_hours_num
    task_efficiency = task_completion / (work_hours + 0.1)
    work_life_balance_score = np.clip(
        ((sleep_hours / 8) * 30 + (breaks / 5) * 30 - (work_hours / 10) * 20 - after_hours_num * 10) * 2,
        0, 100
    )
    fatigue_risk = screen_time - (sleep_hours * 1.5)
    high_workload_flag = int((work_hours > median_hours) and (meetings > median_meetings))
    poor_recovery_flag = int((sleep_hours < 6) and (recovery_index < 0))
    after_hours_work_hours_est = after_hours_num * (work_hours * 0.1)
    is_weekday = 1 if day_type == 'Weekday' else 0
    screen_time_per_meeting = screen_time / (meetings + 0.1)
    work_hours_productivity = task_completion * (1 - (work_hours / 15)) * 100
    health_risk_score = np.clip(
        (1 - (sleep_hours / 8)) * 40 + max(0, fatigue_risk) * 10,
        0, 100
    )

    # Display metrics
    derived_metrics = pd.DataFrame({
        'Metric': [
            'Work Intensity', 'Meeting Burden', 'Break Adequacy', 'Sleep Deficit',
            'Recovery Index', 'Workload Pressure', 'Task Efficiency',
            'Work-Life Balance Score', 'Fatigue Risk', 'High Workload Flag',
            'Poor Recovery Flag', 'After-hours Intensity', 'Day is Weekday',
            'Screen Time/Meeting', 'Work Hours Productivity', 'Health Risk Score'
        ],
        'Value': [
            work_intensity, meeting_burden, break_adequacy, sleep_deficit,
            recovery_index, workload_pressure, task_efficiency,
            work_life_balance_score, fatigue_risk, high_workload_flag,
            poor_recovery_flag, after_hours_work_hours_est, is_weekday,
            screen_time_per_meeting, work_hours_productivity, health_risk_score
        ]
    })

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Work Intensity", f"{work_intensity:.2f}", "High" if work_intensity > 1.2 else "Normal")
    col2.metric("Meeting Load", f"{meeting_burden:.2f}", "Heavy" if meeting_burden > 0.5 else "Light")
    col3.metric("Sleep Deficit", f"{sleep_deficit:.1f}h", "Critical" if sleep_deficit > 2 else "OK")
    col4.metric("Recovery Index", f"{recovery_index:.1f}", "Poor" if recovery_index < 0 else "Good")

    st.markdown("#### All Derived Metrics")
    st.table(derived_metrics.set_index('Metric').round(2))
    
    # Predict button
    if st.button("Analyze Burnout Risk", type="primary", use_container_width=True):
        if not name and not user_id_input:
            st.error("Cannot analyze without at least a name or user ID.")
        else:
            with st.spinner("Analyzing your data..."):
                try:
                    payload = {
                        "work_hours": work_hours,
                        "screen_time_hours": screen_time,
                        "meetings_count": meetings,
                        "breaks_taken": breaks,
                        "after_hours_work": int(after_hours),
                        "sleep_hours": sleep_hours,
                        "task_completion_rate": task_completion,
                        "day_type": day_type,
                        "name": name or None,
                        "user_id": user_id_input or None
                    }
                    
                    response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        risk_level = result["risk_level"]
                        risk_prob = result["risk_probability"] * 100
                        api_features = result.get("features", {})
                        
                        st.success("Analysis Complete!")
                        
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            risk_text = f"{risk_prob:.1f}%"
                            st.metric("Burnout Risk Score", risk_text, delta=f"{risk_prob-50:.1f}%")
                        
                        with col2:
                            st.markdown("### Risk Breakdown")
                            risk_factors = pd.DataFrame({
                                'Factor': ['Work Load', 'Screen Time', 'Sleep Quality', 'Recovery', 'Meetings'],
                                'Score': [
                                    min(100, (work_hours / 12) * 100),
                                    min(100, (screen_time / 10) * 100),
                                    max(0, 100 - (sleep_hours / 8) * 100),
                                    max(0, 100 - ((recovery_index + 10) / 20) * 100),
                                    min(100, (meetings / 10) * 100)
                                ]
                            })
                            st.bar_chart(risk_factors.set_index('Factor'))
                        
                        with col3:
                            st.markdown("### Result")
                            if risk_level == "High":
                                st.markdown('<p class="risk-high">HIGH RISK</p>', unsafe_allow_html=True)
                            else:
                                st.markdown('<p class="risk-low">LOW RISK</p>', unsafe_allow_html=True)
                            st.metric("Probability", f"{risk_prob:.1f}%")
                            st.caption(f"Analyzed at {datetime.now().strftime('%H:%M:%S')}")
                        
                        if api_features:
                            st.markdown("---")
                            st.markdown("### Engineered Features from API")
                            
                            # Create readable labels
                            feature_labels = {
                                'work_hours': 'Work Hours',
                                'screen_time_hours': 'Screen Time Hours',
                                'meetings_count': 'Meetings Count',
                                'breaks_taken': 'Breaks Taken',
                                'after_hours_work': 'After Hours Work',
                                'sleep_hours': 'Sleep Hours',
                                'task_completion_rate': 'Task Completion Rate',
                                'is_weekday': 'Is Weekday',
                                'work_intensity_ratio': 'Work Intensity Ratio',
                                'meeting_burden': 'Meeting Burden',
                                'break_adequacy': 'Break Adequacy',
                                'sleep_deficit': 'Sleep Deficit',
                                'recovery_index': 'Recovery Index',
                                'fatigue_risk': 'Fatigue Risk',
                                'workload_pressure': 'Workload Pressure',
                                'task_efficiency': 'Task Efficiency',
                                'work_life_balance_score': 'Work Life Balance Score',
                                'screen_time_per_meeting': 'Screen Time Per Meeting',
                                'work_hours_productivity': 'Work Hours Productivity',
                                'health_risk_score': 'Health Risk Score',
                                'after_hours_work_hours_est': 'After Hours Work Hours Est',
                                'high_workload_flag': 'High Workload Flag',
                                'poor_recovery_flag': 'Poor Recovery Flag',
                                'name': 'Name',
                                'user_id': 'User ID'
                            }
                            
                            # Create DataFrame with readable labels
                            feat_data = {feature_labels.get(k, k): [v] for k, v in api_features.items()}
                            feat_df = pd.DataFrame(feat_data).T
                            feat_df.columns = ['Value']
                            feat_df = feat_df.round(2)
                            st.table(feat_df)

                        st.markdown("---")
                        st.markdown("### Personalized Recommendations")
                        
                        recommendations = []
                        if work_hours > 10:
                            recommendations.append("**Reduce work hours**: You're working over 10 hours/day. Aim for 8-9 hours.")
                        if screen_time > 8:
                            recommendations.append("**Screen break**: Take 20-20-20 breaks (every 20 min, look 20 feet away for 20 sec)")
                        if sleep_hours < 7:
                            recommendations.append("**Improve sleep**: Aim for 7-8 hours. Create a bedtime routine.")
                        if meetings > 5:
                            recommendations.append("**Meeting optimization**: Too many meetings. Block focus time.")
                        if breaks < 2:
                            recommendations.append("**Take breaks**: Schedule at least 3-4 short breaks during work.")
                        if after_hours:
                            recommendations.append("**Work boundaries**: Avoid after-hours work. Set clear boundaries.")
                        if recovery_index < 0:
                            recommendations.append("**Recovery time**: Your recovery is negative. Prioritize rest.")
                        
                        if not recommendations:
                            st.success("Great job! You're maintaining a healthy work-life balance!")
                        else:
                            for rec in recommendations:
                                st.warning(rec)
                        
                        st.markdown("---")
                        st.markdown("### Your Health Metrics")
                        
                        metrics_df = pd.DataFrame({
                            'Metric': ['Work Hours', 'Screen Time', 'Sleep', 'Breaks', 'Meetings'],
                            'Your Value': [work_hours, screen_time, sleep_hours, breaks, meetings],
                            'Recommended': [8, 6, 8, 4, 3]
                        })
                        st.bar_chart(metrics_df.set_index('Metric'))
                        
                    else:
                        st.error(f"API Error: {response.status_code}")
                        
                except requests.ConnectionError:
                    st.error(f"Cannot connect to API at {API_URL}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.markdown("### Burnout Analytics Dashboard")
    st.info("This section shows aggregated insights from the dataset")
    
    try:
        base = os.path.dirname(__file__)
        df_path = os.path.join(base, '..', 'data', 'work_from_home_burnout_dataset_transformed.csv')
        if not os.path.exists(df_path):
            df_path = os.path.join(base, '..', 'data', 'work_from_home_burnout_dataset.csv')
        df = pd.read_csv(df_path)
        
        col1, col2 = st.columns(2)
        
        with col1:
            dist = df['burnout_risk'].value_counts()
            st.bar_chart(dist)
        
        with col2:
            metrics = ['work_hours', 'sleep_hours', 'meetings_count']
            for extra in ['work_intensity_ratio', 'meeting_burden', 'break_adequacy',
                          'recovery_index', 'work_life_balance_score']:
                if extra in df.columns:
                    metrics.append(extra)
            avg_metrics = df.groupby('burnout_risk')[metrics].mean()
            st.bar_chart(avg_metrics)
        
        st.markdown("### Feature Correlations")
        numeric_cols = ['work_hours', 'screen_time_hours', 'meetings_count', 'breaks_taken', 
                       'sleep_hours', 'task_completion_rate', 'burnout_score']
        for extra in ['work_intensity_ratio', 'meeting_burden', 'break_adequacy',
                      'sleep_deficit', 'recovery_index', 'workload_pressure',
                      'task_efficiency', 'work_life_balance_score', 'fatigue_risk',
                      'health_risk_score']:
            if extra in df.columns:
                numeric_cols.append(extra)
        corr = df[numeric_cols].corr()
        st.write(corr)
        
    except FileNotFoundError:
        st.warning("Dataset not found. Upload data to see analytics.")

with tab3:
    st.markdown("### About This System")
    st.markdown("""
    **Employee Burnout Risk Analyzer** uses machine learning to predict burnout risk based on work-from-home metrics.
    
    #### Features:
    - Real-time burnout risk prediction
    - Personalized health recommendations
    - Interactive visualizations
    - Evidence-based insights
    
    #### ML Model:
    - Algorithm: Ensemble (Random Forest / XGBoost / Gradient Boosting)
    - Features: 17 engineered features
    - Training: Real burnout dataset
    - Accuracy: ~85-90%
    
    #### Metrics Analyzed:
    - Work hours & intensity
    - Screen time exposure
    - Meeting load
    - Sleep quality
    - Recovery index
    - Task efficiency
    - Work-life balance
    
    #### Privacy:
    - Data stored in Neon PostgreSQL
    - All predictions are real-time
    - Secure API endpoints
    
    ---
    **Version**: 2.0 | **Built with**: Streamlit + FastAPI + ML
    """)

st.markdown("---")
st.caption("Tip: Regular monitoring helps prevent burnout. Check your metrics weekly!")
