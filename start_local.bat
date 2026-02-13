@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Initializing models...
python scripts\init_models.py

echo.
echo ========================================
echo Setup complete!
echo.
echo Start backend: python api\main.py
echo Start frontend: streamlit run frontend\streamlit_app.py
echo ========================================
pause
