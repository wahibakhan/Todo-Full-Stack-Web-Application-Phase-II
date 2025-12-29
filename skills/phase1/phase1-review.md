---
description: Review Phase 1 console Todo app implementation for hackathon compliance and quality.
handoffs:
  - label: Fix Issues
    agent: sp.implement
    prompt: Fix the issues identified in the review
  - label: Commit & Create PR
    agent: sp.git.commit_pr
    prompt: Commit changes and create pull request
---

## User Input

```text
$ARGUMENTS
```

## Overview

Conduct a comprehensive compliance and quality review of the Phase 1 console Todo app implementation. This review ensures the solution meets all hackathon requirements and follows Spec-Driven Development principles.

## Review Criteria

### 1. Phase 1 Compliance Check (CRITICAL - Must Pass All)

**Constraint Validation**:
- ✅ No database imports or connections (sqlite3, sqlalchemy, etc.)
- ✅ No web framework imports (flask, django, fastapi, etc.)
- ✅ No file I/O operations (open, read, write, pickle, json.dump to file)
- ✅ In-memory storage only (Python list, dict, set, etc.)
- ✅ Console interface only (print, input, argparse, click)
- ✅ Python 3.8+ compatible

**Disqualifying Violations** (Auto-fail):
```python
# These patterns FAIL Phase 1:
import sqlite3          # ❌ Database
from flask import       # ❌ Web framework
open('file.txt', 'w')   # ❌ File persistence
with open(...)          # ❌ File I/O
pickle.dump(...)        # ❌ Serialization to disk
json.dump(..., file)    # ❌ JSON to file
```

**Allowed Patterns**:
```python
# These are OK for Phase 1:
todos = []              # ✅ In-memory list
todo_dict = {}          # ✅ In-memory dict
print("...")            # ✅ Console output
user_input = input()    # ✅ Console input
import json             # ✅ OK if only for in-memory serialization
```

### 2. Functional Requirements Review

Verify implementation of all CRUD operations:
- ✅ Create: Add new todo with description
- ✅ Read: List all todos, view single todo
- ✅ Update: Modify todo description, toggle completion status
- ✅ Delete: Remove todo by ID

**Test Coverage Requirements**:
- All CRUD operations have tests
- Edge cases covered (empty list, invalid ID, etc.)
- Error handling tested

### 3. Code Quality Review

**Python Best Practices**:
- ✅ PEP 8 compliance (formatting, naming conventions)
- ✅ Type hints used appropriately
- ✅ Docstrings for functions and classes
- ✅ No hardcoded magic values
- ✅ Error handling with meaningful messages
- ✅ Single Responsibility Principle followed

**Code Organization**:
- ✅ Proper package structure (src/todo_app/)
- ✅ Separation of concerns (models, manager, CLI)
- ✅ No circular dependencies
- ✅ Clear, descriptive variable names

### 4. User Experience Review

**Console Interface Quality**:
- ✅ Clear menu/help text
- ✅ Meaningful error messages
- ✅ User-friendly prompts
- ✅ Consistent formatting in output
- ✅ Graceful exit handling

**Edge Case Handling**:
- ✅ Empty todo list handled
- ✅ Invalid ID handled
- ✅ Invalid input validated
- ✅ Duplicate operations prevented (e.g., deleting twice)

### 5. Spec-Driven Development Compliance

**Artifact Traceability**:
- ✅ Implementation matches spec.md requirements
- ✅ All tasks in tasks.md completed
- ✅ Plan.md architecture followed
- ✅ No features outside spec scope
- ✅ All acceptance criteria met

## Review Process

1. **Read Specification Files**:
   - Read `specs/phase1-console-todo/spec.md`
   - Read `specs/phase1-console-todo/plan.md`
   - Read `specs/phase1-console-todo/tasks.md`

2. **Scan Implementation**:
   - Read all Python files in `src/todo_app/`
   - Check imports for disqualifying violations
   - Verify in-memory storage pattern
   - Check for file I/O operations

3. **Run Functional Tests**:
   - Execute test suite: `pytest tests/`
   - Verify all tests pass
   - Check test coverage (aim for 80%+)

4. **Manual Testing** (if applicable):
   - Run the application: `python src/todo_app/cli.py`
   - Test each CRUD operation
   - Verify console output quality
   - Test error handling

5. **Generate Review Report**:

   Create file: `specs/phase1-console-todo/review-report.md`

   ```markdown
   # Phase 1 Review Report

   **Date**: [ISO Date]
   **Reviewer**: Claude Code
   **Feature**: phase1-console-todo

   ## Compliance Status

   ### Phase 1 Constraints: [PASS/FAIL]
   - Database-free: [✅/❌] [Details]
   - Web-free: [✅/❌] [Details]
   - File-free: [✅/❌] [Details]
   - In-memory only: [✅/❌] [Details]
   - Console interface: [✅/❌] [Details]

   ### Functional Requirements: [PASS/FAIL]
   - Create: [✅/❌]
   - Read: [✅/❌]
   - Update: [✅/❌]
   - Delete: [✅/❌]

   ### Code Quality: [PASS/FAIL]
   - PEP 8 compliance: [✅/❌]
   - Test coverage: [XX%]
   - Documentation: [✅/❌]

   ## Issues Found

   ### Critical (Must Fix):
   [List any disqualifying violations]

   ### Major (Should Fix):
   [List quality issues]

   ### Minor (Nice to Have):
   [List improvements]

   ## Strengths
   [What was done well]

   ## Recommendations
   [Suggested improvements]

   ## Final Verdict
   - **Ready for Submission**: [YES/NO]
   - **Hackathon Score Estimate**: [X/100]
   ```

6. **Report Results**:
   - Summarize compliance status
   - List critical issues (if any)
   - Provide actionable recommendations
   - Indicate submission readiness

## Output

Provide review summary:
- ✅/❌ Phase 1 Compliance: [PASS/FAIL]
- ✅/❌ Functional Requirements: [PASS/FAIL]
- ✅/❌ Code Quality: [PASS/FAIL]
- 📊 Test Coverage: [XX%]
- 📋 Review report: `specs/phase1-console-todo/review-report.md`
- 🎯 Submission Ready: [YES/NO]

## Critical Failure Conditions

**Auto-fail scenarios** (require immediate fix):
- Any database import or usage
- Any web framework import or usage
- Any file write operations
- Any persistence mechanism (pickle, shelve, etc.)
- Missing core CRUD operations
- No tests or failing tests

## Success Indicators

**Ready for submission when**:
- All Phase 1 constraints validated
- All CRUD operations working
- Test coverage ≥ 80%
- No critical or major issues
- User experience is polished
- Spec-plan-tasks alignment verified
