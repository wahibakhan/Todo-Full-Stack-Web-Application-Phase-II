# Research & Technology Decisions: Phase 2 Full-Stack Web Application

**Feature**: Full-Stack Web Todo Application with Authentication
**Date**: 2025-12-29
**Phase**: Phase 0 - Research & Technology Decisions

## Overview

This document consolidates research findings for implementing Phase 2 requirements using the constitutionally mandated technology stack. Since technologies are prescribed (Next.js 16+, FastAPI, Better Auth, SQLModel, Neon PostgreSQL), research focuses on **implementation patterns and best practices** rather than technology selection.

## Research Tasks & Findings

### 1. Better Auth Integration with Next.js 16+ App Router

**Question**: How to configure Better Auth for JWT tokens with Next.js 16+ App Router?

**Research Conducted**:
- Better Auth documentation (version 1.x)
- Next.js App Router authentication patterns
- httpOnly cookie configuration

**Decision**: Use Better Auth with JWT plugin configured in `lib/auth.ts`

**Implementation Pattern**:

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: {
    // Better Auth can manage user table in Neon PostgreSQL
    provider: "postgresql",
    url: process.env.DATABASE_URL
  },
  secret: process.env.BETTER_AUTH_SECRET,
  plugins: [
    {
      id: "jwt",
      name: "JWT Plugin",
      options: {
        expiresIn: "24h",
        algorithm: "HS256"
      }
    }
  ],
  session: {
    cookieOptions: {
      httpOnly: true, // XSS protection
      secure: process.env.NODE_ENV === "production", // HTTPS only in production
      sameSite: "lax" // CSRF protection
    }
  }
})
```

**Rationale**:
- Better Auth handles user management, password hashing, and JWT issuance
- httpOnly cookies prevent XSS attacks on tokens
- sameSite: "lax" prevents CSRF while allowing navigation
- 24-hour expiry balances security and user experience

**Alternatives Considered**:
- Custom JWT implementation: Rejected (requires more code, error-prone)
- NextAuth.js: Rejected (not prescribed by constitution, heavier library)

---

### 2. JWT Token Sharing Between Next.js Frontend and FastAPI Backend

**Question**: How to securely share and verify JWT tokens between Next.js (frontend) and FastAPI (backend)?

**Research Conducted**:
- JWT spec (RFC 7519)
- FastAPI JWT verification patterns
- python-jose library documentation

**Decision**: Use shared BETTER_AUTH_SECRET for JWT signing and verification

**Implementation Pattern**:

**Backend (FastAPI - middleware/jwt_auth.py)**:

```python
from fastapi import Request, HTTPException
from jose import jwt, JWTError
import os

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def verify_jwt(request: Request):
    token = request.cookies.get("auth-token") # Better Auth cookie name

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub") # JWT subject claim contains user_id
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Frontend (Next.js - lib/api.ts)**:

```typescript
// API client automatically includes cookies in fetch requests
export async function apiClient(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    credentials: "include", // Send cookies with request
    headers: {
      "Content-Type": "application/json",
      ...options.headers
    }
  })

  if (response.status === 401) {
    // Token invalid/expired - redirect to login
    window.location.href = "/login"
    throw new Error("Unauthorized")
  }

  return response
}
```

**Rationale**:
- Shared secret ensures both frontend and backend can work with same tokens
- Backend verifies token on every request (stateless authentication)
- Frontend includes cookies automatically via credentials: "include"
- 401 responses trigger logout/redirect to login

**Alternatives Considered**:
- Bearer token in Authorization header: Rejected (requires manual token extraction from cookies, more complex)
- Separate frontend and backend secrets: Rejected (tokens wouldn't be compatible)

---

### 3. SQLModel with Neon Serverless PostgreSQL

**Question**: How to connect SQLModel to Neon Serverless PostgreSQL efficiently?

**Research Conducted**:
- Neon PostgreSQL documentation (serverless driver, connection pooling)
- SQLModel documentation (engine creation, sessions)
- FastAPI async patterns

**Decision**: Use Neon's connection pooler with SQLModel sync engine

**Implementation Pattern**:

```python
# database.py
from sqlmodel import create_engine, Session, SQLModel
import os

# Neon connection URL (with pooler)
DATABASE_URL = os.getenv("DATABASE_URL")
# Example: postgresql://user:pass@ep-xxx-pooler.neon.tech/dbname

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True, # Log SQL queries in development
    pool_size=5,
    max_overflow=10
)

# Create tables (run once on startup)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency for getting database session
def get_session():
    with Session(engine) as session:
        yield session
```

**Usage in FastAPI**:

```python
from fastapi import Depends
from sqlmodel import Session

@app.get("/api/tasks")
def get_tasks(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return {"tasks": tasks}
```

**Rationale**:
- Neon's pooler URL handles connection pooling automatically
- Dependency injection ensures proper session lifecycle
- SQLModel's create_all() creates tables automatically (no migration tool needed for Phase 2 MVP)

**Alternatives Considered**:
- Async SQLModel with asyncpg: Rejected (adds complexity, sync is sufficient for Phase 2 scale)
- Alembic migrations: Deferred to post-MVP (SQLModel.metadata.create_all() sufficient for now)

---

### 4. User Isolation Patterns

**Question**: Best practices for enforcing user_id filtering in all database queries?

**Research Conducted**:
- FastAPI dependency injection patterns
- SQLModel query filtering
- Security best practices for multi-tenant applications

**Decision**: Use dependency injection to get current user and enforce filtering in every query

**Implementation Pattern**:

```python
# dependencies.py
from fastapi import Depends, HTTPException
from sqlmodel import Session
from .middleware.jwt_auth import verify_jwt
from .database import get_session

async def get_current_user(
    user_id: int = Depends(verify_jwt)
) -> int:
    return user_id

# routes/tasks.py
from sqlmodel import select

@router.get("/tasks")
def list_tasks(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user) # MANDATORY - automatically filters
):
    # Query MUST filter by user_id
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return {"tasks": tasks}

@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    update_data: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    # Verify ownership before updating
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id # CRITICAL: prevents cross-user access
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task
    task.title = update_data.title or task.title
    task.description = update_data.description
    session.add(task)
    session.commit()
    session.refresh(task)

    return {"task": task}
```

**Rationale**:
- Every route automatically receives user_id from JWT via dependency injection
- Impossible to forget user_id filter (dependency is required)
- 404 Not Found returned for cross-user access attempts (doesn't reveal existence)

**Alternatives Considered**:
- Global query filter: Rejected (SQLModel doesn't support this out of the box)
- Manual filtering in each query: Rejected (error-prone, easy to forget)

---

### 5. Next.js Middleware for Route Protection

**Question**: How to protect routes with JWT verification in Next.js App Router middleware?

**Research Conducted**:
- Next.js middleware documentation
- App Router authentication patterns
- Cookie extraction patterns

**Decision**: Use middleware.ts to protect routes based on JWT presence

**Implementation Pattern**:

```typescript
// middleware.ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token")
  const { pathname } = request.nextUrl

  // Protected routes require authentication
  const protectedRoutes = ["/dashboard"]
  const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route))

  // Public routes (login, signup) should redirect if already authenticated
  const publicRoutes = ["/login", "/signup"]
  const isPublicRoute = publicRoutes.some(route => pathname.startsWith(route))

  if (isProtectedRoute && !token) {
    // No token - redirect to login
    return NextResponse.redirect(new URL("/login", request.url))
  }

  if (isPublicRoute && token) {
    // Already authenticated - redirect to dashboard
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/login",
    "/signup"
  ]
}
```

**Rationale**:
- Middleware runs before page rendering (fast redirect)
- Prevents flash of protected content
- Redirects authenticated users away from login/signup pages

**Alternatives Considered**:
- Client-side protection in layout/page components: Rejected (causes flash of content, slower)
- Server-side protection in Server Components: Supplementary (middleware is first line of defense)

---

### 6. TypeScript Types for API Responses

**Question**: How to maintain type safety between frontend API calls and backend Pydantic responses?

**Research Conducted**:
- TypeScript type generation tools
- Pydantic to TypeScript conversion
- Manual type definition patterns

**Decision**: Manually define TypeScript types matching Pydantic schemas

**Implementation Pattern**:

**Backend (schemas/task.py)**:

```python
from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**Frontend (lib/types.ts)**:

```typescript
export interface Task {
  id: number
  user_id: number
  title: string
  description: string | null
  completed: boolean
  created_at: string // ISO date string
  updated_at: string
}

export interface TaskCreateRequest {
  title: string
  description?: string
}

export interface TaskUpdateRequest {
  title?: string
  description?: string
}

export interface TaskListResponse {
  tasks: Task[]
}

export interface TaskResponse {
  task: Task
}
```

**Rationale**:
- Simple and explicit (no code generation tooling required)
- Full control over type definitions
- Easy to maintain for Phase 2 MVP scale

**Alternatives Considered**:
- openapi-typescript generator: Deferred (adds build complexity, overkill for 5 endpoints)
- Shared TypeScript/Python types: Rejected (no simple solution exists)

---

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Next.js | 16+ | React framework with App Router |
| | TypeScript | 5.x | Type safety |
| | Tailwind CSS | 3.x | Styling |
| | Better Auth | 1.x | Authentication with JWT |
| **Backend** | FastAPI | 0.104+ | Python web framework |
| | SQLModel | 0.0.14+ | ORM (combines SQLAlchemy + Pydantic) |
| | python-jose | 3.x | JWT encoding/decoding |
| | passlib | 1.7+ | Password hashing (bcrypt) |
| **Database** | Neon PostgreSQL | Cloud | Serverless PostgreSQL |
| **Testing** | Jest | 29+ | Frontend unit tests |
| | React Testing Library | 14+ | Component testing |
| | Playwright | 1.40+ | E2E testing |
| | pytest | 7+ | Backend tests |

## Best Practices Consolidated

### Security

1. **JWT Storage**: httpOnly cookies only (never localStorage)
2. **Password Hashing**: bcrypt with salt (via passlib)
3. **User Isolation**: Mandatory user_id filter in ALL database queries
4. **Input Validation**: Pydantic models (backend), form validation (frontend)
5. **CORS**: Restrict to frontend origin only
6. **Environment Variables**: Never commit secrets to git

### Performance

1. **Database Connections**: Use Neon pooler URL for connection pooling
2. **React Rendering**: Server Components by default, Client Components only when needed
3. **API Response Size**: Return only necessary fields
4. **Query Optimization**: Add indexes on user_id, created_at columns

### Code Organization

1. **Frontend Structure**: app/ (pages), components/ (UI), lib/ (utilities, types, API client)
2. **Backend Structure**: models/ (SQLModel), routes/ (endpoints), schemas/ (Pydantic), middleware/ (JWT)
3. **Type Safety**: TypeScript strict mode, Pydantic models for all requests/responses
4. **Error Handling**: Try/catch (frontend), HTTPException (backend), error boundaries (React)

### Testing

1. **Backend**: pytest with TestClient for API endpoint tests
2. **Frontend**: Jest + RTL for components, Playwright for E2E flows
3. **User Isolation**: Dedicated test suite (test_user_isolation.py)
4. **Coverage Target**: 80%+ for both frontend and backend

## Implementation Readiness

**All NEEDS CLARIFICATION items resolved**: ✅

| Topic | Status | Decision |
|-------|--------|----------|
| Better Auth configuration | ✅ Resolved | JWT plugin with httpOnly cookies |
| JWT token sharing | ✅ Resolved | Shared BETTER_AUTH_SECRET |
| SQLModel + Neon connection | ✅ Resolved | Neon pooler URL with sync engine |
| User isolation pattern | ✅ Resolved | Dependency injection with mandatory user_id filter |
| Route protection | ✅ Resolved | Next.js middleware.ts |
| Type safety | ✅ Resolved | Manual TypeScript types matching Pydantic |

---

**Research Phase**: ✅ **COMPLETE**
**Next Phase**: Design & Contracts (data-model.md, contracts/, quickstart.md)
