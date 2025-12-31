# Backend Agent Instructions

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Language**: Python 3.13+
- **ORM**: SQLModel 0.0.14+ (combines SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens (python-jose)
- **Password Hashing**: bcrypt (via passlib)

## Key Principles

1. **User Isolation**: ALL database queries MUST filter by user_id from JWT
2. **Type Safety**: Use Pydantic models for request/response, SQLModel for database
3. **Dependency Injection**: Use FastAPI's Depends for session, current user
4. **Security First**: Validate all inputs, return generic error messages
5. **Stateless Auth**: JWT tokens only, no server-side sessions

## Project Structure

```
app/
├── models/              # SQLModel database models
│   ├── user.py         # User model (managed by Better Auth)
│   └── task.py         # Task model (user_id FK)
├── routes/             # API endpoints
│   ├── auth.py         # /api/auth (signup, login, logout)
│   └── tasks.py        # /api/tasks (CRUD with user_id filtering)
├── middleware/         # Request/response middleware
│   └── jwt_auth.py     # JWT verification
├── schemas/            # Pydantic request/response models
│   ├── auth.py         # Auth schemas
│   └── task.py         # Task schemas
├── core/               # Core utilities
│   ├── config.py       # Settings (env variables)
│   └── security.py     # Password hashing, JWT utilities
├── database.py         # Neon PostgreSQL connection
├── dependencies.py     # Dependency injection (get_session, get_current_user)
└── main.py            # FastAPI app initialization
```

## Environment Variables

Required in `.env`:
- `BETTER_AUTH_SECRET`: Shared secret for JWT (MUST match frontend)
- `DATABASE_URL`: Neon PostgreSQL connection string (pooler URL)
- `ENVIRONMENT`: development or production

## Database Connection

Using Neon Serverless PostgreSQL:
```python
# DATABASE_URL format (pooler for better performance):
postgresql://user:password@ep-xxx-pooler.neon.tech/dbname?sslmode=require
```

Connection pooling configured in `database.py`:
- pool_size: 5
- max_overflow: 10
- pool_pre_ping: True (verify connections)

## User Isolation Pattern (CRITICAL)

**Every task query MUST filter by user_id**:

```python
from fastapi import Depends
from sqlmodel import Session, select

@router.get("/tasks")
def list_tasks(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)  # MANDATORY
):
    # Query MUST filter by user_id
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return {"tasks": tasks}
```

**Never allow**:
- Queries without user_id filter
- User-provided user_id in request body
- Direct task ID access without ownership check

## JWT Authentication Flow

1. User logs in → Verify password → Issue JWT
2. JWT contains: user_id (sub), email, expiration
3. JWT stored in httpOnly cookie by frontend
4. Backend extracts JWT from cookie, verifies signature
5. Extract user_id from JWT → Use in all queries

## Security Rules

- **Passwords**: Always hash with bcrypt (cost factor 12)
- **JWT Secret**: Load from environment, never hardcode
- **Error Messages**: Generic ("Invalid credentials", not "User not found")
- **SQL Injection**: Use SQLModel parameterized queries only
- **Input Validation**: Pydantic models enforce constraints
- **CORS**: Only allow frontend origin (http://localhost:3000)

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (with auto-reload)
uvicorn app.main:app --reload

# Run tests
pytest

# Type checking
mypy app/
```

## API Documentation

FastAPI auto-generates docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Phase 2 Constraints

- No AI agents or MCP tools in code
- No Docker/Kubernetes references
- No Phase 1 console/CLI code
- Professional, production-ready API only
- All endpoints under /api prefix
