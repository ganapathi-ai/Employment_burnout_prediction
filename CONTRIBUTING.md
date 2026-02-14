# 🤝 Contributing Guidelines

Thank you for considering contributing to the Employee Burnout Prediction System!

## How to Contribute

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Employment_burnout_prediction.git
cd Employment_burnout_prediction
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes
- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation

### 4. Test Your Changes
```bash
# Run tests
pytest tests/ -v

# Check code quality
pylint api/ --fail-under=7.0
flake8 api/

# Test locally
python api/main.py
streamlit run frontend/streamlit_app.py
```

### 5. Commit Changes
```bash
git add -A
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve bug"
```

**Commit Message Format**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Formatting
- `chore:` Maintenance

### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create Pull Request on GitHub.

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small (<50 lines)
- Pylint score ≥7.0

### Example
```python
def calculate_risk(work_hours: float, sleep_hours: float) -> float:
    """Calculate burnout risk score.
    
    Args:
        work_hours: Daily work hours
        sleep_hours: Daily sleep hours
        
    Returns:
        Risk score between 0 and 1
    """
    risk = (work_hours / 24) - (sleep_hours / 8)
    return max(0, min(1, risk))
```

## Testing Requirements

- All new features must have tests
- Maintain >80% code coverage
- All tests must pass before PR

## Documentation

Update relevant docs:
- README.md
- API.md
- ARCHITECTURE.md
- Code comments

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add description of changes
4. Link related issues
5. Request review

## Development Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

## Questions?

Open an issue or discussion on GitHub.

---

**Thank you for contributing!** 🎉
