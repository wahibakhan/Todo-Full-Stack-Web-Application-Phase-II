# Skills Directory Structure

## Overview

This directory contains custom Claude Code skills organized by hackathon phase.

## Directory Tree

```
skills/
├── README.md              # Main skills documentation
├── STRUCTURE.md           # This file - directory structure
│
├── phase1/                # Phase 1: Console Todo App
│   ├── README.md          # Phase 1 skills guide
│   ├── phase1-init.md     # Project initialization skill
│   ├── phase1-spec.md     # Specification generator skill
│   └── phase1-review.md   # Compliance reviewer skill
│
├── phase2/                # Phase 2: Database Integration (future)
│   └── README.md
│
└── phase3/                # Phase 3: Web Interface (future)
    └── README.md
```

## Skill Locations

Skills must be in `.claude/commands/` to be executable as slash commands:

```
.claude/commands/
├── phase1-init.md      ← Executable skill
├── phase1-spec.md      ← Executable skill
├── phase1-review.md    ← Executable skill
├── sp.specify.md       ← Existing SDD skills
├── sp.plan.md
├── sp.tasks.md
├── sp.implement.md
└── ...
```

The `skills/` folder serves as:
- **Documentation** - Organized reference for all skills
- **Backup** - Copy of skills with detailed README files
- **Version control** - Track skill evolution by phase

## Phase Organization

### Phase 1: Console Todo App
**Status**: ✅ Complete (3 skills)
- Initialization, Specification, Review
- Enforces: no DB, no web, in-memory only

### Phase 2: Database Integration
**Status**: 🔜 Coming soon
- Planned skills: database setup, migration, persistence

### Phase 3: Web Interface
**Status**: 🔜 Coming soon
- Planned skills: web framework setup, API endpoints, UI

## Usage Pattern

1. **Skills are executed from `.claude/commands/`**:
   ```
   /phase1-init
   /phase1-spec
   /phase1-review
   ```

2. **Documentation is in `skills/`**:
   - Read `skills/README.md` for overview
   - Read `skills/phase1/README.md` for Phase 1 details
   - Reference individual skill `.md` files for specifics

## Maintenance

When creating new skills:

1. Create in `.claude/commands/` (for execution)
2. Copy to `skills/phaseX/` (for documentation)
3. Update `skills/phaseX/README.md`
4. Update `skills/README.md` with new phase/skill

## Benefits

- **Organized**: Skills grouped by phase and purpose
- **Documented**: Each phase has comprehensive README
- **Discoverable**: Clear structure for finding skills
- **Maintainable**: Easy to add new phases and skills
- **Educational**: README files explain workflow and best practices
