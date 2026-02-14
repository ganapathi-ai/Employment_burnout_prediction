# Employee Burnout Prediction System

Advanced ML-powered system to predict employee burnout risk with interactive visualizations.

## 🚀 Features

- **Real-time Predictions**: ML model with 17 engineered features
- **Interactive Dashboard**: Gauge charts, bar charts, heatmaps
- **Personalized Insights**: Custom recommendations based on metrics
- **Analytics**: Dataset insights and correlations
- **REST API**: FastAPI backend with health monitoring
- **CI/CD**: Automated deployment with GitHub Actions
- **ML Tracking**: Live experiment tracking with Weights & Biases

## \ud83d\udcca Tech Stack

- **Backend**: FastAPI, scikit-learn, XGBoost, PostgreSQL
- **Frontend**: Streamlit
- **Deployment**: Render (Free tier)
- **CI/CD**: GitHub Actions, Docker Hub
- **ML Tracking**: Weights & Biases

## \ud83d\udee0\ufe0f Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd Employers_Burnout_prediction

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Setup W&B (optional)
wandb login
# Or set WANDB_API_KEY in .env

# Train model
python scripts/train_model.py

# Run backend
python api/main.py

# Run frontend (new terminal)
streamlit run frontend/streamlit_app.py
```

Visit:
- Backend: http://localhost:8000
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

### Deploy to Render

Follow **DEPLOYMENT.md** for complete deployment guide.

## \ud83d\udcc1 Project Structure

```
\u251c\u2500\u2500 api/                    # FastAPI backend
\u2502   \u2514\u2500\u2500 main.py            # API endpoints
\u251c\u2500\u2500 frontend/               # Streamlit dashboard
\u2502   \u2514\u2500\u2500 streamlit_app.py  # Interactive UI
\u251c\u2500\u2500 scripts/                # Utility scripts
\u2502   \u251c\u2500\u2500 train_model.py    # ML training
\u2502   \u2514\u2500\u2500 init_models.py    # Model initialization
\u251c\u2500\u2500 data/                   # Dataset
\u251c\u2500\u2500 tests/                  # Test suite
\u251c\u2500\u2500 .github/workflows/      # CI/CD pipelines
\u251c\u2500\u2500 requirements.txt        # Dependencies
\u251c\u2500\u2500 render.yaml            # Render config
\u2514\u2500\u2500 DEPLOYMENT.md          # Deployment guide
```

## \ud83e\udde0 ML Model

### Features (17 total)
- Work hours, screen time, meetings, breaks
- Sleep hours, task completion rate
- Work intensity ratio, meeting burden
- Break adequacy, sleep deficit
- Recovery index, fatigue risk
- Workload pressure, task efficiency
- Work-life balance score

### Models Tested
- Random Forest
- Gradient Boosting
- XGBoost

Best model selected automatically based on ROC-AUC score.

## \ud83d\udcca Dashboard Features

### Input Tab
- Interactive sliders for all metrics
- Real-time metric calculations
- Quick insights display

### Results
- Gauge chart for risk score
- Bar chart for risk factors
- Personalized recommendations
- Comparison with recommended values

### Analytics Tab
- Burnout risk distribution
- Average metrics by risk level
- Correlation heatmap
- Dataset statistics

## \ud83d\udd12 Security

- Environment variables for all credentials
- No hardcoded secrets in code
- .env file in .gitignore
- CORS configured properly
- Secure API endpoints

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=api --cov-report=html

# Test W&B integration
python test_wandb.py

# Lint code
flake8 api/ scripts/
pylint api/
```

## \ud83d\udce6 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Burnout prediction
- `GET /metrics` - Prometheus metrics
- `GET /docs` - Interactive API documentation

## \ud83d\udc65 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## \ud83d\udcdd License

This project is for educational purposes.

## 🔗 Links

- **Documentation**: See DEPLOYMENT.md
- **W&B Guide**: See WANDB_GUIDE.md
- **Code Verification**: See CODE_VERIFICATION_REPORT.md
- **Issues**: GitHub Issues
- **CI/CD**: GitHub Actions
- **W&B Dashboard**: https://wandb.ai/kakarlagana18-iihmr

---

**Built with \u2764\ufe0f using FastAPI, Streamlit, and Machine Learning**
<!-- trigger workflows push -->
