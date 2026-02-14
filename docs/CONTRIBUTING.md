# 🤝 Contributing Guidelines

Thank you for considering contributing to the Employee Burnout Prediction System!

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes**:
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## How to Contribute

### Types of Contributions

1. **Bug Reports**: Found a bug? Report it!
2. **Feature Requests**: Have an idea? Suggest it!
3. **Code Contributions**: Fix bugs or add features
4. **Documentation**: Improve docs
5. **Testing**: Add or improve tests
6. **Code Review**: Review pull requests

### First Time Contributors

Look for issues labeled:
- `good first issue`: Easy issues for beginners
- `help wanted`: Issues where we need help
- `documentation`: Documentation improvements

## Development Setup

### 1. Fork and Clone

```bash
# Fork repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Employment_burnout_prediction.git
cd Employment_burnout_prediction

# Add upstream remote
git remote add upstream https://github.com/ganapathi-ai/Employment_burnout_prediction.git
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov pylint flake8 black isort pre-commit
```

### 3. Setup Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

### 4. Create Branch

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fix
git checkout -b fix/bug-description
```

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Line length: 120 characters (not 79)
# Use double quotes for strings
# Use type hints where possible

# Good
def predict_burnout(work_hours: float, sleep_hours: float) -> dict:
    """Predict burnout risk based on metrics."""
    return {"risk": "Low"}

# Bad
def predict_burnout(work_hours,sleep_hours):
    return {'risk':'Low'}
```

### Code Formatting

```bash
# Format with Black
black api/ frontend/ scripts/

# Sort imports with isort
isort api/ frontend/ scripts/

# Check with Flake8
flake8 api/ --max-line-length=120

# Lint with Pylint
pylint api/ --fail-under=7.0
```

### Naming Conventions

```python
# Variables and functions: snake_case
user_data = get_user_data()

# Classes: PascalCase
class BurnoutPredictor:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_WORK_HOURS = 24

# Private methods: _leading_underscore
def _internal_method():
    pass
```

### Documentation

```python
def engineer_features(data: UserData) -> tuple:
    """
    Engineer features from raw input data.
    
    Args:
        data (UserData): Raw user input data
        
    Returns:
        tuple: (features_array, all_features_dict)
            - features_array: numpy array of shape (1, 17)
            - all_features_dict: dictionary with all features
            
    Example:
        >>> data = UserData(work_hours=8, ...)
        >>> features, all_feats = engineer_features(data)
        >>> features.shape
        (1, 17)
    """
    # Implementation
    pass
```

### Type Hints

```python
from typing import List, Dict, Optional, Tuple

def process_data(
    data: List[Dict[str, float]],
    threshold: Optional[float] = None
) -> Tuple[List[float], Dict[str, int]]:
    """Process data with optional threshold."""
    pass
```

## Testing Guidelines

### Writing Tests

```python
# tests/test_new_feature.py
import pytest
from api.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

def test_new_feature(client):
    """Test new feature functionality."""
    # Arrange
    payload = {"key": "value"}
    
    # Act
    response = client.post("/endpoint", json=payload)
    
    # Assert
    assert response.status_code == 200
    assert "expected_key" in response.json()
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_api.py::test_health_check -v

# Run with coverage
pytest tests/ --cov=api --cov-report=html

# Run with markers
pytest tests/ -m "slow" -v
```

### Test Coverage

- Aim for **85%+ coverage**
- All new features must have tests
- Bug fixes must include regression tests

### Test Categories

```python
# Mark tests
import pytest

@pytest.mark.unit
def test_feature_engineering():
    """Unit test for feature engineering."""
    pass

@pytest.mark.integration
def test_api_database():
    """Integration test for API and database."""
    pass

@pytest.mark.slow
def test_model_training():
    """Slow test for model training."""
    pass
```

## Pull Request Process

### Before Submitting

1. ✅ **Update from upstream**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. ✅ **Run tests**
   ```bash
   pytest tests/ -v
   ```

3. ✅ **Check code quality**
   ```bash
   pylint api/ --fail-under=7.0
   flake8 api/ --max-line-length=120
   black api/ --check
   ```

4. ✅ **Update documentation**
   - Update README if needed
   - Add docstrings
   - Update CHANGELOG.md

5. ✅ **Commit with meaningful message**
   ```bash
   git add .
   git commit -m "feat: add new feature for X"
   ```

### Commit Message Format

Follow **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
feat(api): add batch prediction endpoint

Add new endpoint /predict/batch for processing multiple predictions
at once. Improves performance for bulk operations.

Closes #123

---

fix(frontend): resolve CORS error on prediction

Update CORS middleware configuration to allow requests from
frontend domain.

Fixes #456

---

docs(readme): update installation instructions

Add troubleshooting section for common installation issues.
```

### Creating Pull Request

1. **Push to your fork**
   ```bash
   git push origin your-branch
   ```

2. **Create PR on GitHub**
   - Go to original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in PR template

3. **PR Title Format**
   ```
   [Type] Brief description
   
   Examples:
   [Feature] Add batch prediction endpoint
   [Fix] Resolve database connection timeout
   [Docs] Update API documentation
   ```

4. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] Added new tests
   - [ ] Updated existing tests
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No new warnings
   
   ## Related Issues
   Closes #123
   ```

### Code Review Process

1. **Automated Checks**
   - CI/CD pipeline runs tests
   - Code quality checks (Pylint, Flake8)
   - Coverage report generated

2. **Manual Review**
   - Maintainer reviews code
   - Provides feedback
   - Requests changes if needed

3. **Addressing Feedback**
   ```bash
   # Make changes
   git add .
   git commit -m "refactor: address review comments"
   git push origin your-branch
   ```

4. **Approval and Merge**
   - Once approved, maintainer merges
   - Branch is deleted
   - Changes deployed

## Issue Guidelines

### Reporting Bugs

**Use the bug report template**:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10]
- Python: [e.g., 3.9.7]
- Browser: [e.g., Chrome 96]

## Screenshots
If applicable

## Additional Context
Any other information
```

### Feature Requests

**Use the feature request template**:

```markdown
## Feature Description
Clear description of the feature

## Problem it Solves
What problem does this solve?

## Proposed Solution
How should it work?

## Alternatives Considered
Other solutions you've considered

## Additional Context
Any other information
```

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested
- `wontfix`: This will not be worked on
- `duplicate`: This issue already exists

## Development Workflow

### Typical Workflow

```bash
# 1. Update main
git checkout main
git pull upstream main

# 2. Create branch
git checkout -b feature/new-feature

# 3. Make changes
# ... edit files ...

# 4. Test changes
pytest tests/ -v
pylint api/ --fail-under=7.0

# 5. Commit changes
git add .
git commit -m "feat: add new feature"

# 6. Push to fork
git push origin feature/new-feature

# 7. Create PR on GitHub

# 8. Address review comments
# ... make changes ...
git add .
git commit -m "refactor: address review"
git push origin feature/new-feature

# 9. Merge (done by maintainer)

# 10. Update local main
git checkout main
git pull upstream main

# 11. Delete branch
git branch -d feature/new-feature
```

### Keeping Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge into main
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

## Project Structure

When adding new files, follow this structure:

```
api/              # Backend code
frontend/         # Frontend code
scripts/          # Utility scripts
tests/            # Test files
docs/             # Documentation
models/           # ML models
data/             # Datasets
monitoring/       # Monitoring configs
.github/          # GitHub configs
```

## Documentation Standards

### README Updates

- Keep README concise
- Link to detailed docs in `docs/`
- Update badges if needed

### API Documentation

- Use docstrings for all functions
- Update API.md for new endpoints
- Include examples

### Code Comments

```python
# Good: Explain WHY, not WHAT
# Calculate work-life balance using weighted formula
# Higher weight on sleep (30%) as it's most critical
wlb_score = (sleep/8)*30 + (breaks/5)*30 - (work/10)*20

# Bad: Obvious comment
# Add 1 to counter
counter += 1
```

## Performance Guidelines

### Optimization

- Profile before optimizing
- Use appropriate data structures
- Cache expensive operations
- Minimize database queries

### Example

```python
# Bad: Multiple database queries
for user_id in user_ids:
    user = db.query(User).filter(User.id == user_id).first()
    process(user)

# Good: Single query
users = db.query(User).filter(User.id.in_(user_ids)).all()
for user in users:
    process(user)
```

## Security Guidelines

### Never Commit

- ❌ API keys
- ❌ Passwords
- ❌ Database credentials
- ❌ Private keys
- ❌ .env files

### Use Environment Variables

```python
# Good
DATABASE_URL = os.getenv("DATABASE_URL")

# Bad
DATABASE_URL = "postgresql://user:pass@host/db"
```

### Input Validation

```python
# Always validate user input
from pydantic import BaseModel, Field

class UserData(BaseModel):
    work_hours: float = Field(..., ge=0, le=24)
    # ... other fields with validation
```

## Questions?

- **Documentation**: Check `docs/` folder
- **GitHub Discussions**: Ask questions
- **Issues**: Report bugs or request features
- **Email**: Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing! 🎉
