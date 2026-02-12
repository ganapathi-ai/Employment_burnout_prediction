-- Database Schema for Burnout Prediction System
-- File: data/schema/database_schema.sql

-- Create table for burnout records
CREATE TABLE IF NOT EXISTS burnout_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    day_type VARCHAR(10) NOT NULL,
    is_weekday INTEGER DEFAULT 0,
    work_hours DECIMAL(5,2) NOT NULL,
    screen_time_hours DECIMAL(5,2) NOT NULL,
    meetings_count INTEGER DEFAULT 0,
    breaks_taken INTEGER DEFAULT 0,
    after_hours_work INTEGER DEFAULT 0,
    sleep_hours DECIMAL(5,2) NOT NULL,
    task_completion_rate DECIMAL(5,2) NOT NULL,
    work_intensity_ratio DECIMAL(5,2),
    meeting_burden DECIMAL(5,2),
    break_adequacy DECIMAL(5,2),
    sleep_deficit DECIMAL(5,2),
    recovery_index DECIMAL(5,2),
    workload_pressure DECIMAL(5,2),
    task_efficiency DECIMAL(5,2),
    work_life_balance_score DECIMAL(5,2),
    fatigue_risk DECIMAL(5,2),
    high_workload_flag INTEGER DEFAULT 0,
    poor_recovery_flag INTEGER DEFAULT 0,
    health_risk_score DECIMAL(5,2),
    burnout_score DECIMAL(5,2) NOT NULL,
    burnout_score_normalized DECIMAL(5,2),
    burnout_risk VARCHAR(20) NOT NULL CHECK (burnout_risk IN ('Low', 'Medium', 'High')),
    high_burnout_risk_flag INTEGER DEFAULT 0,
    medium_high_burnout_risk_flag INTEGER DEFAULT 0,
    after_hours_work_hours_est DECIMAL(5,2),
    screen_time_per_meeting DECIMAL(5,2),
    work_hours_productivity DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_burnout_user_id ON burnout_records(user_id);
CREATE INDEX IF NOT EXISTS idx_burnout_risk ON burnout_records(burnout_risk);
CREATE INDEX IF NOT EXISTS idx_burnout_created_at ON burnout_records(created_at);
CREATE INDEX IF NOT EXISTS idx_burnout_score ON burnout_records(burnout_score);

-- Create view for burnout statistics
CREATE OR REPLACE VIEW burnout_statistics AS
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT user_id) as total_users,
    AVG(burnout_score) as avg_burnout_score,
    MAX(burnout_score) as max_burnout_score,
    MIN(burnout_score) as min_burnout_score,
    COUNT(CASE WHEN burnout_risk = 'High' THEN 1 END) as high_risk_count,
    COUNT(CASE WHEN burnout_risk = 'Medium' THEN 1 END) as medium_risk_count,
    COUNT(CASE WHEN burnout_risk = 'Low' THEN 1 END) as low_risk_count,
    ROUND(100.0 * COUNT(CASE WHEN burnout_risk = 'High' THEN 1 END) / COUNT(*), 2) as high_risk_percentage,
    AVG(work_hours) as avg_work_hours,
    AVG(sleep_hours) as avg_sleep_hours,
    AVG(task_completion_rate) as avg_task_completion
FROM burnout_records;

-- Sample SELECT queries

-- Get summary statistics
-- SELECT * FROM burnout_statistics;

-- Get high-risk employees
-- SELECT user_id, COUNT(*) as high_risk_days
-- FROM burnout_records
-- WHERE burnout_risk = 'High'
-- GROUP BY user_id
-- ORDER BY high_risk_days DESC;

-- Get average metrics by day type
-- SELECT day_type, AVG(work_hours), AVG(sleep_hours), AVG(burnout_score)
-- FROM burnout_records
-- GROUP BY day_type;

-- Get records for a specific user
-- SELECT * FROM burnout_records WHERE user_id = 1 ORDER BY created_at DESC;
