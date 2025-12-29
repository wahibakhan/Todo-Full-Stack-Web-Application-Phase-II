---
description: Initialize Phase 1 hackathon project structure with required directories and baseline files.
handoffs:
  - label: Create Specification
    agent: phase1-spec
    prompt: Generate the Phase 1 specification
    send: true
  - label: Review Implementation
    agent: phase1-review
    prompt: Review Phase 1 implementation for compliance
---

## User Input

```text
$ARGUMENTS
```

## Overview

Initialize the complete project structure for Phase 1 of Panaversity Hackathon II: Console Todo App. This skill sets up all required directories, configuration files, and baseline documentation following the Spec-Driven Development workflow.

## Phase 1 Requirements

Phase 1 is a **console-based Python Todo application** with these strict constraints:

- **In-memory only** - No database, no file persistence
- **Console interface** - No web UI, no GUI
- **Basic CRUD operations** - Create, Read, Update, Delete todos
- **Python implementation** - Use Python 3.x
- **Spec-Driven Development** - Must follow SDD workflow: specs → plan → tasks → approval → code

## Initialization Steps

1. **Create Directory Structure**:
   ```
   todo_app/
   ├── specs/
   │   └── phase1-console-todo/
   │       ├── spec.md
   │       ├── plan.md
   │       ├── tasks.md
   │       └── checklists/
   ├── src/
   │   └── todo_app/
   │       ├── __init__.py
   │       ├── models.py
   │       ├── todo_manager.py
   │       └── cli.py
   ├── tests/
   │   └── __init__.py
   ├── history/
   │   ├── prompts/
   │   │   ├── constitution/
   │   │   ├── general/
   │   │   └── phase1-console-todo/
   │   └── adr/
   ├── .specify/
   │   └── memory/
   │       └── constitution.md
   └── README.md
   ```

2. **Create README.md** with Phase 1 overview:
   - Project title: "Panaversity Hackathon II - Phase 1: Console Todo App"
   - Brief description of Phase 1 constraints
   - How to run the app
   - Development workflow (SDD process)

3. **Initialize Python Project**:
   - Create `requirements.txt` (if needed for testing libraries)
   - Create `.gitignore` for Python projects
   - Ensure proper Python package structure with `__init__.py` files

4. **Create Baseline Constitution** at `.specify/memory/constitution.md`:
   - Code quality principles for Python
   - Testing requirements
   - Phase 1 specific constraints (no DB, no web, in-memory only)
   - Security considerations
   - Documentation standards

5. **Set Up Git** (if not already initialized):
   - Initialize git repository
   - Create initial commit with baseline structure
   - Create `master` or `main` branch

6. **Validation Checks**:
   - Verify all directories exist
   - Verify Python package structure is correct
   - Verify `.gitignore` includes Python-specific ignores
   - Verify constitution includes Phase 1 constraints

## Output

Report the following:
- ✅ Directory structure created
- ✅ Python package initialized
- ✅ Constitution created with Phase 1 constraints
- ✅ README.md created
- ✅ Git repository initialized (if applicable)
- 📋 Next step: Run `/phase1-spec` to create the specification

## Notes

- **DO NOT** write any implementation code yet - only structure and documentation
- **DO NOT** create database files or configuration
- **DO NOT** add web framework dependencies
- Focus on setting up the proper SDD workflow structure
