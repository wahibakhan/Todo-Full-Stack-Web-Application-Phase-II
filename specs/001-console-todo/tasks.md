---
description: "Atomic task breakdown for Phase 1 Console Todo Application"
---

# Tasks: Phase 1 Console Todo Application

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md, spec.md (user stories), data-model.md, research.md

**Tests**: Tasks include TDD test tasks per Constitution IV requirement (Red-Green-Refactor cycle, ≥80% coverage)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Single Python project structure per plan.md:
- **Source**: `src/todo_app/` (models.py, storage.py, cli.py, main.py)
- **Tests**: `tests/` (test_models.py, test_storage.py, test_cli.py, test_integration.py)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project structure and Python package initialization

- [ ] T-001 Create project directory structure (src/todo_app/, tests/, specs/)
- [ ] T-002 [P] Create Python package files: src/todo_app/__init__.py, tests/__init__.py
- [ ] T-003 [P] Create requirements.txt with dev dependencies (pytest>=8.0, mypy>=1.0, coverage>=7.0)
- [ ] T-004 [P] Configure mypy.ini with strict type checking (per Constitution III)

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and exceptions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundation (TDD: Write tests FIRST, ensure they FAIL)

- [ ] T-005 [P] [Foundation] Unit tests for Task dataclass in tests/test_models.py (field types, immutability, string representation)
- [ ] T-006 [P] [Foundation] Unit tests for custom exceptions in tests/test_models.py (TaskNotFoundError, ValidationError)

### Foundation Implementation

- [ ] T-007 [Foundation] Implement Task dataclass in src/todo_app/models.py (5 fields: id, title, description, completed, created_at per data-model.md)
- [ ] T-008 [P] [Foundation] Implement TaskNotFoundError exception in src/todo_app/models.py
- [ ] T-009 [P] [Foundation] Implement ValidationError exception in src/todo_app/models.py

**Checkpoint**: Run tests (T-005, T-006) - should PASS. Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First Launch and Navigation (Priority: P1) 🎯 MVP

**Goal**: User sees welcome message, main menu with 6 options, and can navigate/exit cleanly

**Independent Test**: Run `python -m src.todo_app.main`, verify menu displays, select option 6 to exit gracefully

### Tests for User Story 1 (TDD: Write tests FIRST, ensure they FAIL)

- [ ] T-010 [P] [US1] Unit tests for display_welcome() in tests/test_cli.py (verify banner text, in-memory warning)
- [ ] T-011 [P] [US1] Unit tests for display_menu() in tests/test_cli.py (verify 6 menu options displayed)
- [ ] T-012 [P] [US1] Unit tests for get_menu_choice() in tests/test_cli.py (valid input 1-6, invalid input handling, type conversion)
- [ ] T-013 [US1] Integration test for main loop in tests/test_integration.py (menu display → exit workflow)

### Implementation for User Story 1

- [ ] T-014 [P] [US1] Implement display_welcome() in src/todo_app/cli.py (welcome banner, in-memory notice per FR-001)
- [ ] T-015 [P] [US1] Implement display_menu() in src/todo_app/cli.py (6 options: Add/List/Update/Delete/Toggle/Exit per FR-002)
- [ ] T-016 [US1] Implement get_menu_choice() in src/todo_app/cli.py (input validation 1-6, error handling per FR-003)
- [ ] T-017 [US1] Implement main loop in src/todo_app/main.py (menu display → route command → repeat until exit per FR-033)
- [ ] T-018 [US1] Add clean exit handling in src/todo_app/main.py (Ctrl+C, option 6, goodbye message per FR-032)

**Checkpoint**: Run `python -m src.todo_app.main` - Menu displays, navigation works, exit is clean. All US1 tests PASS.

---

## Phase 4: User Story 2 - Adding New Tasks (Priority: P1) 🎯 MVP

**Goal**: User can add tasks with title (required) and optional description, see confirmation

**Independent Test**: Run app, select "Add task", enter title "Buy groceries", description "Milk, eggs", verify confirmation shows ID=1

### Tests for User Story 2 (TDD: Write tests FIRST, ensure they FAIL)

- [ ] T-019 [P] [US2] Unit tests for TaskStorage.__init__() in tests/test_storage.py (verify _tasks={}, _next_id=1)
- [ ] T-020 [P] [US2] Unit tests for TaskStorage.add_task() in tests/test_storage.py (valid title, optional description, ID assignment, validation errors per data-model.md)
- [ ] T-021 [P] [US2] Unit tests for input validation in tests/test_storage.py (empty title rejected, title>200 rejected, description>1000 rejected per FR-021, FR-022)
- [ ] T-022 [US2] Unit tests for add_task_ui() in tests/test_cli.py (prompt for title/description, display confirmation, retry on validation error per FR-023, FR-024)

### Implementation for User Story 2

- [ ] T-023 [US2] Implement TaskStorage class initialization in src/todo_app/storage.py (_tasks: dict[int, Task], _next_id: int)
- [ ] T-024 [US2] Implement TaskStorage.add_task(title, description) in src/todo_app/storage.py (validation, ID generation, Task creation per data-model.md lines 127-158)
- [ ] T-025 [US2] Implement add_task_ui() in src/todo_app/cli.py (prompt title, prompt description, call storage.add_task(), display confirmation per FR-004)
- [ ] T-026 [US2] Integrate add_task_ui() into main loop in src/todo_app/main.py (route option 1 to add_task_ui)
- [ ] T-027 [US2] Add error handling for validation failures in src/todo_app/cli.py (catch ValidationError, display message, allow retry per FR-023)

**Checkpoint**: Run app, add 3 tasks with various titles/descriptions, verify IDs increment (1, 2, 3), validation errors handled. All US2 tests PASS.

---

## Phase 5: User Story 3 - Viewing Task List (Priority: P1) 🎯 MVP

**Goal**: User can view all tasks in tabular format with ID, status, title, description

**Independent Test**: Run app, add 2 tasks (1 incomplete, 1 complete), select "List tasks", verify table format with status indicators [ ] and [x]

### Tests for User Story 3 (TDD: Write tests FIRST, ensure they FAIL)

- [ ] T-028 [P] [US3] Unit tests for TaskStorage.get_all_tasks() in tests/test_storage.py (empty list, single task, multiple tasks, sorted by ID per FR-009)
- [ ] T-029 [P] [US3] Unit tests for format_task_list() in tests/test_cli.py (table headers, status indicators [ ]/[x], empty list message per FR-006, FR-008)
- [ ] T-030 [US3] Unit tests for display_task_summary() in tests/test_cli.py (total count, incomplete count, completed count per FR-030)

### Implementation for User Story 3

- [ ] T-031 [US3] Implement TaskStorage.get_all_tasks() in src/todo_app/storage.py (return sorted list[Task] by ID per data-model.md lines 161-179)
- [ ] T-032 [US3] Implement format_task_list() in src/todo_app/cli.py (table format: ID, Status, Title, Description per FR-007)
- [ ] T-033 [US3] Implement display_task_summary() in src/todo_app/cli.py (count total/incomplete/completed tasks per FR-030)
- [ ] T-034 [US3] Implement list_tasks_ui() in src/todo_app/cli.py (call get_all_tasks, format table, display summary, handle empty list per FR-006)
- [ ] T-035 [US3] Integrate list_tasks_ui() into main loop in src/todo_app/main.py (route option 2 to list_tasks_ui)

**Checkpoint**: Run app, add multiple tasks, list them, verify table format correct, status indicators work, summary accurate. All US3 tests PASS. **MVP COMPLETE** (P1 features: navigate, add, list)

---

## Phase 6: User Story 4 - Updating Task Details (Priority: P2)

**Goal**: User can update title and/or description of existing tasks by ID

**Independent Test**: Run app, add task ID=1 "Old title", update to "New title", verify change persists in list

### Tests for User Story 4 (TDD: Write tests FIRST, ensure they FAIL)

- [ ] T-036 [P] [US4] Unit tests for TaskStorage.get_task_by_id() in tests/test_storage.py (valid ID returns task, invalid ID raises TaskNotFoundError per data-model.md lines 182-206)
- [ ] T-037 [P] [US4] Unit tests for TaskStorage.update_task() in tests/test_storage.py (update title only, description only, both, preserve id/completed/created_at, validation per data-model.md lines 209-246)
- [ ] T-038 [US4] Unit tests for update_task_ui() in tests/test_cli.py (prompt ID, show current task, prompt new values, skip if empty, display confirmation per FR-010, FR-012)

### Implementation for User Story 4

- [ ] T-039 [US4] Implement TaskStorage.get_task_by_id(task_id) in src/todo_app/storage.py (O(1) dict lookup, raise TaskNotFoundError if missing per data-model.md)
- [ ] T-040 [US4] Implement TaskStorage.update_task(task_id, title, description) in src/todo_app/storage.py (partial update, validation, preserve immutable fields per FR-011)
- [ ] T-041 [US4] Implement update_task_ui() in src/todo_app/cli.py (prompt ID, show current task, prompt changes, call storage.update_task(), display confirmation per FR-010)
- [ ] T-042 [US4] Integrate update_task_ui() into main loop in src/todo_app/main.py (route option 3 to update_task_ui)
- [ ] T-043 [US4] Add error handling for TaskNotFoundError in src/todo_app/cli.py (display "Task not found" message, allow retry per FR-027)

**Checkpoint**: Run app, update tasks by ID, verify partial updates work, invalid IDs rejected, immutable fields preserved. All US4 tests PASS.

---

## Phase 7: User Story 5 - Deleting Unwanted Tasks (Priority: P2)

**Goal**: User can delete tasks by ID with confirmation prompt

**Independent Test**: Run app, add task ID=1, delete it with confirmation 'y', verify it's removed from list and ID not reused

### Tests for User Story 5 (TDD: Write tests FIRST, ensure they FAIL)

- [ ] T-044 [P] [US5] Unit tests for TaskStorage.delete_task() in tests/test_storage.py (valid ID deletes task, invalid ID raises error, ID not reused per FR-017, data-model.md lines 249-276)
- [ ] T-045 [US5] Unit tests for delete_task_ui() in tests/test_cli.py (prompt ID, show task preview, confirm y/n, delete on 'y', cancel on 'n' per FR-014, FR-015)

### Implementation for User Story 5

- [ ] T-046 [US5] Implement TaskStorage.delete_task(task_id) in src/todo_app/storage.py (remove from dict, return deleted task, do NOT decrement _next_id per FR-017)
- [ ] T-047 [US5] Implement delete_task_ui() in src/todo_app/cli.py (prompt ID, display task preview, confirm deletion, call storage.delete_task(), display confirmation per FR-013)
- [ ] T-048 [US5] Implement confirmation prompt in src/todo_app/cli.py (y/n input, case insensitive, allow cancellation per FR-015)
- [ ] T-049 [US5] Integrate delete_task_ui() into main loop in src/todo_app/main.py (route option 4 to delete_task_ui)

**Checkpoint**: Run app, delete tasks, verify confirmation required, deletion works, cancelled deletions preserved, IDs never reused. All US5 tests PASS.

---

## Phase 8: User Story 6 - Marking Tasks Complete/Incomplete (Priority: P2)

**Goal**: User can toggle task completion status by ID

**Independent Test**: Run app, add task ID=1 (incomplete [ ]), toggle to complete [x], toggle back to incomplete [ ]

### Tests for User Story 6 (TDD: Write tests FIRST, ensure they FAIL)

- [ ] T-050 [P] [US6] Unit tests for TaskStorage.toggle_complete() in tests/test_storage.py (False→True, True→False, invalid ID raises error per data-model.md lines 279-304)
- [ ] T-051 [US6] Unit tests for toggle_complete_ui() in tests/test_cli.py (prompt ID, toggle status, display confirmation with new status per FR-018, FR-019)

### Implementation for User Story 6

- [ ] T-052 [US6] Implement TaskStorage.toggle_complete(task_id) in src/todo_app/storage.py (flip boolean, return updated task per data-model.md)
- [ ] T-053 [US6] Implement toggle_complete_ui() in src/todo_app/cli.py (prompt ID, call storage.toggle_complete(), display confirmation with new status per FR-018)
- [ ] T-054 [US6] Integrate toggle_complete_ui() into main loop in src/todo_app/main.py (route option 5 to toggle_complete_ui)

**Checkpoint**: Run app, toggle tasks between complete/incomplete, verify status changes bidirectionally. All US6 tests PASS. **ALL P2 FEATURES COMPLETE**

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, validation polish, integration testing, documentation

- [ ] T-055 [P] Add comprehensive input validation for menu choices in src/todo_app/cli.py (non-numeric input, out-of-range, empty input per FR-025, FR-026)
- [ ] T-056 [P] Add input validation for task IDs in src/todo_app/cli.py (non-integer input, negative numbers per FR-028)
- [ ] T-057 [P] Add edge case handling for max length inputs in src/todo_app/cli.py (title=200 chars, description=1000 chars per FR-029)
- [ ] T-058 Integration test for full CRUD workflow in tests/test_integration.py (add → list → update → toggle → delete in sequence)
- [ ] T-059 [P] Integration test for validation error recovery in tests/test_integration.py (retry after validation failures per FR-031)
- [ ] T-060 [P] Performance test for 100 tasks in tests/test_integration.py (add 100, list all <1s per SC-003)
- [ ] T-061 Run mypy type checking: `mypy src/todo_app` (must pass with no errors per Constitution III)
- [ ] T-062 Run pytest with coverage: `coverage run -m pytest tests/ && coverage report` (must achieve ≥80% per Constitution IV)
- [ ] T-063 [P] Manual testing using quickstart.md checklist (all 28 checklist items)
- [ ] T-064 Final code review for PEP 8 compliance and code quality (per Constitution III)

**Checkpoint**: All tests PASS, coverage ≥80%, mypy clean, manual checklist complete. **READY FOR PHASE 1 REVIEW**

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - User stories CAN proceed in parallel after Foundation (if team capacity allows)
  - OR sequentially in priority order: US1 (P1) → US2 (P1) → US3 (P1) → US4 (P2) → US5 (P2) → US6 (P2)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 - Navigation (P1)**: Foundation only → Can start after Phase 2
- **US2 - Add Tasks (P1)**: Foundation only → Can start after Phase 2 (parallel with US1/US3)
- **US3 - List Tasks (P1)**: Foundation only → Can start after Phase 2 (parallel with US1/US2)
- **US4 - Update Tasks (P2)**: Foundation + US2 (needs add_task for testing) → Can start after US2
- **US5 - Delete Tasks (P2)**: Foundation + US2 (needs add_task for testing) → Can start after US2
- **US6 - Toggle Complete (P2)**: Foundation + US2 (needs add_task for testing) → Can start after US2

### Within Each User Story (TDD Workflow)

1. **Write tests FIRST** (T-xxx test tasks)
2. **Run tests** → Verify they FAIL (RED phase)
3. **Implement feature** (T-xxx implementation tasks)
4. **Run tests** → Verify they PASS (GREEN phase)
5. **Refactor** if needed (improve code quality while keeping tests passing)
6. **Checkpoint** validation → Story works independently

### Parallel Opportunities

#### Phase 1 (Setup)
All tasks T-002, T-003, T-004 can run in parallel (different files)

#### Phase 2 (Foundation - Tests)
Tasks T-005, T-006 can run in parallel (different test files)

Tasks T-008, T-009 can run in parallel (both exceptions in models.py, different classes)

#### Phase 3 (US1 - Tests)
Tasks T-010, T-011, T-012 can run in parallel (different test functions)

Tasks T-014, T-015 can run in parallel (different CLI functions)

#### Phase 4 (US2 - Tests)
Tasks T-019, T-020, T-021, T-022 can run in parallel (different test files/functions)

#### Phase 5 (US3 - Tests)
Tasks T-028, T-029, T-030 can run in parallel (different test functions)

#### After Foundation Complete (Phase 2)
US1 (Phase 3), US2 (Phase 4), US3 (Phase 5) can ALL start in parallel if team capacity allows

#### Phase 9 (Polish)
Tasks T-055, T-056, T-057, T-059, T-060, T-063, T-064 can run in parallel (different concerns/files)

---

## Parallel Execution Examples

### Example 1: Foundation Tests (RED Phase)

```bash
# Launch all foundation test tasks in parallel:
Task T-005: "Unit tests for Task dataclass in tests/test_models.py"
Task T-006: "Unit tests for custom exceptions in tests/test_models.py"

# Run pytest to verify they FAIL (RED)
pytest tests/test_models.py  # Expected: FAIL (not implemented yet)
```

### Example 2: User Story 2 Tests (RED Phase)

```bash
# Launch all US2 test tasks in parallel:
Task T-019: "Unit tests for TaskStorage.__init__() in tests/test_storage.py"
Task T-020: "Unit tests for TaskStorage.add_task() in tests/test_storage.py"
Task T-021: "Unit tests for input validation in tests/test_storage.py"
Task T-022: "Unit tests for add_task_ui() in tests/test_cli.py"

# Run pytest to verify they FAIL (RED)
pytest tests/test_storage.py tests/test_cli.py  # Expected: FAIL
```

### Example 3: Parallel User Stories (After Foundation)

```bash
# If team has 3 developers, split work after Phase 2 completes:
Developer A: Phase 3 (US1 - Navigation)
Developer B: Phase 4 (US2 - Add Tasks)
Developer C: Phase 5 (US3 - List Tasks)

# Each developer follows TDD independently:
# 1. Write tests (RED)
# 2. Implement (GREEN)
# 3. Refactor
# 4. Checkpoint validation
```

---

## Implementation Strategy

### Recommended: Sequential by Priority (Solo Developer)

1. **Phase 1**: Setup (T-001 → T-004)
2. **Phase 2**: Foundation (T-005 → T-009) → CHECKPOINT: Tests PASS
3. **Phase 3**: US1 Navigation (T-010 → T-018) → CHECKPOINT: Menu works
4. **Phase 4**: US2 Add Tasks (T-019 → T-027) → CHECKPOINT: Can add tasks
5. **Phase 5**: US3 List Tasks (T-028 → T-035) → **MVP COMPLETE** → DEMO/VALIDATE
6. **Phase 6**: US4 Update (T-036 → T-043) → CHECKPOINT: Updates work
7. **Phase 7**: US5 Delete (T-044 → T-049) → CHECKPOINT: Deletion works
8. **Phase 8**: US6 Toggle (T-050 → T-054) → CHECKPOINT: Toggle works
9. **Phase 9**: Polish (T-055 → T-064) → **PHASE 1 COMPLETE** → RUN `/phase1-review`

### Alternative: Parallel Team Strategy (3 Developers)

1. **All**: Complete Phase 1 + Phase 2 together (Foundation MUST be complete)
2. **After Foundation**:
   - Developer A: US1 (T-010 → T-018)
   - Developer B: US2 (T-019 → T-027)
   - Developer C: US3 (T-028 → T-035)
3. **Integrate** → MVP COMPLETE
4. **P2 Features** (after US2 complete for dependencies):
   - Developer A: US4 (T-036 → T-043)
   - Developer B: US5 (T-044 → T-049)
   - Developer C: US6 (T-050 → T-054)
5. **All**: Polish together (T-055 → T-064)

---

## Task Summary

**Total Tasks**: 64 tasks
- **Phase 1 (Setup)**: 4 tasks
- **Phase 2 (Foundation)**: 5 tasks (2 tests + 3 implementation)
- **Phase 3 (US1 - Navigation, P1)**: 9 tasks (4 tests + 5 implementation)
- **Phase 4 (US2 - Add Tasks, P1)**: 9 tasks (4 tests + 5 implementation)
- **Phase 5 (US3 - List Tasks, P1)**: 8 tasks (3 tests + 5 implementation)
- **Phase 6 (US4 - Update, P2)**: 8 tasks (3 tests + 5 implementation)
- **Phase 7 (US5 - Delete, P2)**: 6 tasks (2 tests + 4 implementation)
- **Phase 8 (US6 - Toggle, P2)**: 5 tasks (2 tests + 3 implementation)
- **Phase 9 (Polish)**: 10 tasks (validation, integration tests, quality checks)

**TDD Coverage**: 20 test tasks + 44 implementation tasks = Following Red-Green-Refactor cycle
**Parallel Opportunities**: 25+ tasks marked [P] can run in parallel
**User Story Coverage**: All 6 user stories (3 P1, 3 P2) fully decomposed

---

## Constitution Compliance

✅ **C-001 (Spec-Driven Development)**: Tasks derived from spec.md user stories and plan.md architecture
✅ **C-002 (In-Memory Only)**: No persistence tasks, all storage via TaskStorage class
✅ **C-003 (No Network)**: No HTTP/API tasks
✅ **C-004 (Console Only)**: All UI via cli.py using input()/print()
✅ **C-005 (No Authentication)**: No auth tasks
✅ **C-006 (Python 3.13+)**: All tasks use Python standard library (datetime, dataclasses, typing)
✅ **C-007 (No File I/O)**: No file read/write tasks
✅ **Constitution III (Type Safety)**: T-061 validates full type hints with mypy
✅ **Constitution IV (TDD)**: 20 test tasks, Red-Green-Refactor workflow, T-062 validates ≥80% coverage

---

## Notes

- **[P] tasks**: Different files, no dependencies, can execute in parallel
- **[Story] label**: Maps task to user story for traceability (US1-US6)
- **TDD Workflow**: Write tests → Run (FAIL/RED) → Implement → Run (PASS/GREEN) → Refactor
- **Checkpoints**: Validate after each user story phase before proceeding
- **MVP Definition**: Phases 1-5 complete (Setup + Foundation + US1/US2/US3 P1 features)
- **Commit Strategy**: Commit after each task or logical group (e.g., all tests for a story)
- **Testing Order**: Unit tests before integration tests; story tests before story implementation
- **Task IDs**: T-001 through T-064, sequential, never reused (mirroring Task ID design)

---

**Ready for**: `/sp.implement` (execute tasks with TDD workflow) or `/sp.analyze` (cross-artifact consistency check)

**Next Command**: `/sp.implement` to begin TDD implementation following task sequence
