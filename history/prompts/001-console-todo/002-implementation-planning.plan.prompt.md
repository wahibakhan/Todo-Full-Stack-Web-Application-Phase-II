---
id: 002
title: Phase 1 Implementation Planning
stage: plan
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5
feature: 001-console-todo
branch: 001-console-todo
user: HP
command: /sp.plan
labels: ["planning", "architecture", "phase1", "console-todo", "sdd"]
links:
  spec: specs/001-console-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-console-todo/plan.md
 - specs/001-console-todo/research.md
 - specs/001-console-todo/data-model.md
 - specs/001-console-todo/quickstart.md
 - specs/001-console-todo/contracts/README.md
tests:
 - N/A (planning phase)
---

## Prompt

/sp.plan # speckit.plan
## Implementation Plan for Phase 1: In-Memory Python Console Todo App

### Architectural Overview
The application will follow a clean, modular, layered architecture suitable for a console-based tool:

- **Models Layer**: Defines the data structure for a Task
- **Storage Layer**: Manages in-memory collection and CRUD operations
- **CLI Layer**: Handles user interaction, input processing, and display formatting
- **Main Entry Point**: Orchestrates the application loop

All layers will be explicitly separated into different modules under /src/ to ensure maintainability and testability.

### Component Breakdown

1. **Task Model** (`src/models.py`)
   - Dataclass representing a single task
   - Fields: id (int), title (str), description (str, optional), completed (bool), created_at (datetime)
   - Immutable where possible; clear string representation

2. **In-Memory Storage** (`src/storage.py`)
   - Class or simple module managing a list/collection of Task objects
   - Methods:
     - add_task(title, description) → returns new Task
     - get_all_tasks() → returns list[Task]
     - get_task_by_id(id) → Task or None
     - update_task(id, title=None, description=None)
     - delete_task(id)
     - toggle_complete(id)
   - Auto-incrementing ID generation
   - Input validation and exception handling (e.g., TaskNotFound)

3. **CLI Interface** (`src/cli.py`)
   - Functions for:
     - Displaying welcome banner and main menu
     - Rendering task list in readable format with status indicators
     - Prompting user for input (add, update, etc.)
     - Showing success/error messages
   - Uses simple print/input or optional minimal third-party library (e.g., rich) only if justified

4. **Application Loop** (`src/main.py`)
   - Entry point (`if __name__ == "__main__"`)
   - Instantiates storage
   - Runs infinite loop displaying menu and routing commands
   - Clean exit handling (Ctrl+C or "exit" command)

### Data Flow
1. User interacts via CLI → cli.py collects input
2. CLI calls appropriate storage method
3. Storage updates in-memory state
4. CLI refreshes display with updated task list

### Implementation Sequence
The following order ensures incremental development and early feedback:

1. Define Task model and basic storage skeleton
2. Implement add_task and list_tasks (core loop visible early)
3. Implement update_task
4. Implement toggle_complete
5. Implement delete_task (with confirmation)
6. Polish CLI formatting and error messages
7. Final integration and main loop refinement

### Dependencies & Constraints Compliance
- Python standard library only (datetime, typing, dataclasses)
- No external packages required
- No persistence to disk
- No network or external service calls
- Full adherence to Phase 1 constitution

### Risk Mitigation
- Early validation of input edge cases (empty title, invalid ID)
- Clear separation prevents tight coupling
- Incremental implementation allows early detection of usability issues

This speckit.plan document defines HOW the requirements in speckit.specify will be technically realized while remaining strictly within Phase 1 boundaries.

## Response snapshot

Successfully completed comprehensive Phase 1 implementation planning for Console Todo Application.

**Phase 0 - Research**:
- Created `research.md` with technology decisions (Python 3.13+, standard library only, dict storage, pytest, mypy)
- Documented architectural patterns (layered architecture, auto-incrementing IDs, custom exceptions)
- Identified implementation sequence aligned with user story priorities (P1/P2)
- Zero unknowns or clarifications needed - all decisions straightforward

**Phase 1 - Design**:
- Created `data-model.md` with complete Task entity specification
  - Task dataclass with 5 fields (id, title, description, completed, created_at)
  - TaskStorage class with 6 methods (add/get_all/get_by_id/update/delete/toggle)
  - Custom exceptions (TaskNotFoundError, ValidationError)
  - Validation matrix with rules and error messages
- Created `contracts/README.md` - Explains why API contracts not applicable for console app
- Created `quickstart.md` - Setup, running, development, and troubleshooting guide

**Final Plan Document** (`plan.md`):
- **Summary**: Phase 1 constraints, technical approach, layered architecture
- **Technical Context**: Python 3.13+, standard library only, in-memory dict storage, pytest testing
- **Constitution Check**: All 7 Phase 1 constraints PASSED, zero violations
- **Project Structure**: Documentation tree, source code tree, structure decision
- **Architectural Overview**: 4-layer architecture with layer diagram and component breakdown
- **Data Flow**: Operation flow pattern, example add task flow
- **Implementation Sequence**: 11 tasks organized into 3 phases (Foundation, CRUD Completion, Validation & Polish)
- **Testing Strategy**: TDD workflow (Red-Green-Refactor), test organization, coverage requirements (≥80%)
- **Dependencies**: Standard library only (runtime), pytest/mypy (development)
- **Risk Mitigation**: 4 identified risks with mitigations, non-risks documented
- **Performance Considerations**: Targets, complexity analysis, memory usage estimates
- **ADR Suggestions**: 3 architectural decisions identified for optional documentation
- **Next Steps**: Awaiting human approval → Run `/sp.tasks` → Follow TDD workflow → `/phase1-review` → `/sp.git.commit_pr`

**Constitution Compliance**:
- ✅ Phase 1 Constraints (C-001 through C-007): All passed
- ✅ Code Quality Standards: Full type hints, dataclass, module separation planned
- ✅ TDD Standards: Red-Green-Refactor workflow, 80% coverage target set
- ✅ Traceability: Task ID comments, acceptance criteria mapping planned

**Agent Context Updated**:
- CLAUDE.md updated with project context (though template placeholders used since plan was being written)

## Outcome

- ✅ Impact: Created complete technical blueprint for Phase 1 implementation with layered architecture, TDD workflow, and comprehensive testing strategy - ready for task breakdown
- 🧪 Tests: Planning phase - TDD workflow documented, test structure planned, coverage target (80%) set, testing strategy defined
- 📁 Files: Created 5 planning artifacts (plan.md, research.md, data-model.md, quickstart.md, contracts/README.md)
- 🔁 Next prompts: /sp.tasks (generate atomic task breakdown), /sp.implement (execute tasks with TDD), /phase1-review (compliance check)
- 🧠 Reflection: Plan strictly adheres to Phase 1 Constitution with zero violations. Layered architecture (models/storage/cli/main) ensures clear separation of concerns. Implementation sequence aligned with user story priorities (P1 foundation first, P2 polish second). TDD workflow planned with Red-Green-Refactor cycle. All 33 functional requirements mapped to 11 tasks. Dict-based storage provides O(1) lookups while remaining simple. Custom exceptions enable Pythonic error handling. Plan provides complete blueprint while leaving implementation details to coding phase.

## Evaluation notes (flywheel)

- Failure modes observed: None - all Phase 1 constraints satisfied, zero violations, complete planning artifacts generated
- Graders run and results (PASS/FAIL): Constitution Check PASS (all 7 constraints verified), Code Quality PASS (type hints/dataclass/separation planned), TDD PASS (workflow documented)
- Prompt variant (if applicable): User provided detailed architectural guidance in prompt, which was incorporated into formal plan structure with additional Phase 0 research and Phase 1 design artifacts
- Next experiment (smallest change to try): Run `/sp.tasks` to convert 11-task implementation sequence into detailed atomic task breakdown with acceptance criteria, test specifications, and file change tracking. Tasks should reference both plan.md and spec.md for traceability.
