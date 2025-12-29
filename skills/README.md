# Skills Directory

This directory contains custom Claude Code skills for the Panaversity Hackathon II project.

## Organization

Skills are organized by phase and purpose:

```
skills/
├── phase1/          # Phase 1: Console Todo App skills
│   ├── phase1-init.md
│   ├── phase1-spec.md
│   └── phase1-review.md
├── phase2/          # Phase 2: Database integration (future)
└── phase3/          # Phase 3: Web interface (future)
```

## Phase 1 Skills

### `/phase1-init` - Project Initialization
Initializes the complete Phase 1 project structure with proper directories, Python packages, and baseline documentation.

**Usage**: `/phase1-init`

**Creates**:
- Directory structure (src, tests, specs, history)
- Python package structure with `__init__.py`
- Constitution with Phase 1 constraints
- README and .gitignore

---

### `/phase1-spec` - Specification Generator
Generates hackathon-compliant specification for the console Todo app.

**Usage**: `/phase1-spec [additional requirements]`

**Creates**:
- `specs/phase1-console-todo/spec.md` - Complete feature specification
- `specs/phase1-console-todo/checklists/requirements.md` - Quality checklist

**Key Features**:
- Enforces technology-agnostic language (WHAT, not HOW)
- Documents Phase 1 constraints explicitly
- Defines all CRUD operations with acceptance criteria
- Validates against spec quality checklist

---

### `/phase1-review` - Compliance Reviewer
Comprehensive review of Phase 1 implementation for hackathon compliance and quality.

**Usage**: `/phase1-review`

**Reviews**:
- ✅ Phase 1 constraint compliance (no DB, no web, in-memory only)
- ✅ CRUD operations implementation
- ✅ Code quality (PEP 8, tests, documentation)
- ✅ User experience (error handling, console interface)

**Creates**:
- `specs/phase1-console-todo/review-report.md` - Detailed review report

**Auto-fail Detection**:
- Database imports (sqlite3, sqlalchemy, etc.)
- Web frameworks (flask, django, etc.)
- File I/O operations (open, write, pickle, etc.)

---

## Workflow

The recommended workflow for Phase 1:

```
1. /phase1-init        → Initialize project structure
2. /phase1-spec        → Generate specification
3. /sp.plan            → Create technical plan
4. /sp.tasks           → Generate task breakdown
5. /sp.implement       → Execute tasks
6. /phase1-review      → Review for compliance
7. /sp.git.commit_pr   → Commit and create PR
```

## Installation

Skills in `.claude/commands/` are automatically available as slash commands. To use these skills:

1. Keep them in `.claude/commands/` (already done)
2. Invoke with `/skill-name` in Claude Code
3. Or copy to this folder for documentation/backup

## Notes

- All Phase 1 skills enforce Spec-Driven Development workflow
- Skills include handoff buttons for guided workflow
- Phase 1 constraints are hardcoded and non-negotiable
- Review skill provides submission readiness verdict
