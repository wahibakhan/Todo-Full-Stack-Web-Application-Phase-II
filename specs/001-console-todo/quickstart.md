# Quick Start Guide: Console Todo Application

**Feature**: 001-console-todo
**Phase**: Phase 1 - Panaversity Hackathon II
**Date**: 2025-12-29

## Overview

This guide helps you set up, run, and develop the Console Todo Application. The app is a standalone Python console application with no external dependencies beyond Python 3.13+ standard library.

---

## Prerequisites

### Required
- **Python 3.13 or higher**
  - Check version: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/

### Optional (Development Only)
- **pytest** - For running tests
- **mypy** - For type checking
- **coverage** - For code coverage reports

---

## Installation

### 1. Clone Repository (if applicable)

```bash
git clone <repository-url>
cd todo_app
```

### 2. Verify Python Version

```bash
python --version
# Should output: Python 3.13.x or higher
```

### 3. Install Development Dependencies (Optional)

If you want to run tests or type checking:

```bash
pip install pytest mypy coverage
```

**Note**: These are development tools only. The application itself requires no dependencies beyond Python standard library.

---

## Running the Application

### Option 1: Run from Project Root

```bash
python -m src.todo_app.main
```

### Option 2: Run Directly

```bash
python src/todo_app/main.py
```

### Expected Output

```
========================================
    Console Todo App - Phase 1
========================================
In-memory only - data not saved between runs

=== Main Menu ===
1. Add task
2. List tasks
3. Update task
4. Delete task
5. Toggle complete
6. Exit

Enter choice (1-6):
```

---

## Using the Application

### Add a Task

1. Select option `1` from main menu
2. Enter task title (required, 1-200 characters)
3. Enter task description (optional, max 1000 characters, or press Enter to skip)
4. Task is created with unique ID and shown in confirmation message

**Example**:
```
Enter choice (1-6): 1

Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread

✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread

Press Enter to continue...
```

### List All Tasks

1. Select option `2` from main menu
2. All tasks are displayed in tabular format
3. Status indicators: `[ ]` = incomplete, `[x]` = complete

**Example**:
```
Enter choice (1-6): 2

=== Task List ===
ID  Status  Title                Description
--  ------  -------------------  ---------------------------
1   [ ]     Buy groceries        Milk, eggs, bread
2   [x]     Complete homework    Math assignment due Friday

Total: 2 tasks (1 incomplete, 1 completed)

Press Enter to continue...
```

### Update a Task

1. Select option `3` from main menu
2. Enter task ID
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

**Example**:
```
Enter choice (1-6): 3

Enter task ID: 1

Current task:
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread

Enter new title (or press Enter to keep current): Buy groceries and fruits
Enter new description (or press Enter to keep current): Milk, eggs, bread, apples, bananas

✓ Task updated successfully!

Press Enter to continue...
```

### Delete a Task

1. Select option `4` from main menu
2. Enter task ID
3. Confirm deletion (y/n)

**Example**:
```
Enter choice (1-6): 4

Enter task ID: 2

Task to delete:
  ID: 2
  Title: Complete homework
  Description: Math assignment due Friday

Are you sure you want to delete this task? (y/n): y

✓ Task deleted successfully!

Press Enter to continue...
```

### Toggle Task Completion

1. Select option `5` from main menu
2. Enter task ID
3. Completion status is toggled

**Example**:
```
Enter choice (1-6): 5

Enter task ID: 1

✓ Task marked as complete!
  ID: 1
  Title: Buy groceries

Press Enter to continue...
```

### Exit Application

1. Select option `6` from main menu
2. Application displays goodbye message and exits

**Example**:
```
Enter choice (1-6): 6

Thank you for using Console Todo App!
All data has been cleared from memory.
```

---

## Development Workflow

### Project Structure

```
todo_app/
├── src/
│   └── todo_app/
│       ├── __init__.py       # Package initialization
│       ├── models.py          # Task dataclass
│       ├── storage.py         # In-memory storage and CRUD
│       ├── cli.py             # CLI interface functions
│       └── main.py            # Application entry point
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py         # Task model tests
│   ├── test_storage.py        # Storage layer tests
│   ├── test_cli.py            # CLI layer tests
│   └── test_integration.py    # End-to-end tests
│
├── specs/
│   └── 001-console-todo/
│       ├── spec.md            # Feature specification
│       ├── plan.md            # Implementation plan
│       ├── research.md        # Technology decisions
│       ├── data-model.md      # Data structures
│       ├── quickstart.md      # This file
│       └── tasks.md           # Task breakdown (created by /sp.tasks)
│
└── requirements.txt           # Development dependencies (pytest, mypy)
```

### Running Tests

#### Run All Tests

```bash
pytest tests/
```

#### Run Specific Test File

```bash
pytest tests/test_storage.py
```

#### Run Tests with Coverage

```bash
coverage run -m pytest tests/
coverage report
coverage html  # Generate HTML report in htmlcov/
```

#### Expected Coverage Target

Minimum 80% coverage per Constitution requirement.

### Type Checking

```bash
mypy src/todo_app
```

Expected output: `Success: no issues found`

### Code Quality Checks

#### PEP 8 Compliance

```bash
# Install flake8 if needed
pip install flake8

# Run linting
flake8 src/todo_app
```

#### Format Code (optional)

```bash
# Install black if needed
pip install black

# Auto-format code
black src/todo_app
```

---

## Troubleshooting

### Python Version Issues

**Problem**: `python --version` shows Python 2.x or < 3.13

**Solution**: Use `python3` command or install Python 3.13+

```bash
python3 --version
python3 -m src.todo_app.main
```

### Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running from project root directory

```bash
pwd  # Verify you're in todo_app/ directory
python -m src.todo_app.main
```

### Import Errors in Tests

**Problem**: Tests can't import modules from `src/`

**Solution**: Run pytest from project root, not from `tests/` directory

```bash
# Correct (from project root)
pytest tests/

# Incorrect (from tests directory)
cd tests && pytest  # ❌ Don't do this
```

### No Data Persisted

**Problem**: Tasks disappear when I restart the application

**Solution**: This is expected behavior for Phase 1! Data is in-memory only (no persistence). This is stated in:
- Phase 1 Constitution constraint C-002
- Assumption A-005
- Welcome message when app starts

---

## Testing the Application

### Manual Test Checklist

Use this checklist to verify all features work correctly:

#### Basic Operations
- [ ] Application starts and displays welcome message
- [ ] Main menu shows all 6 options
- [ ] Empty task list displays "No tasks found"
- [ ] Add task with title only
- [ ] Add task with title and description
- [ ] List tasks shows all added tasks with correct format
- [ ] Exit option terminates application gracefully

#### CRUD Operations
- [ ] Update task title only
- [ ] Update task description only
- [ ] Update both title and description
- [ ] Update preserves ID, status, and creation time
- [ ] Delete task shows confirmation prompt
- [ ] Delete task removes it from list
- [ ] Deleted task ID is not reused for new tasks
- [ ] Toggle incomplete task to complete ([ ] → [x])
- [ ] Toggle complete task to incomplete ([x] → [ ])

#### Input Validation
- [ ] Empty title is rejected with error message
- [ ] Title > 200 characters is rejected
- [ ] Description > 1000 characters is rejected
- [ ] Invalid task ID shows error message
- [ ] Non-existent task ID shows "not found" error
- [ ] Invalid menu choice (letter, out-of-range number) shows error
- [ ] User can retry after validation error

#### Edge Cases
- [ ] Title with exactly 200 characters is accepted
- [ ] Description with exactly 1000 characters is accepted
- [ ] Title with special characters works correctly
- [ ] Update with no changes (skip both fields) works
- [ ] Delete confirmation 'n' cancels deletion
- [ ] Application handles 100 tasks without issues

---

## Common Development Tasks

### Adding a New Feature

1. Update `specs/001-console-todo/spec.md` with new requirement
2. Get human approval for spec changes
3. Update `specs/001-console-todo/plan.md` with technical approach
4. Run `/sp.tasks` to update task breakdown
5. Get human approval for updated tasks
6. Follow TDD workflow:
   - Write failing test (Red)
   - Implement feature (Green)
   - Refactor code (Refactor)
7. Verify coverage ≥ 80%
8. Update documentation as needed

### Debugging

#### Enable Debug Logging

Add to `src/todo_app/main.py`:

```python
import sys

# Add debug flag
DEBUG = '--debug' in sys.argv

if DEBUG:
    print(f"[DEBUG] Storage state: {storage._tasks}")
```

Run with: `python -m src.todo_app.main --debug`

#### Interactive Python Shell

```python
# Test components interactively
python

>>> from src.todo_app.models import Task
>>> from src.todo_app.storage import TaskStorage
>>> from datetime import datetime

>>> # Create storage and add tasks
>>> storage = TaskStorage()
>>> task = storage.add_task("Test", "Description")
>>> print(task)
>>> storage.get_all_tasks()
```

---

## Performance Expectations

Based on Success Criteria (spec.md):

- **Add task**: < 10 seconds (including user input time)
- **List tasks**: < 1 second for up to 100 tasks
- **Update/Delete/Toggle**: Near-instant (< 1 second)
- **Menu navigation**: Immediate response

All performance targets easily met with in-memory dict operations.

---

## Known Limitations (Phase 1)

These are intentional constraints, not bugs:

1. **No Data Persistence**: Tasks lost when application exits
2. **No Database**: In-memory storage only
3. **No File I/O**: Cannot save/load tasks
4. **No Web Interface**: Console only
5. **Single User**: No multi-user support or authentication
6. **No Undo**: Cannot reverse operations
7. **No Search**: Must view full list
8. **No Categories/Tags**: Flat task list only
9. **No Due Dates**: Creation timestamp only (not for deadline tracking)
10. **No Network**: Standalone application, no sync

These limitations will be addressed in Phase 2 (database) and Phase 3 (web interface).

---

## Next Steps

After verifying the application works correctly:

1. **Run Phase 1 Review**: Use `/phase1-review` skill to validate compliance
2. **Check Coverage**: Ensure tests cover ≥ 80% of code
3. **Verify Constitution**: Confirm no Phase 1 constraint violations
4. **Submit for Review**: Get human approval before Phase 2

---

## Getting Help

- **Documentation**: See `specs/001-console-todo/spec.md` for requirements
- **Architecture**: See `specs/001-console-todo/plan.md` for technical design
- **Data Model**: See `specs/001-console-todo/data-model.md` for data structures
- **Constitution**: See `.specify/memory/constitution.md` for standards

---

**Quick Start Guide Status**: ✅ COMPLETE
**Ready to Run**: ✅ YES (after implementation)
**Constitution Compliant**: ✅ VERIFIED
