#!/usr/bin/env python3
"""Advanced Streamlit Dashboard for Burnout Risk Prediction"""
import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime

# previously used Plotly for charts; switched to Streamlit natives
# (no external plotting library required)

# if you want to add visual libraries in future, import them here

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
        st.error("❌ API_URL not set!")
        st.stop()
else:
    API_URL = os.getenv("API_URL", "http://localhost:8000")

# Header
st.markdown('<p class="main-header">🧠 Employee Burnout Risk Analyzer</p>', unsafe_allow_html=True)
st.markdown("**AI-powered burnout prediction with comprehensive health insights**")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/mental-health.png", width=80)
    st.markdown("### 📊 System Info")
    st.caption(f"Environment: {ENVIRONMENT}")
    st.caption(f"API: {API_URL}")
    st.markdown("---")
    st.markdown("### 📖 How to Use")
    st.info("""
    1. Enter your work metrics
    2. Click 'Analyze Burnout Risk'
    3. Review personalized insights
    4. Follow recommendations
    """)
    st.markdown("---")
    st.markdown("### 🎯 Risk Levels")
    st.markdown("🟢 **Low**: Healthy balance")
    st.markdown("🟡 **Medium**: Monitor closely")
    st.markdown("🔴 **High**: Take action now")

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Input Data", "📊 Analytics", "ℹ️ About"])

with tab1:
    st.markdown("### Enter Your Work Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**⏰ Work Schedule**")
        work_hours = st.slider("Work Hours/Day", 0.0, 24.0, 8.0, 0.5, 
                               help="Total hours worked per day")
        screen_time = st.slider("Screen Time (hrs)", 0.0, 24.0, 6.0, 0.5,
                               help="Hours spent on computer/devices")
        day_type = st.selectbox("Day Type", ["Weekday", "Weekend"])
    
    with col2:
        st.markdown("**👥 Meetings & Tasks**")
        meetings = st.slider("Meetings Count", 0, 20, 3,
                            help="Number of meetings per day")
        task_completion = st.slider("Task Completion %", 0, 100, 80,
                                    help="Percentage of tasks completed")
        after_hours = st.checkbox("After-Hours Work?",
                                  help="Do you work after regular hours?")
    
    with col3:
        st.markdown("**💤 Health & Recovery**")
        sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.0, 0.5,
                               help="Hours of sleep per night")
        breaks = st.slider("Breaks Taken", 0, 10, 2,
                          help="Number of breaks during work")
    
    st.markdown("---")
    
    # Calculate derived metrics
    work_intensity = screen_time / (work_hours + 0.1)
    meeting_burden = meetings / (work_hours + 0.1)
    break_adequacy = breaks / (work_hours + 0.1)
    sleep_deficit = 8 - sleep_hours
    recovery_index = (sleep_hours + breaks) - screen_time
    
    # Display quick insights
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Work Intensity", f"{work_intensity:.2f}", 
                "High" if work_intensity > 1.2 else "Normal")
    col2.metric("Meeting Load", f"{meeting_burden:.2f}",
                "Heavy" if meeting_burden > 0.5 else "Light")
    col3.metric("Sleep Deficit", f"{sleep_deficit:.1f}h",
                "Critical" if sleep_deficit > 2 else "OK")
    col4.metric("Recovery Index", f"{recovery_index:.1f}",
                "Poor" if recovery_index < 0 else "Good")
    
    # Predict button
    if st.button("🔮 Analyze Burnout Risk", type="primary", use_container_width=True):
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
                    "day_type": day_type
                }
                
                response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    risk_level = result["risk_level"]
                    risk_prob = result["risk_probability"] * 100
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    # Risk visualization (simpler charts)
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        # show risk probability as a metric with color cue
                        risk_text = f"{risk_prob:.1f}%"
                        st.metric("Burnout Risk Score", risk_text,
                                  delta=f"{risk_prob-50:.1f}%")
                    
                    with col2:
                        st.markdown("### 📊 Risk Breakdown")
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
                        st.markdown("### 🎯 Result")
                        if risk_level == "High":
                            st.markdown(f'<p class="risk-high">⚠️ HIGH RISK</p>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<p class="risk-low">✅ LOW RISK</p>', unsafe_allow_html=True)
                        st.metric("Probability", f"{risk_prob:.1f}%")
                        st.caption(f"Analyzed at {datetime.now().strftime('%H:%M:%S')}")
                    
                    # Recommendations
                    st.markdown("---")
                    st.markdown("### 💡 Personalized Recommendations")
                    
                    recommendations = []
                    if work_hours > 10:
                        recommendations.append("⏰ **Reduce work hours**: You're working over 10 hours/day. Aim for 8-9 hours.")
                    if screen_time > 8:
                        recommendations.append("👁️ **Screen break**: Take 20-20-20 breaks (every 20 min, look 20 feet away for 20 sec)")
                    if sleep_hours < 7:
                        recommendations.append("💤 **Improve sleep**: Aim for 7-8 hours. Create a bedtime routine.")
                    if meetings > 5:
                        recommendations.append("📅 **Meeting optimization**: Too many meetings. Block focus time.")
                    if breaks < 2:
                        recommendations.append("☕ **Take breaks**: Schedule at least 3-4 short breaks during work.")
                    if after_hours:
                        recommendations.append("🚫 **Work boundaries**: Avoid after-hours work. Set clear boundaries.")
                    if recovery_index < 0:
                        recommendations.append("🔋 **Recovery time**: Your recovery is negative. Prioritize rest.")
                    
                    if not recommendations:
                        st.success("🎉 Great job! You're maintaining a healthy work-life balance!")
                    else:
                        for rec in recommendations:
                            st.warning(rec)
                    
                    # Health metrics visualization
                    st.markdown("---")
                    st.markdown("### 📈 Your Health Metrics")
                    
                    metrics_df = pd.DataFrame({
                        'Metric': ['Work Hours', 'Screen Time', 'Sleep', 'Breaks', 'Meetings'],
                        'Your Value': [work_hours, screen_time, sleep_hours, breaks, meetings],
                        'Recommended': [8, 6, 8, 4, 3]
                    })
                    st.bar_chart(metrics_df.set_index('Metric'))
                    
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    
            except requests.ConnectionError:
                st.error(f"❌ Cannot connect to API at {API_URL}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.markdown("### 📊 Burnout Analytics Dashboard")
    st.info("This section shows aggregated insights from the dataset")
    
    try:
        # ensure we load dataset relative to this file, not the cwd
        base = os.path.dirname(__file__)
        df_path = os.path.join(base, '..', 'data', 'work_from_home_burnout_dataset.csv')
        df = pd.read_csv(df_path)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Burnout distribution
            dist = df['burnout_risk'].value_counts()
            st.bar_chart(dist)
        
        with col2:
            # Average metrics by risk
            avg_metrics = df.groupby('burnout_risk')[['work_hours', 'sleep_hours', 'meetings_count']].mean()
            st.bar_chart(avg_metrics)
        
        # Correlation heatmap
        st.markdown("### 🔥 Feature Correlations")
        numeric_cols = ['work_hours', 'screen_time_hours', 'meetings_count', 'breaks_taken', 
                       'sleep_hours', 'task_completion_rate', 'burnout_score']
        corr = df[numeric_cols].corr()
        st.write(corr)
        
    except FileNotFoundError:
        st.warning("Dataset not found. Upload data to see analytics.")

with tab3:
    st.markdown("### ℹ️ About This System")
    st.markdown("""
    **Employee Burnout Risk Analyzer** uses machine learning to predict burnout risk based on work-from-home metrics.
    
    #### 🎯 Features:
    - Real-time burnout risk prediction
    - Personalized health recommendations
    - Interactive visualizations
    - Evidence-based insights
    
    #### 🤖 ML Model:
    - Algorithm: Ensemble (Random Forest / XGBoost / Gradient Boosting)
    - Features: 17 engineered features
    - Training: Real burnout dataset
    - Accuracy: ~85-90%
    
    #### 📊 Metrics Analyzed:
    - Work hours & intensity
    - Screen time exposure
    - Meeting load
    - Sleep quality
    - Recovery index
    - Task efficiency
    - Work-life balance
    
    #### 🔒 Privacy:
    - No data is stored
    - All predictions are real-time
    - Your information is private
    
    ---
    **Version**: 2.0 | **Built with**: Streamlit + FastAPI + ML
    """)

st.markdown("---")
st.caption("💡 Tip: Regular monitoring helps prevent burnout. Check your metrics weekly!")
