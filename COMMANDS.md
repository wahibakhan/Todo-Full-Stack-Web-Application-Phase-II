# Quick Command Reference

## Running the Application

### Windows (PowerShell)
```powershell
# Method 1: Using Python module syntax
python -m src.todo_app.main

# Method 2: Using batch file
.\run_app.bat
```

### Linux/Mac (Bash)
```bash
# Using Python module syntax
python -m src.todo_app.main

# Or with python3 explicitly
python3 -m src.todo_app.main
```

## Running Tests

### Run ALL tests
```bash
pytest tests/
```

### Run ALL tests with verbose output
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_cli.py
pytest tests/test_storage.py
pytest tests/test_models.py
pytest tests/test_integration.py
```

### Run tests with coverage
```bash
coverage run -m pytest tests/
coverage report
```

### Run tests quietly (summary only)
```bash
pytest tests/ -q
```

## Code Quality Checks

### Type checking with mypy
```bash
mypy --explicit-package-bases src/todo_app
```

### Check code formatting (if you have flake8)
```bash
pip install flake8
flake8 src/todo_app
```

## Common Issues

### ❌ ERROR: ModuleNotFoundError: No module named 'src'

**Problem**: Running test file directly
```bash
# DON'T DO THIS:
python tests/test_cli.py
python c:/projects/todo_app/tests/test_cli.py
```

**Solution**: Use pytest from project root
```bash
# DO THIS INSTEAD:
cd C:\projects\todo_app
pytest tests/test_cli.py
```

### ❌ ERROR: No module named 'pytest'

**Solution**: Install development dependencies
```bash
pip install -r requirements.txt
```

### ❌ ERROR: No module named 'coverage'

**Solution**: Install coverage
```bash
pip install coverage
```

## Development Workflow

### 1. Make changes to code
```bash
# Edit files in src/todo_app/
```

### 2. Run tests
```bash
pytest tests/ -v
```

### 3. Check coverage
```bash
coverage run -m pytest tests/
coverage report
```

### 4. Type check
```bash
mypy --explicit-package-bases src/todo_app
```

### 5. Run the app manually
```bash
python -m src.todo_app.main
```

## Project Structure

```
todo_app/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models.py       # Data models
│       ├── storage.py      # CRUD operations
│       ├── cli.py          # User interface
│       └── main.py         # Entry point
│
├── tests/
│   ├── test_models.py      # Model tests
│   ├── test_storage.py     # Storage tests
│   ├── test_cli.py         # CLI tests
│   └── test_integration.py # Integration tests
│
├── run_app.bat             # Quick launcher (Windows)
├── requirements.txt        # Dependencies
├── mypy.ini               # Type checking config
└── README.md              # Documentation
```

## Quick Start Checklist

- [ ] Install Python 3.13+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run tests: `pytest tests/`
- [ ] Check coverage: `coverage run -m pytest tests/ && coverage report`
- [ ] Type check: `mypy --explicit-package-bases src/todo_app`
- [ ] Run app: `python -m src.todo_app.main`

## Remember

✅ **Always run commands from project root**: `C:\projects\todo_app`
✅ **Use pytest for tests**, not direct Python execution
✅ **Use `-m` flag for running the app**: `python -m src.todo_app.main`
