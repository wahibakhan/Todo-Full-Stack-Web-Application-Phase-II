# Phase 1 Skills - Console Todo App

Phase 1 custom skills for Panaversity Hackathon II: Console-based Python Todo application.

## Phase 1 Constraints (CRITICAL)

These constraints are enforced across all Phase 1 skills:

1. ❌ **No Database** - In-memory storage only (Python list/dict)
2. ❌ **No Web Interface** - Console/terminal interface only
3. ❌ **No File Persistence** - Data lost when app closes
4. ✅ **Python Console App** - Pure Python 3.8+, no GUI frameworks
5. ✅ **CRUD Operations** - Create, Read, Update, Delete todos
6. ✅ **Spec-Driven Development** - No code until specs/plan/tasks approved

## Available Skills

### 1. phase1-init.md
**Command**: `/phase1-init`

**Purpose**: Initialize Phase 1 project structure

**What it does**:
- Creates complete directory structure
- Initializes Python package with `__init__.py` files
- Creates constitution with Phase 1 constraints
- Sets up README.md and .gitignore
- Validates baseline structure

**When to use**: First step when starting Phase 1

**Next steps**: `/phase1-spec`

---

### 2. phase1-spec.md
**Command**: `/phase1-spec [requirements]`

**Purpose**: Generate Phase 1 specification

**What it does**:
- Creates `specs/phase1-console-todo/spec.md`
- Defines user stories and acceptance criteria
- Documents CRUD operations
- Creates technology-agnostic success criteria
- Generates spec quality checklist

**When to use**: After project initialization

**Next steps**: `/sp.plan` or `/sp.clarify`

**Key Validations**:
- ✅ No implementation details (classes, functions, APIs)
- ✅ Technology-agnostic success criteria
- ✅ Phase 1 constraints explicitly documented
- ✅ All CRUD operations have acceptance criteria

---

### 3. phase1-review.md
**Command**: `/phase1-review`

**Purpose**: Review implementation for hackathon compliance

**What it does**:
- Scans code for disqualifying violations
- Validates CRUD operations implementation
- Checks code quality (PEP 8, tests, docs)
- Reviews user experience
- Generates detailed review report

**When to use**: After implementation, before submission

**Next steps**: `/sp.implement` (fix issues) or `/sp.git.commit_pr` (submit)

**Critical Checks**:
```python
# Auto-fail patterns (disqualifying):
import sqlite3              # ❌ Database
from flask import           # ❌ Web framework
open('file.txt', 'w')       # ❌ File I/O
pickle.dump(...)            # ❌ Persistence

# Allowed patterns:
todos = []                  # ✅ In-memory list
print("...")                # ✅ Console output
user_input = input()        # ✅ Console input
```

**Review Report Location**: `specs/phase1-console-todo/review-report.md`

---

## Typical Phase 1 Workflow

```mermaid
graph TD
    A[/phase1-init] --> B[/phase1-spec]
    B --> C{Clarifications needed?}
    C -->|Yes| D[/sp.clarify]
    C -->|No| E[/sp.plan]
    D --> E
    E --> F[/sp.tasks]
    F --> G{Tasks approved?}
    G -->|No| F
    G -->|Yes| H[/sp.implement]
    H --> I[/phase1-review]
    I --> J{Ready for submission?}
    J -->|No - Issues found| H
    J -->|Yes - All pass| K[/sp.git.commit_pr]
```

## Compliance Checklist

Before final submission, ensure:

- [ ] ✅ No database imports or connections
- [ ] ✅ No web framework imports
- [ ] ✅ No file I/O operations (open, write, etc.)
- [ ] ✅ In-memory storage only (list, dict)
- [ ] ✅ Console interface only (print, input)
- [ ] ✅ All CRUD operations working
- [ ] ✅ Tests passing (coverage ≥ 80%)
- [ ] ✅ PEP 8 compliant
- [ ] ✅ Proper error handling
- [ ] ✅ User-friendly console messages
- [ ] ✅ Spec-plan-tasks alignment verified

## Bonus Points Opportunities

The skills help you achieve:

- **Clean Architecture**: Separation of concerns (models, manager, CLI)
- **Test Coverage**: Comprehensive tests for all CRUD operations
- **Code Quality**: PEP 8, type hints, docstrings
- **User Experience**: Clear messages, error handling
- **Documentation**: README, docstrings, comments

## Common Pitfalls (Auto-Detected by /phase1-review)

1. **Using `json.dump(data, file)`** - File persistence ❌
   - **Fix**: Use `json.dumps(data)` for in-memory only ✅

2. **Importing `sqlite3`** - Database usage ❌
   - **Fix**: Use plain Python lists/dicts ✅

3. **Using `pickle.dump()`** - File persistence ❌
   - **Fix**: Keep data in memory only ✅

4. **Missing error handling** - Poor UX
   - **Fix**: Add try-except with user-friendly messages ✅

5. **No tests** - Missing requirement
   - **Fix**: Add pytest tests for all CRUD operations ✅

## Support

For questions about these skills or Phase 1 requirements:
1. Review this README
2. Check `CLAUDE.md` for project-wide guidelines
3. Run `/phase1-review` to validate your implementation
4. Ask Claude Code for clarification

---

**Remember**: Phase 1 is about demonstrating clean, well-tested Python code that strictly adheres to the constraints. Keep it simple, follow the workflow, and let the skills guide you!
