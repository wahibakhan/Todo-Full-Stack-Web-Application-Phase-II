# Research & Technology Decisions: Console Todo Application

**Feature**: 001-console-todo
**Date**: 2025-12-29
**Phase**: Phase 0 - Research and Technology Selection

## Overview

This document captures all technology decisions and research findings for Phase 1 Console Todo Application. Given the strict Phase 1 constraints (Python 3.13+ standard library only, no external dependencies, in-memory storage), this research phase confirms architectural patterns rather than evaluating alternative technologies.

## Technology Stack (Mandated by Phase 1 Constraints)

### Language & Runtime
- **Decision**: Python 3.13+
- **Rationale**: Mandated by Phase 1 Constitution (C-007)
- **Alternatives Considered**: None permitted - Phase 1 is Python-only
- **Justification**: Python standard library provides all necessary capabilities:
  - `dataclasses` for Task model
  - `datetime` for timestamps
  - `typing` for type hints
  - `sys` and `os` for I/O
  - Built-in `input()` and `print()` for console interaction

### Data Storage
- **Decision**: In-memory Python data structures (list or dict)
- **Rationale**: Phase 1 Constitution explicitly prohibits databases and file I/O
- **Alternatives Considered**:
  - ❌ SQLite - Violates C-001 (no databases)
  - ❌ JSON files - Violates C-002 (no file persistence)
  - ❌ Pickle - Violates C-002 (no serialization to disk)
- **Implementation Choice**: Python `dict[int, Task]` for O(1) ID lookup
  - Key: Task ID (int)
  - Value: Task dataclass instance
  - Alternative: `list[Task]` with linear search (acceptable for < 100 tasks)

### Testing Framework
- **Decision**: pytest (development dependency only, not application runtime)
- **Rationale**:
  - Industry standard for Python testing
  - Constitution explicitly permits pytest as optional justified dependency
  - Excellent support for fixtures, parametrization, and coverage reporting
- **Alternatives Considered**:
  - `unittest` (standard library) - More verbose, less expressive
  - `nose2` - Less actively maintained
- **Justification**: pytest provides better developer experience while remaining minimal

### Type Checking
- **Decision**: mypy (development dependency only)
- **Rationale**: Constitution mandates full type hints; mypy validates compliance
- **Alternatives Considered**:
  - `pyright` - Microsoft tool, equally capable
  - Manual review - Error-prone, not scalable
- **Justification**: mypy is Python community standard for static type checking

### User Interface
- **Decision**: Python standard library `input()` and `print()`
- **Rationale**: Phase 1 Constitution requires console-only interface
- **Alternatives Considered**:
  - ❌ `rich` library - External dependency, not justified for Phase 1 simplicity
  - ❌ `click` - Command-line framework, unnecessary for menu-driven interface
  - ❌ `curses` - TUI framework, adds complexity without value for simple CRUD
- **Implementation Pattern**:
  - Numbered menu system with `input()` prompts
  - Formatted output using f-strings and basic string alignment
  - No ANSI color codes (maintain portability)

## Architectural Patterns

### Module Organization
- **Decision**: Layered architecture with clear separation of concerns
- **Rationale**: Constitution (III) mandates strict module separation
- **Layers**:
  1. **Models Layer** (`src/todo_app/models.py`)
     - Pure data structures (Task dataclass)
     - No business logic, no dependencies on other layers
  2. **Storage Layer** (`src/todo_app/storage.py`)
     - Business logic for CRUD operations
     - Depends on: models
     - Encapsulates in-memory storage implementation
  3. **CLI Layer** (`src/todo_app/cli.py`)
     - User interaction logic
     - Depends on: models, storage
     - Handles input/output formatting
  4. **Application Layer** (`src/todo_app/main.py`)
     - Entry point and main loop
     - Depends on: cli, storage
     - Orchestrates application flow

### Task ID Generation
- **Decision**: Auto-incrementing integer counter
- **Rationale**:
  - Simple, predictable, user-friendly
  - No UUID library needed (keeps dependencies minimal)
  - IDs never reused after deletion (per FR-017)
- **Implementation**: Storage layer maintains `next_id` counter, incremented on each add
- **Alternatives Considered**:
  - UUID - Overkill for single-user, in-memory app
  - Timestamp-based - Non-sequential, poor UX

### Error Handling Strategy
- **Decision**: Custom exception classes + validation at layer boundaries
- **Rationale**: Clear error messages required by FR-026
- **Exceptions**:
  - `TaskNotFoundError` - Raised when ID doesn't exist
  - `ValidationError` - Raised for invalid input (title length, etc.)
- **Validation Points**:
  - CLI layer: Validate user input format (numeric ID, non-empty strings)
  - Storage layer: Validate business rules (title length, task existence)
- **Error Display**: CLI layer catches exceptions and displays user-friendly messages

### Task Completion Status
- **Decision**: Boolean `completed` field with visual indicators in display
- **Rationale**: Simple, clear, meets FR-020 requirements
- **Display Format**:
  - Incomplete: `[ ]`
  - Complete: `[x]`
- **Alternatives Considered**:
  - Enum (TODO/IN_PROGRESS/DONE) - Overly complex for Phase 1
  - String status - Type-unsafe, error-prone

## Data Model Design

### Task Entity
- **Fields** (from FR-001 through FR-005):
  - `id: int` - Unique identifier, auto-generated
  - `title: str` - Required, 1-200 characters
  - `description: str` - Optional (empty string if not provided), max 1000 characters
  - `completed: bool` - Default False
  - `created_at: datetime` - Auto-set on creation
- **Immutability**: Task dataclass with `frozen=False` (allow updates per FR-010)
- **Validation**: Performed in storage layer, not in dataclass itself

### Storage Container
- **Structure**: `dict[int, Task]`
- **Operations**:
  - Add: O(1) insertion with auto-incremented ID
  - Get by ID: O(1) lookup
  - Get all: O(n) iteration over values
  - Update: O(1) lookup + field modification
  - Delete: O(1) removal
  - Toggle: O(1) lookup + boolean flip
- **Concurrency**: Not applicable (single-threaded console app per A-001)

## Testing Strategy

### Test Organization
- **Structure**: Mirror source structure in `tests/` directory
  - `tests/test_models.py` - Task dataclass tests
  - `tests/test_storage.py` - Storage layer tests (core CRUD logic)
  - `tests/test_cli.py` - CLI layer tests (input/output, mocking)
  - `tests/test_integration.py` - End-to-end workflow tests
- **Fixtures**: Shared test data (sample tasks, storage instances)
- **Mocking**: Mock `input()` and `print()` in CLI tests

### TDD Workflow
- **Phase**: Red-Green-Refactor (per Constitution IV)
- **Test-First Examples**:
  1. Write test for add_task with valid input → Fail (red)
  2. Implement add_task logic → Pass (green)
  3. Refactor for clarity → Still pass (green)
- **Coverage Target**: ≥ 80% per Constitution
- **Edge Cases to Test**:
  - Empty title validation
  - Title/description length boundaries (200/1000 chars)
  - Invalid task IDs (negative, non-existent, non-numeric)
  - Empty task list operations
  - ID sequence after deletions

## Performance Considerations

### Scale Assumptions
- **Max Tasks**: 100 tasks per session (per A-004)
- **Response Time**: < 1 second for list display (per SC-002)
- **Memory**: Negligible with 100 tasks (~10KB total)

### Optimization Strategy
- **Not Required**: O(1) dict lookups handle 100 tasks trivially
- **Avoid Premature Optimization**: Keep code simple and readable
- **Performance Gates**: Validated in acceptance tests, not profiled

## User Experience Design

### Menu System
- **Pattern**: Numbered menu with loop-back after each operation
- **Flow**: Welcome → Menu → Operation → Confirmation → Menu → ...
- **Exit**: Explicit "Exit" option + graceful Ctrl+C handling
- **Example Menu**:
  ```
  === Console Todo App ===
  1. Add task
  2. List tasks
  3. Update task
  4. Delete task
  5. Toggle complete
  6. Exit

  Enter choice (1-6):
  ```

### Output Formatting
- **Task List Display**:
  ```
  ID  Status  Title                Description
  --  ------  -------------------  ---------------------------
  1   [ ]     Buy groceries        Milk, eggs, bread
  2   [x]     Complete homework    Math assignment due Friday
  ```
- **Alignment**: Fixed-width columns for readability
- **Truncation**: Long titles/descriptions truncated with "..." indicator
- **Empty State**: "No tasks found. Add a task to get started!"

### Error Messages
- **Format**: Clear, actionable, specific
- **Examples**:
  - "Error: Title cannot be empty. Please enter a title (1-200 characters)."
  - "Error: Task ID 999 not found. Please enter a valid task ID."
  - "Error: Invalid menu choice. Please enter a number between 1 and 6."

## Risk Assessment & Mitigation

### Identified Risks

1. **Risk**: User enters extremely long input, causing display issues
   - **Impact**: Medium - Poor UX, no data corruption
   - **Mitigation**: Validate length limits (200/1000 chars), truncate display
   - **Status**: Mitigated by FR-021, FR-022

2. **Risk**: User accidentally deletes task without reading confirmation
   - **Impact**: Low - Annoying but not catastrophic (in-memory only)
   - **Mitigation**: Clear confirmation prompt with task details shown
   - **Status**: Mitigated by FR-015

3. **Risk**: Input validation allows edge cases (e.g., whitespace-only title)
   - **Impact**: Low - Creates unusable tasks
   - **Mitigation**: Strip whitespace, validate non-empty after strip
   - **Status**: Address in storage layer validation

4. **Risk**: User expects data persistence, loses work on exit
   - **Impact**: Low - User education issue, not a bug
   - **Mitigation**: Welcome message states "In-memory only - data not saved"
   - **Status**: Documented in assumption A-005

### Non-Risks (Explicitly Out of Scope)

- **No Concurrency Issues**: Single-threaded, single-user per A-001
- **No Network Failures**: No network communication per C-003
- **No Database Migrations**: No database per C-001
- **No Authentication**: No auth per C-005

## Implementation Sequence (Informed by User Stories)

### Phase 1: Foundation (P1 User Stories)
1. **Task T-001**: Define Task model dataclass
   - Implements: Task entity design
   - Files: `src/todo_app/models.py`
   - Tests: `tests/test_models.py`

2. **Task T-002**: Implement storage layer with add/list operations
   - Implements: FR-001 through FR-009
   - Files: `src/todo_app/storage.py`
   - Tests: `tests/test_storage.py` (add, list, get_by_id)

3. **Task T-003**: Implement CLI menu and navigation
   - Implements: FR-029, FR-030, FR-031, FR-033
   - Files: `src/todo_app/cli.py`, `src/todo_app/main.py`
   - Tests: `tests/test_cli.py`, `tests/test_integration.py`

4. **Task T-004**: Implement add task workflow
   - Implements: User Story 2, FR-001 through FR-005, FR-021, FR-026
   - Files: `src/todo_app/cli.py` (add_task_ui)
   - Tests: Add validation and error handling tests

5. **Task T-005**: Implement list tasks display
   - Implements: User Story 3, FR-006 through FR-009
   - Files: `src/todo_app/cli.py` (list_tasks_ui)
   - Tests: Display formatting tests

### Phase 2: CRUD Completion (P2 User Stories)
6. **Task T-006**: Implement update task workflow
   - Implements: User Story 4, FR-010 through FR-013
   - Files: `src/todo_app/storage.py`, `src/todo_app/cli.py`
   - Tests: Update validation, partial update, preserve fields

7. **Task T-007**: Implement toggle complete workflow
   - Implements: User Story 6, FR-018 through FR-020
   - Files: `src/todo_app/storage.py`, `src/todo_app/cli.py`
   - Tests: Toggle logic, status display

8. **Task T-008**: Implement delete task workflow
   - Implements: User Story 5, FR-014 through FR-017
   - Files: `src/todo_app/storage.py`, `src/todo_app/cli.py`
   - Tests: Delete with confirmation, ID non-reuse

### Phase 3: Polish & Validation
9. **Task T-009**: Implement comprehensive input validation
   - Implements: FR-021 through FR-025, FR-028
   - Files: All CLI functions
   - Tests: Edge case suite (empty input, boundaries, invalid IDs)

10. **Task T-010**: Implement error handling and messages
    - Implements: FR-026, FR-027, FR-028
    - Files: `src/todo_app/storage.py` (exceptions), `src/todo_app/cli.py` (error display)
    - Tests: Error message clarity, retry flow

11. **Task T-011**: Final integration and UX polish
    - Implements: All success criteria (SC-001 through SC-013)
    - Files: All files (refinement)
    - Tests: Integration tests, acceptance test suite

## Constitution Compliance Verification

### Phase 1 Constraints Check
- ✅ **C-001**: No database - Using Python dict only
- ✅ **C-002**: No file I/O - Pure in-memory storage
- ✅ **C-003**: No web frameworks - Console only with input/print
- ✅ **C-004**: No GUI - Terminal interface only
- ✅ **C-005**: No authentication - Single-user, no auth
- ✅ **C-006**: No external integrations - Standalone application
- ✅ **C-007**: Python 3.13+ only - Standard library + pytest/mypy (dev only)

### Code Quality Check
- ✅ **Type hints**: All functions will have full type annotations
- ✅ **Dataclass**: Task model will be implemented as dataclass
- ✅ **Module separation**: models.py, storage.py, cli.py, main.py
- ✅ **No global state**: Storage passed explicitly
- ✅ **Docstrings**: All modules, classes, functions documented
- ✅ **PEP 8**: Enforced via linting tools

### TDD Check
- ✅ **Test-first workflow**: Red-Green-Refactor cycle planned
- ✅ **80% coverage**: Target set
- ✅ **pytest**: Selected framework
- ✅ **Edge cases**: Identified in research

## Decision Summary

| Decision Area | Choice | Rationale |
|--------------|--------|-----------|
| Language | Python 3.13+ | Constitution mandated |
| Storage | dict[int, Task] | O(1) lookup, simple, Phase 1 compliant |
| UI | input()/print() | Standard library, no dependencies |
| Testing | pytest | Industry standard, Constitution approved |
| Type Checking | mypy | Validates type hint compliance |
| Task ID | Auto-increment int | Simple, user-friendly, no libraries needed |
| Error Handling | Custom exceptions | Clear messages, layer boundary validation |
| Architecture | Layered (models/storage/cli/main) | Constitution-mandated separation |
| TDD Workflow | Red-Green-Refactor | Constitution-mandated |

## Next Steps

1. ✅ **Phase 0 Complete**: All technology decisions made, no unknowns remain
2. ⏭️ **Phase 1 Next**: Create data-model.md with detailed entity specifications
3. ⏭️ **Phase 1 Next**: Generate contracts/ (N/A for CLI app - no API contracts)
4. ⏭️ **Phase 1 Next**: Create quickstart.md with setup and running instructions
5. ⏭️ **Phase 2 After Planning**: Run `/sp.tasks` to generate atomic task breakdown
6. ⏭️ **Implementation**: Follow Red-Green-Refactor TDD cycle per Constitution

---

**Research Status**: ✅ COMPLETE - Zero unknowns, all decisions documented
**Constitution Compliance**: ✅ VERIFIED - Zero violations
**Ready for Phase 1**: ✅ YES - Proceed to data-model.md and contracts generation
