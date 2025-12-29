# Implementation Plan: Console Todo Application

**Branch**: `001-console-todo` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-console-todo/spec.md`

## Summary

Phase 1 Console Todo Application is a standalone, command-line task management tool built with Python 3.13+ standard library only. The application provides five basic CRUD operations (Create, Read, Update, Delete, Toggle Complete) entirely through console interaction with in-memory storage. No databases, file persistence, web frameworks, or external integrations are permitted per Phase 1 Constitution constraints.

**Primary Technical Approach** (from research.md):
- **Architecture**: Layered architecture with strict separation of concerns (models/storage/cli/main)
- **Storage**: In-memory `dict[int, Task]` with auto-incrementing integer IDs
- **UI**: Python standard library `input()` and `print()` for console interaction
- **Testing**: pytest framework with TDD (Red-Green-Refactor) workflow
- **Validation**: Custom exceptions with layer boundary validation

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (dataclasses, datetime, typing, sys, os)
**Storage**: In-memory dict[int, Task] (no database, no file persistence)
**Testing**: pytest (development dependency only, not runtime)
**Target Platform**: Cross-platform console (Windows/Linux/macOS with Python 3.13+)
**Project Type**: Single project - standalone console application
**Performance Goals**: <1 second for list display up to 100 tasks, <10 seconds for task creation including input time
**Constraints**: Phase 1 - No databases, no web, no files, in-memory only, console-only interface
**Scale/Scope**: Single-user, up to 100 tasks per session, ~1000 lines of code total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase 1 Constraints (Constitution II) - ✅ ALL PASSED

- ✅ **C-001 (No Databases)**: Using Python dict only, no SQLite/PostgreSQL/etc.
- ✅ **C-002 (No File I/O)**: Pure in-memory storage, no JSON/pickle/CSV persistence
- ✅ **C-003 (No Web Frameworks)**: Console only with input/print, no Flask/Django/FastAPI
- ✅ **C-004 (No GUI)**: Terminal interface only, no Tkinter/PyQt
- ✅ **C-005 (No Authentication)**: Single-user, no auth/user management
- ✅ **C-006 (No External Integrations)**: Standalone application, no APIs/cloud/AI
- ✅ **C-007 (Python 3.13+ Only)**: Standard library + pytest/mypy (dev dependencies only)

**Violations**: NONE

### Code Quality Standards (Constitution III) - ✅ ALL PLANNED

- ✅ **Full Type Hints**: All public functions, methods, classes will have complete type annotations
- ✅ **Task as Dataclass**: Task model implemented as frozen dataclass with type hints
- ✅ **Module Separation**: Strict layer separation (models.py, storage.py, cli.py, main.py)
- ✅ **No Global State**: Storage passed explicitly to all functions
- ✅ **Pure Functions**: Preferred where feasible (models, validation)
- ✅ **Comprehensive Docstrings**: Google style for all modules/classes/functions
- ✅ **PEP 8 Compliance**: Enforced via linting tools
- ✅ **Defensive Programming**: Input validation with clear error messages

### TDD Standards (Constitution IV) - ✅ WORKFLOW PLANNED

- ✅ **TDD Workflow**: Red-Green-Refactor cycle planned for all features
- ✅ **80% Coverage**: Target set, measured with pytest-cov
- ✅ **CRUD Test Coverage**: All operations (add/list/update/delete/toggle) tested
- ✅ **Edge Case Tests**: Empty input, boundaries (200/1000 chars), invalid IDs
- ✅ **Error Handling Tests**: Validation errors, not-found errors
- ✅ **pytest Framework**: Selected and justified
- ✅ **Runnable from Root**: Tests run with `pytest tests/`

### Traceability (Constitution VI) - ✅ PLANNED

- ✅ **Task ID Comments**: All code will include `# Task T-XXX:` comments
- ✅ **Acceptance Criteria**: Each task will reference spec acceptance scenarios
- ✅ **File Change Tracking**: Tasks.md will document file modifications

**Gate Status**: ✅ PASSED - Zero violations, all requirements planned for compliance

---

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (implementation plan)
├── research.md          # Technology decisions and architectural patterns
├── data-model.md        # Task entity and storage structure
├── quickstart.md        # Setup and running instructions
├── contracts/           # API contracts (N/A for console app)
│   └── README.md        # Explains why contracts not applicable
├── checklists/
│   └── requirements.md  # Spec quality validation (all passed)
└── tasks.md             # Atomic task breakdown (created by /sp.tasks command)
```

### Source Code (repository root)

```text
todo_app/
├── src/
│   └── todo_app/
│       ├── __init__.py          # Package initialization
│       ├── models.py             # Task dataclass, custom exceptions
│       ├── storage.py            # TaskStorage class with CRUD operations
│       ├── cli.py                # CLI interface functions (menu, display, input)
│       └── main.py               # Application entry point and main loop
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py            # Task dataclass tests
│   ├── test_storage.py           # Storage layer tests (CRUD, validation)
│   ├── test_cli.py               # CLI layer tests (mocking input/print)
│   └── test_integration.py       # End-to-end workflow tests
│
├── .specify/
│   ├── memory/
│   │   └── constitution.md       # Phase 1 constraints and standards
│   ├── templates/
│   └── scripts/
│
├── specs/                        # Feature specifications (see above)
├── history/
│   └── prompts/
│       ├── constitution/
│       └── 001-console-todo/     # PHRs for this feature
│
├── skills/
│   └── phase1/
│       ├── phase1-init.md
│       ├── phase1-spec.md
│       └── phase1-review.md
│
├── requirements.txt              # pytest, mypy (development only)
├── .gitignore                    # Python standard ignores
├── README.md                     # Project overview
└── CLAUDE.md                     # Agent instructions
```

**Structure Decision**: **Option 1 - Single Project** selected because this is a standalone console application with no backend/frontend separation. The structure follows Constitution-mandated module separation with clear layer boundaries.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations found** - This section intentionally left empty per instruction.

All Phase 1 constraints satisfied. No complexity justifications needed.

---

## Architectural Overview

The application follows a **clean, modular, layered architecture** suitable for a console-based tool with strict separation of concerns (Constitution III):

### Layer Diagram

```
┌─────────────────────────────────────┐
│     User (Terminal Input/Output)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  CLI Layer (cli.py)                 │
│  - Display menu and prompts         │
│  - Format task list output          │
│  - Collect and validate user input  │
│  - Display error messages           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Storage Layer (storage.py)         │
│  - CRUD operations                  │
│  - Business logic validation        │
│  - Exception handling               │
│  - In-memory state management       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Models Layer (models.py)           │
│  - Task dataclass                   │
│  - Custom exceptions                │
│  - Pure data structures             │
└─────────────────────────────────────┘
               ▲
               │
┌──────────────┴──────────────────────┐
│  Application Layer (main.py)        │
│  - Entry point orchestration        │
│  - Main menu loop                   │
│  - Operation dispatch               │
│  - Exit handling                    │
└─────────────────────────────────────┘
```

### Component Breakdown

#### 1. Task Model (`src/todo_app/models.py`)

**Purpose**: Define pure data structures with no business logic or dependencies.

**Contents**:
- **Task Dataclass** (Constitution requirement):
  - Fields: `id: int`, `title: str`, `description: str`, `completed: bool`, `created_at: datetime`
  - Frozen: False (allow updates per FR-010)
  - Type hints: Full annotations on all fields
  - String representation: `__str__` for console display

- **Custom Exceptions**:
  - `TaskNotFoundError(Exception)` - Raised when ID doesn't exist
  - `ValidationError(Exception)` - Raised for invalid input

**Dependencies**: Standard library only (dataclasses, datetime)

**Test Coverage**: `tests/test_models.py`
- Dataclass creation with valid data
- Field types and defaults
- String representation

---

#### 2. In-Memory Storage (`src/todo_app/storage.py`)

**Purpose**: Manage in-memory collection and provide CRUD operations with validation.

**Contents**:
- **TaskStorage Class**:
  - State: `_tasks: dict[int, Task]`, `_next_id: int`
  - Methods:
    - `add_task(title: str, description: str = "") -> Task`
    - `get_all_tasks() -> list[Task]`
    - `get_task_by_id(task_id: int) -> Task`
    - `update_task(task_id: int, title: str | None, description: str | None) -> Task`
    - `delete_task(task_id: int) -> Task`
    - `toggle_complete(task_id: int) -> Task`

**Validation Rules** (enforced here):
- Title: Non-empty after strip, ≤ 200 characters
- Description: ≤ 1000 characters
- Task ID: Must exist in `_tasks`

**Exception Handling**:
- Raises `ValidationError` for input violations
- Raises `TaskNotFoundError` for invalid IDs

**Auto-Incrementing IDs**:
- Start at 1, increment on each add
- Never reused after deletion (FR-017)
- Gaps allowed in sequence

**Dependencies**: models.py (Task, exceptions)

**Test Coverage**: `tests/test_storage.py`
- Add with valid/invalid title and description
- Get all when empty/single/multiple tasks
- Get by valid/invalid ID
- Update with partial/full updates
- Delete and verify ID not reused
- Toggle complete multiple times
- Edge cases: boundaries, empty input, non-existent IDs

---

#### 3. CLI Interface (`src/todo_app/cli.py`)

**Purpose**: Handle user interaction, input processing, and display formatting.

**Functions** (all with type hints and docstrings):
- **Menu Display**:
  - `display_welcome()` - Welcome banner with app name and in-memory warning
  - `display_menu()` - Numbered menu with 6 options

- **Task Display**:
  - `display_task_list(tasks: list[Task])` - Formatted table with ID/Status/Title/Description
  - `display_task_details(task: Task)` - Single task display for confirmation

- **Input Collection**:
  - `get_menu_choice() -> int` - Prompt for menu selection (1-6)
  - `get_task_title() -> str` - Prompt for task title with validation
  - `get_task_description() -> str` - Prompt for optional description
  - `get_task_id() -> int` - Prompt for task ID with validation
  - `get_confirmation(message: str) -> bool` - Yes/no confirmation prompt

- **Feedback Display**:
  - `show_success(message: str)` - Success confirmation message
  - `show_error(message: str)` - Error message with retry hint
  - `show_info(message: str)` - Informational message

**Display Formatting**:
- Fixed-width columns for task list alignment
- Status indicators: `[ ]` for incomplete, `[x]` for complete
- Truncation with "..." for long titles/descriptions
- Empty state: "No tasks found" message

**Input Validation** (layer boundary):
- Menu choice: 1-6 range, numeric only
- Task ID: Positive integer only
- Title/description: Length checked in CLI, business rules in storage

**Error Handling**:
- Catches `TaskNotFoundError` and `ValidationError` from storage layer
- Displays user-friendly messages
- Allows retry without restarting app

**Dependencies**: models.py (Task), storage.py (TaskStorage, exceptions)

**Test Coverage**: `tests/test_cli.py`
- Mock `input()` and `print()` for testing
- Verify menu display format
- Test task list formatting
- Validate input collection and validation
- Error message display

---

#### 4. Application Loop (`src/todo_app/main.py`)

**Purpose**: Entry point that instantiates storage and orchestrates the main menu loop.

**Contents**:
- **Entry Point**: `if __name__ == "__main__":`
- **Storage Initialization**: `storage = TaskStorage()`
- **Main Loop**:
  - Display menu
  - Get user choice
  - Dispatch to appropriate CLI function
  - Handle storage operations
  - Loop until exit selected

**Operation Dispatch**:
- Choice 1 → Add task workflow
- Choice 2 → List tasks workflow
- Choice 3 → Update task workflow
- Choice 4 → Delete task workflow
- Choice 5 → Toggle complete workflow
- Choice 6 → Exit application

**Exit Handling**:
- Graceful exit message
- Ctrl+C handling (KeyboardInterrupt)
- Memory cleanup (implicit - Python garbage collection)

**Dependencies**: cli.py (all display/input functions), storage.py (TaskStorage)

**Test Coverage**: `tests/test_integration.py`
- End-to-end workflow tests
- Menu navigation flow
- Operation sequencing
- Exit behavior

---

## Data Flow

### Operation Flow Pattern

All CRUD operations follow this consistent pattern:

```
1. User interacts via CLI → cli.py collects input
   - Display menu/prompt
   - Get user input (menu choice, task ID, title, description)
   - Validate input format (numeric, length, non-empty)

2. CLI calls appropriate storage method
   - Pass validated input to storage layer
   - Storage performs business logic validation
   - Storage updates in-memory state

3. Storage returns result or raises exception
   - Success: Returns Task instance
   - Failure: Raises TaskNotFoundError or ValidationError

4. CLI handles result
   - Success: Display confirmation message
   - Failure: Catch exception, display error, allow retry

5. Return to main menu
   - Display menu again
   - Wait for next user choice
```

### Example: Add Task Flow

```
[User]
  ↓ Selects "1. Add task"
[main.py]
  ↓ Calls cli.display_menu(), cli.get_menu_choice()
[cli.py]
  ↓ Calls cli.get_task_title() → validates non-empty
  ↓ Calls cli.get_task_description()
  ↓ Calls storage.add_task(title, description)
[storage.py]
  ↓ Validates title length (1-200), description length (0-1000)
  ↓ Creates Task with id=_next_id, completed=False, created_at=now()
  ↓ Adds to _tasks[id], increments _next_id
  ↓ Returns Task instance
[cli.py]
  ↓ Receives Task, calls cli.show_success() with task details
  ↓ Returns to main.py
[main.py]
  ↓ Loops back to display_menu()
```

---

## Implementation Sequence

The following order ensures **incremental development** with early feedback, aligned with user story priorities (research.md):

### Phase 1: Foundation (P1 User Stories - Essential Features)

#### Task T-001: Define Task Model Dataclass
**Implements**: Task entity design, Constitution dataclass requirement
**Priority**: P1 (Foundation)
**Files Created**: `src/todo_app/__init__.py`, `src/todo_app/models.py`
**Tests Created**: `tests/__init__.py`, `tests/test_models.py`
**Acceptance Criteria**:
- Task dataclass with all 5 fields (id, title, description, completed, created_at)
- Full type hints on all fields
- `__str__` method for console display
- TaskNotFoundError and ValidationError exceptions defined

---

#### Task T-002: Implement Storage Layer with Add/List Operations
**Implements**: FR-001 through FR-009 (Task Creation, Task Retrieval)
**Priority**: P1 (Core CRUD)
**Files Created**: `src/todo_app/storage.py`
**Tests Created**: `tests/test_storage.py` (add, list, get_by_id tests)
**Acceptance Criteria**:
- TaskStorage class with `_tasks` dict and `_next_id` counter
- `add_task()` validates title/description, assigns ID, returns Task
- `get_all_tasks()` returns sorted list by ID
- `get_task_by_id()` returns Task or raises TaskNotFoundError
- Auto-incrementing IDs start at 1

---

#### Task T-003: Implement CLI Menu and Navigation
**Implements**: FR-029, FR-030, FR-031, FR-033 (User Interface), User Story 1
**Priority**: P1 (User can navigate app)
**Files Created**: `src/todo_app/cli.py`, `src/todo_app/main.py`
**Tests Created**: `tests/test_cli.py`, `tests/test_integration.py`
**Acceptance Criteria**:
- Welcome message displays app name and "in-memory only" warning
- Main menu shows all 6 options with clear numbering
- get_menu_choice() validates 1-6 range
- Exit option terminates gracefully
- Main loop returns to menu after each operation

---

#### Task T-004: Implement Add Task Workflow
**Implements**: User Story 2, FR-001 through FR-005, FR-021, FR-026
**Priority**: P1 (Core CREATE operation)
**Files Modified**: `src/todo_app/cli.py` (add `add_task_ui()` function)
**Tests Modified**: `tests/test_cli.py` (add task workflow tests)
**Acceptance Criteria**:
- Prompts for title (required) and description (optional)
- Validates title non-empty and ≤ 200 characters
- Validates description ≤ 1000 characters
- Calls storage.add_task() and displays confirmation
- Shows task ID and title in success message
- Handles ValidationError with user-friendly message

---

#### Task T-005: Implement List Tasks Display
**Implements**: User Story 3, FR-006 through FR-009
**Priority**: P1 (Core READ operation)
**Files Modified**: `src/todo_app/cli.py` (add `list_tasks_ui()` function)
**Tests Modified**: `tests/test_cli.py` (list display tests)
**Acceptance Criteria**:
- Displays tasks in tabular format with ID | Status | Title | Description
- Status indicators: `[ ]` incomplete, `[x]` complete
- Tasks ordered by ID (creation order)
- Empty list shows "No tasks found" message
- Long titles/descriptions truncated with "..." indicator

---

### Phase 2: CRUD Completion (P2 User Stories - Polish Features)

#### Task T-006: Implement Update Task Workflow
**Implements**: User Story 4, FR-010 through FR-013
**Priority**: P2 (UPDATE operation)
**Files Modified**: `src/todo_app/storage.py` (add `update_task()` method), `src/todo_app/cli.py` (add `update_task_ui()`)
**Tests Modified**: `tests/test_storage.py`, `tests/test_cli.py`
**Acceptance Criteria**:
- Prompts for task ID, shows current task details
- Prompts for new title (Enter to keep current)
- Prompts for new description (Enter to keep current)
- Validates new title/description if provided
- Preserves ID, completed status, created_at
- Handles partial updates (title only, description only, both, none)

---

#### Task T-007: Implement Toggle Complete Workflow
**Implements**: User Story 6, FR-018 through FR-020
**Priority**: P2 (Completion tracking)
**Files Modified**: `src/todo_app/storage.py` (add `toggle_complete()` method), `src/todo_app/cli.py` (add `toggle_complete_ui()`)
**Tests Modified**: `tests/test_storage.py`, `tests/test_cli.py`
**Acceptance Criteria**:
- Prompts for task ID
- Toggles completed boolean (False → True or True → False)
- Displays new status in confirmation message
- Status indicator updates in task list ([  ] ↔ [x])

---

#### Task T-008: Implement Delete Task Workflow
**Implements**: User Story 5, FR-014 through FR-017
**Priority**: P2 (DELETE operation)
**Files Modified**: `src/todo_app/storage.py` (add `delete_task()` method), `src/todo_app/cli.py` (add `delete_task_ui()`)
**Tests Modified**: `tests/test_storage.py`, `tests/test_cli.py`
**Acceptance Criteria**:
- Prompts for task ID
- Shows task details and confirmation prompt ("Are you sure? y/n")
- Deletes task if confirmed (y)
- Cancels if not confirmed (n)
- Deleted task ID never reused for new tasks
- Handles TaskNotFoundError with user-friendly message

---

### Phase 3: Validation & Polish

#### Task T-009: Implement Comprehensive Input Validation
**Implements**: FR-021 through FR-025, FR-028, Edge Cases
**Priority**: P2 (Robustness)
**Files Modified**: All CLI functions (strengthen validation)
**Tests Created**: Edge case test suite
**Acceptance Criteria**:
- Title validation: strip whitespace, check non-empty, check ≤ 200 chars
- Description validation: check ≤ 1000 chars
- Task ID validation: positive integer, exists in storage
- Menu choice validation: 1-6 range, numeric only
- Boundary tests: exactly 200 char title, exactly 1000 char description
- Special character handling in titles/descriptions

---

#### Task T-010: Implement Error Handling and Messages
**Implements**: FR-026, FR-027, FR-028
**Priority**: P2 (User experience)
**Files Modified**: `src/todo_app/cli.py` (error display functions), all operation functions
**Tests Modified**: Error handling tests
**Acceptance Criteria**:
- All exceptions caught and displayed as user-friendly messages
- Specific error messages (not generic "Error")
  - "Task ID 999 not found" (not "Error")
  - "Title cannot be empty" (not "ValidationError")
- Retry flow: after error, user can try again without restart
- Invalid menu input shows error and re-displays menu

---

#### Task T-011: Final Integration and UX Polish
**Implements**: All Success Criteria (SC-001 through SC-013)
**Priority**: P2 (Quality)
**Files Modified**: All files (refinement)
**Tests Modified**: Integration test suite
**Acceptance Criteria**:
- Performance: Add task < 10s, list < 1s for 100 tasks
- All CRUD operations work without errors
- 100% of invalid inputs get clear error messages
- Data preserved during operations (no corruption)
- Menu loop works continuously without restart
- Application handles 100 tasks without issues
- Output is well-formatted and consistent
- First-time users can add/view tasks without docs

---

## Testing Strategy

### Test-Driven Development (TDD) Workflow

**Constitution Requirement**: Red-Green-Refactor cycle (Constitution IV)

For each task:
1. **Red**: Write failing test first
   - Define expected behavior in test
   - Run test, verify it fails (no implementation yet)

2. **Green**: Implement minimal code to pass test
   - Write simplest code that makes test pass
   - Run test, verify it passes

3. **Refactor**: Improve code quality
   - Simplify logic, improve naming, reduce duplication
   - Run test again, verify it still passes

### Test Organization

```
tests/
├── test_models.py            # Task dataclass unit tests
├── test_storage.py           # Storage layer unit tests (core logic)
├── test_cli.py               # CLI layer unit tests (mocked I/O)
└── test_integration.py       # End-to-end workflow tests
```

### Test Coverage Requirements

**Target**: ≥ 80% code coverage (Constitution IV)

**Coverage by Layer**:
- Models: 100% (simple dataclass, easy to cover)
- Storage: 95%+ (all CRUD operations, edge cases, exceptions)
- CLI: 80%+ (mocked input/output, challenging to test I/O)
- Integration: End-to-end scenarios covering happy paths

**Tools**:
- `pytest` - Test runner
- `pytest-cov` - Coverage measurement
- Command: `coverage run -m pytest tests/ && coverage report`

### Test Categories

#### Unit Tests (test_models.py, test_storage.py)
- Test individual components in isolation
- Mock dependencies (e.g., datetime for timestamps)
- Fast execution (< 1 second total)

#### CLI Tests (test_cli.py)
- Mock `input()` and `print()` to test I/O functions
- Verify correct prompts displayed
- Verify correct calls to storage layer
- Test error message formatting

#### Integration Tests (test_integration.py)
- Test complete workflows end-to-end
- Example: Add task → List tasks → Update task → List again → Verify change
- Use real storage instance (in-memory, no mocking)
- Verify data consistency across operations

#### Edge Case Tests (across all test files)
- Empty title (should fail validation)
- Title with exactly 200 characters (should pass)
- Description with exactly 1000 characters (should pass)
- Title/description exceeding limits (should fail)
- Invalid task IDs (negative, non-existent, non-numeric)
- Operations on empty task list
- ID sequence after deletions (gaps preserved)
- 100 tasks performance test

---

## Dependencies & Constraints Compliance

### Required Dependencies (Runtime)

**Python Standard Library Only**:
- `dataclasses` - Task dataclass implementation
- `datetime` - Timestamp generation (created_at field)
- `typing` - Type hints (list, dict, Optional)
- `sys` - System functions (exit, argv for future CLI args)
- `os` - Operating system interface (if needed for cross-platform)

**No External Packages** - Constitution C-007 compliance

### Optional Dependencies (Development Only)

**Testing & Quality Tools**:
- `pytest` - Test framework (justified per Constitution)
- `pytest-cov` / `coverage` - Code coverage measurement
- `mypy` - Static type checking (justified per Constitution)
- `flake8` - PEP 8 linting
- `black` - Code formatting (optional)

**Installation**: `pip install pytest mypy coverage flake8 black`

**Justification**: All development tools only, not required at runtime. Application runs with Python 3.13+ standard library alone.

### Phase 1 Constraints Verified

| Constraint | Status | Implementation |
|------------|--------|----------------|
| No Databases | ✅ | Using `dict[int, Task]` in memory |
| No File I/O | ✅ | No open/read/write/pickle/json.dump to file |
| No Web Frameworks | ✅ | Console only with input/print |
| No GUI | ✅ | Terminal interface only |
| No Authentication | ✅ | Single-user, no auth logic |
| No External Integrations | ✅ | Standalone application |
| Python 3.13+ Only | ✅ | Using standard library features |

---

## Risk Mitigation

### Identified Risks (from research.md)

1. **Risk**: User enters extremely long input, causing display issues
   - **Mitigation**: Validate length limits (FR-021, FR-022), truncate display with "..."
   - **Status**: Mitigated in T-009 (input validation)

2. **Risk**: User accidentally deletes task without reading confirmation
   - **Mitigation**: Clear confirmation prompt showing task details (FR-015)
   - **Status**: Mitigated in T-008 (delete workflow)

3. **Risk**: Input validation allows edge cases (e.g., whitespace-only title)
   - **Mitigation**: Strip whitespace before validation, check non-empty after strip
   - **Status**: Mitigated in T-002 (storage validation) and T-009 (CLI validation)

4. **Risk**: User expects data persistence, loses work on exit
   - **Mitigation**: Welcome message states "In-memory only - data not saved"
   - **Status**: Mitigated in T-003 (display welcome) and documented in quickstart.md

### Non-Risks (Explicitly Out of Scope)

- **Concurrency Issues**: Single-threaded, single-user per Assumption A-001
- **Network Failures**: No network communication per Constraint C-003
- **Database Migrations**: No database per Constraint C-001
- **Authentication Vulnerabilities**: No auth per Constraint C-005

---

## Performance Considerations

### Performance Targets (from Success Criteria)

| Operation | Target | Implementation |
|-----------|--------|----------------|
| Add task | < 10 seconds (including user input) | Trivial with dict insertion O(1) |
| List tasks | < 1 second for 100 tasks | dict.values() + sort is O(n log n) ≈ 664 ops for 100 tasks |
| Update task | Near-instant | dict lookup O(1) + field assignment |
| Delete task | Near-instant | dict deletion O(1) |
| Toggle complete | Near-instant | dict lookup O(1) + boolean flip |

### Complexity Analysis

| Storage Operation | Time Complexity | Space Complexity |
|------------------|----------------|------------------|
| add_task | O(1) | O(1) |
| get_all_tasks | O(n log n) - sorting | O(n) - new list |
| get_task_by_id | O(1) - dict lookup | O(1) |
| update_task | O(1) | O(1) |
| delete_task | O(1) | O(1) |
| toggle_complete | O(1) | O(1) |

### Memory Usage

**Estimated for 100 tasks**:
- Task object: ~200 bytes (int + 2 strings + bool + datetime + overhead)
- 100 tasks: ~20 KB total
- Python dict overhead: ~10 KB
- **Total**: ~30 KB (negligible)

**No Optimization Needed**: Performance targets easily met with dict-based storage.

---

## Architectural Decision Records (ADR) Suggestions

Based on the **three-part test** (Impact, Alternatives, Scope) from Constitution:

### ADR Candidate 1: In-Memory Dict Storage vs. List Storage

**Impact**: Long-term (affects all CRUD operations)
**Alternatives**: dict[int, Task] vs. list[Task]
**Scope**: Cross-cutting (storage layer architecture)

**Suggestion**: 📋 Architectural decision detected: **In-memory storage structure (dict vs. list)**
Document reasoning and tradeoffs? Run `/sp.adr "In-Memory Storage Structure Choice"`

**Decision Preview**:
- Chosen: `dict[int, Task]` for O(1) ID lookup
- Rejected: `list[Task]` with linear search (acceptable for < 100 tasks but less future-proof)
- Rationale: O(1) lookups scale better, minimal code complexity difference

---

### ADR Candidate 2: Auto-Incrementing Integer IDs vs. UUIDs

**Impact**: Long-term (ID generation strategy affects all task references)
**Alternatives**: Integer counter vs. UUID library
**Scope**: Cross-cutting (affects storage, display, user input)

**Suggestion**: 📋 Architectural decision detected: **Task ID generation strategy (int vs. UUID)**
Document reasoning and tradeoffs? Run `/sp.adr "Task ID Generation Strategy"`

**Decision Preview**:
- Chosen: Auto-incrementing integers starting at 1
- Rejected: UUIDs (requires library, poor UX for console input)
- Rationale: User-friendly (easy to type "5" vs. "550e8400-e29b-41d4-a716-446655440000"), no library needed

---

### ADR Candidate 3: Custom Exceptions vs. Error Codes

**Impact**: Moderate (affects error handling throughout application)
**Alternatives**: Custom exception classes vs. error code returns
**Scope**: Cross-cutting (storage and CLI layers)

**Suggestion**: 📋 Architectural decision detected: **Error handling approach (exceptions vs. codes)**
Document reasoning and tradeoffs? Run `/sp.adr "Error Handling Strategy"`

**Decision Preview**:
- Chosen: Custom exception classes (TaskNotFoundError, ValidationError)
- Rejected: Error code returns (e.g., return None or (-1, "error message"))
- Rationale: Pythonic, separates happy path from error path, clearer error propagation

---

**Note**: These ADRs are **suggestions only**. User can choose to document them or proceed without ADRs if decisions are straightforward.

---

## Next Steps

### Immediate Actions (After Plan Approval)

1. ✅ **Phase 0 Complete**: research.md created with all technology decisions
2. ✅ **Phase 1 Complete**: data-model.md, contracts/, quickstart.md created
3. ✅ **Agent Context Updated**: CLAUDE.md updated with project context
4. ⏭️ **Phase 2 Next**: Run `/sp.tasks` to generate atomic task breakdown
   - Converts implementation sequence into detailed tasks.md
   - Each task will reference this plan and spec.md
   - Tasks will include acceptance criteria and file changes

### Development Workflow (After Tasks Approved)

1. **Get Human Approval** for tasks.md (Constitution requirement)
2. **Run `/sp.implement`** to execute tasks following TDD workflow
3. **For Each Task**:
   - Write tests first (Red)
   - Implement code (Green)
   - Refactor (Refactor)
   - Add task ID comments in code
   - Run tests to verify
4. **After Implementation**: Run `/phase1-review` for compliance check
5. **Submit**: Run `/sp.git.commit_pr` to commit and create pull request

### Quality Gates Before Implementation

- [ ] Specification approved by human (`spec.md` ✅ already approved)
- [ ] Plan approved by human (`plan.md` ⏭️ awaiting approval)
- [ ] Tasks approved by human (`tasks.md` ⏭️ not yet created)
- [ ] All [NEEDS CLARIFICATION] markers resolved (✅ zero found)
- [ ] Constitution compliance verified (✅ passed all gates)

---

## Summary

This implementation plan provides a complete technical blueprint for building the Phase 1 Console Todo Application while strictly adhering to Phase 1 Constitution constraints. The layered architecture with clear separation of concerns, TDD workflow, and comprehensive testing strategy ensures a high-quality, maintainable codebase.

**Key Highlights**:
- ✅ Zero Phase 1 constraint violations
- ✅ Complete layer separation (models/storage/cli/main)
- ✅ TDD workflow planned with ≥ 80% coverage target
- ✅ All 33 functional requirements mapped to tasks
- ✅ In-memory dict storage for O(1) operations
- ✅ User-friendly console interface with robust error handling
- ✅ Incremental implementation sequence aligned with user story priorities

**Plan Status**: ✅ COMPLETE - Ready for task breakdown (`/sp.tasks`)
**Constitution Compliance**: ✅ VERIFIED - All gates passed
**Approval Gate**: ⏭️ Human approval required before proceeding to `/sp.tasks`

---

**Planning Artifacts Generated**:
- `specs/001-console-todo/plan.md` - This implementation plan
- `specs/001-console-todo/research.md` - Technology decisions and patterns
- `specs/001-console-todo/data-model.md` - Task entity and storage structure
- `specs/001-console-todo/quickstart.md` - Setup and running guide
- `specs/001-console-todo/contracts/README.md` - API contracts (N/A for console)

**Next Command**: `/sp.tasks` to generate atomic task breakdown
