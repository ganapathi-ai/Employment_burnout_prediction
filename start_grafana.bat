@echo off
echo ========================================
echo   Grafana Monitoring Stack Starter
echo ========================================
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not running!
    echo.
    echo Please:
    echo 1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
    echo 2. Start Docker Desktop
    echo 3. Run this script again
    pause
    exit /b 1
)

echo [OK] Docker is installed
echo.

REM Start monitoring stack
echo Starting Prometheus + Grafana...
docker-compose up -d

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start containers!
    echo.
    echo Try:
    echo   docker-compose down
    echo   docker-compose up -d
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS! Monitoring Stack Started
echo ========================================
echo.
echo Access your dashboards:
echo.
echo   Grafana:    http://localhost:3000
echo   Username:   admin
echo   Password:   admin
echo.
echo   Prometheus: http://localhost:9090
echo.
echo Next steps:
echo   1. Open http://localhost:3000 in browser
echo   2. Login with admin/admin
echo   3. Import dashboards from monitoring/grafana_dashboards.json
echo.
echo To stop:
echo   docker-compose down
echo.
echo View logs:
echo   docker logs grafana
echo   docker logs prometheus
echo.
pause
