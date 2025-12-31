# Data Model: Phase 2 Full-Stack Web Application

**Feature**: Full-Stack Web Todo Application with Authentication
**Date**: 2025-12-29
**Phase**: Phase 1 - Design & Contracts
**Database**: Neon Serverless PostgreSQL

## Overview

This document defines the database schema, entity relationships, validation rules, and state transitions for Phase 2. The data model supports multi-user authentication with strict user isolation enforced at the database level.

## Entity Relationship Diagram

```
┌─────────────┐           ┌─────────────┐
│    User     │           │    Task     │
├─────────────┤           ├─────────────┤
│ id (PK)     │──────────<│ user_id (FK)│
│ email       │    1:N    │ id (PK)     │
│ password    │           │ title       │
│ created_at  │           │ description │
└─────────────┘           │ completed   │
                          │ created_at  │
                          │ updated_at  │
                          └─────────────┘

Relationship: One user has many tasks (1:N)
Constraint: user_id in Task is NOT NULL (every task must belong to a user)
Cascade: ON DELETE CASCADE (deleting user deletes all their tasks)
```

## Entities

### 1. User

**Purpose**: Represents a registered user account for authentication and task ownership.

**Managed By**: Better Auth library (handles table creation, password hashing, authentication flows)

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Better Auth may add additional fields (e.g., email_verified, last_login)
```

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `email` | String (255) | UNIQUE, NOT NULL, INDEX | User's email address (used for login) |
| `hashed_password` | String (255) | NOT NULL | Bcrypt hashed password (never store plaintext) |
| `created_at` | Timestamp | NOT NULL, DEFAULT NOW() | Account creation timestamp |

**Validation Rules**:

- **email**:
  - Must be valid email format (contains @ and domain)
  - Must be unique (Better Auth enforces this)
  - Maximum 255 characters
  - Case-insensitive comparison for uniqueness

- **password** (before hashing):
  - Minimum 8 characters
  - Better Auth handles hashing automatically (bcrypt with salt)

**Indexes**:

- Primary key index on `id`
- Unique index on `email` (for fast login lookups)

**State Transitions**:

```
[Not Registered]
     ↓ (signup with email + password)
[Registered]
     ↓ (login with correct credentials)
[Authenticated Session]
     ↓ (logout)
[Registered]
```

**Notes**:

- Better Auth manages this table automatically
- Additional fields may be added by Better Auth (e.g., `email_verified`, `last_login_at`)
- Password reset and email verification are out of scope for Phase 2

---

### 2. Task

**Purpose**: Represents a todo item owned by a specific user.

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional for queries)
    # user: Optional[User] = Relationship(back_populates="tasks")
```

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| `user_id` | Integer | FOREIGN KEY (users.id), NOT NULL, INDEX | Owner of the task (CRITICAL for user isolation) |
| `title` | String (200) | NOT NULL | Task title (required) |
| `description` | String (1000) | NULLABLE | Task description (optional, can be empty) |
| `completed` | Boolean | NOT NULL, DEFAULT FALSE | Completion status (false = incomplete, true = complete) |
| `created_at` | Timestamp | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| `updated_at` | Timestamp | NOT NULL, DEFAULT NOW(), ON UPDATE NOW() | Last modification timestamp |

**Validation Rules**:

- **title**:
  - Required (cannot be null or empty string)
  - Minimum 1 character
  - Maximum 200 characters
  - Trimmed of leading/trailing whitespace

- **description**:
  - Optional (can be null or empty string)
  - Maximum 1000 characters if provided
  - Trimmed of leading/trailing whitespace

- **user_id**:
  - Must exist in users table (foreign key constraint)
  - Cannot be null
  - Set automatically from JWT during creation (not user-editable)

- **completed**:
  - Boolean only (true or false)
  - Defaults to false on creation

**Indexes**:

- Primary key index on `id`
- Index on `user_id` (critical for performance - filters all queries by user)
- Composite index on `(user_id, created_at)` (optional, for sorted task lists)

**Foreign Key Constraints**:

```sql
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

- **ON DELETE CASCADE**: Deleting a user automatically deletes all their tasks
- **Rationale**: Prevents orphaned tasks, maintains data integrity

**State Transitions**:

```
[Not Created]
     ↓ (user creates task with title)
[Created - Incomplete]
     ↓ (user toggles completion)
[Created - Complete]
     ↓ (user toggles completion again)
[Created - Incomplete]
     ↓ (user deletes task)
[Deleted]
```

**Query Patterns**:

All queries MUST filter by user_id to enforce user isolation:

```python
# List tasks for current user
statement = select(Task).where(Task.user_id == current_user_id)
tasks = session.exec(statement).all()

# Get specific task (verify ownership)
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == current_user_id
)
task = session.exec(statement).first()
if not task:
    raise HTTPException(status_code=404, detail="Task not found")

# Update task (verify ownership)
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == current_user_id
)
task = session.exec(statement).first()
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
task.title = new_title
task.updated_at = datetime.utcnow()
session.add(task)
session.commit()

# Delete task (verify ownership)
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == current_user_id
)
task = session.exec(statement).first()
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
session.delete(task)
session.commit()
```

---

## Database Schema (SQL DDL)

**For Reference - SQLModel generates this automatically via `create_all()`**:

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_id_created_at ON tasks(user_id, created_at);
```

## Data Integrity Rules

### User Isolation (CRITICAL)

1. **All queries MUST include `user_id` filter**:
   - Enforced via dependency injection (`user_id = Depends(get_current_user)`)
   - Prevents cross-user data access

2. **Foreign key constraint**:
   - `tasks.user_id` references `users.id`
   - Cannot create task without valid user_id
   - Deleting user cascades to delete all their tasks

3. **403/404 for unauthorized access**:
   - If User A requests User B's task by ID, return 404 (not 403)
   - Rationale: 403 reveals existence of task, 404 is safer

### Data Validation

1. **Backend validation** (Pydantic schemas):
   - Title length: 1-200 characters
   - Description length: 0-1000 characters
   - Email format validation
   - Password minimum 8 characters

2. **Database constraints**:
   - NOT NULL on required fields
   - UNIQUE on email
   - FOREIGN KEY on user_id
   - VARCHAR length limits

3. **Frontend validation** (pre-submit):
   - Same rules as backend (client-side for UX)
   - Backend is ultimate authority (don't trust frontend)

### Timestamp Management

1. **created_at**:
   - Set automatically on INSERT
   - Never modified

2. **updated_at**:
   - Set automatically on INSERT
   - Updated automatically on UPDATE
   - SQLModel handles this via `default_factory` and manual update

## Migration Strategy

**Phase 2 MVP Approach**: No migrations (use `SQLModel.metadata.create_all()`)

```python
# app/main.py (on startup)
from app.database import engine
from sqlmodel import SQLModel

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
```

**Rationale**:
- Simple for MVP (no migration history needed)
- Tables created automatically on first run
- Sufficient for Phase 2 requirements

**Future (Post-MVP)**:
- Use Alembic for migrations if schema changes frequently
- Not required for Phase 2 submission

## Example Data

**Users**:

| id | email | hashed_password | created_at |
|----|-------|----------------|------------|
| 1 | alice@example.com | $2b$12$abc... | 2025-12-29 10:00:00 |
| 2 | bob@example.com | $2b$12$xyz... | 2025-12-29 11:00:00 |

**Tasks**:

| id | user_id | title | description | completed | created_at | updated_at |
|----|---------|-------|-------------|-----------|------------|------------|
| 1 | 1 | Buy groceries | Milk, eggs, bread | false | 2025-12-29 10:05:00 | 2025-12-29 10:05:00 |
| 2 | 1 | Fix bug in app | See issue #42 | true | 2025-12-29 10:10:00 | 2025-12-29 12:00:00 |
| 3 | 2 | Schedule meeting | Team sync on Friday | false | 2025-12-29 11:15:00 | 2025-12-29 11:15:00 |

**User Isolation Verification**:
- User 1 (alice) can only see task IDs 1 and 2
- User 2 (bob) can only see task ID 3
- User 1 attempting to access task ID 3 returns 404 Not Found

---

**Data Model**: ✅ **COMPLETE**
**Next Artifact**: API Contracts (contracts/auth-endpoints.md, contracts/task-endpoints.md)
