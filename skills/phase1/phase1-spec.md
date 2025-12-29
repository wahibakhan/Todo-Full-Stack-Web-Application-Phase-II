---
description: Generate complete Phase 1 specification for console Todo app following Panaversity Hackathon standards.
handoffs:
  - label: Create Technical Plan
    agent: sp.plan
    prompt: Create technical plan for Phase 1 console Todo app
    send: true
  - label: Generate Task Breakdown
    agent: sp.tasks
    prompt: Generate task breakdown from the plan
---

## User Input

```text
$ARGUMENTS
```

## Overview

Generate a complete, hackathon-compliant specification for Phase 1: Console Todo App. The spec must be technology-focused on **WHAT** the app does, not **HOW** it's implemented, while strictly adhering to Phase 1 constraints.

## Phase 1 Constraints (CRITICAL)

These constraints MUST be explicitly documented in the spec:

1. **No Database** - In-memory storage only (Python list/dict)
2. **No Web Interface** - Console/terminal interface only
3. **No File Persistence** - Data lost when app closes
4. **Python Console App** - Pure Python, no GUI frameworks
5. **CRUD Operations** - Create, Read, Update, Delete todos
6. **Spec-Driven Development** - No code until specs/plan/tasks approved

## Specification Generation Steps

1. **Create Feature Directory**: `specs/phase1-console-todo/`

2. **Generate `spec.md`** with these sections:

   ### Required Sections:

   **Feature Overview**
   - Brief description of console Todo app
   - Phase 1 scope and constraints
   - User value proposition

   **User Stories** (minimum 5):
   - As a user, I want to add a new todo...
   - As a user, I want to view all todos...
   - As a user, I want to mark a todo as complete...
   - As a user, I want to delete a todo...
   - As a user, I want to update a todo description...

   **Functional Requirements**:
   - FR1: Add todo with description and optional due date
   - FR2: List all todos with their status
   - FR3: Mark todo as complete/incomplete
   - FR4: Delete todo by ID
   - FR5: Update todo description
   - FR6: View todo details
   - FR7: Exit application gracefully

   **Success Criteria** (Technology-Agnostic):
   - User can manage todos entirely from command line
   - All CRUD operations complete in under 1 second
   - Zero data persistence (validates in-memory constraint)
   - Clear, user-friendly console messages
   - Invalid input handled with helpful error messages

   **User Scenarios & Acceptance Criteria**:
   - Scenario 1: Adding first todo
   - Scenario 2: Viewing todo list
   - Scenario 3: Completing a todo
   - Scenario 4: Deleting a todo
   - Scenario 5: Updating a todo

   **Constraints & Assumptions**:
   - Python 3.8+ required
   - In-memory storage only (no DB, no files)
   - Console interface only (no web, no GUI)
   - Data not persisted between runs
   - Single-user application (no concurrency)

   **Out of Scope**:
   - Database integration
   - Web interface
   - File persistence
   - Multi-user support
   - Authentication
   - Cloud deployment

   **Dependencies**:
   - Python 3.8+ standard library only
   - Optional: pytest for testing

   **Key Entities**:
   - Todo: {id, description, completed, created_at, due_date (optional)}

3. **Create Spec Quality Checklist**: `specs/phase1-console-todo/checklists/requirements.md`
   - Validate no implementation details (no mention of classes, functions, libraries)
   - Validate technology-agnostic success criteria
   - Validate Phase 1 constraints are documented
   - Validate all CRUD operations have acceptance criteria

4. **Validation**:
   - ✅ No mention of Python classes, functions, or modules
   - ✅ No mention of data structures (list, dict, etc.)
   - ✅ Success criteria measurable from user perspective
   - ✅ Phase 1 constraints explicitly stated
   - ✅ Out of scope clearly defines what's NOT in Phase 1

5. **Handle Clarifications**:
   - If user provides additional requirements in $ARGUMENTS, incorporate them
   - Use [NEEDS CLARIFICATION] only for critical scope decisions (max 3)
   - Make reasonable assumptions for minor details

## Output

Generate the complete spec and report:
- ✅ Spec file created at `specs/phase1-console-todo/spec.md`
- ✅ Checklist created at `specs/phase1-console-todo/checklists/requirements.md`
- ✅ All Phase 1 constraints documented
- ✅ All CRUD operations specified
- ✅ Technology-agnostic success criteria defined
- 📋 Next step: Run `/sp.plan` to create technical architecture

## Important Notes

- **Focus on WHAT, not HOW**: Spec describes behavior, not implementation
- **Phase 1 constraints are non-negotiable**: Must be explicit in spec
- **Keep it simple**: Don't over-engineer for Phase 1
- **Think like a product manager**: Write for non-technical stakeholders
- **Avoid technical jargon**: No classes, functions, APIs, databases in spec
