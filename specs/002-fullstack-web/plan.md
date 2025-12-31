# Implementation Plan: Full-Stack Web Todo Application with Authentication

**Branch**: `002-fullstack-web` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web/spec.md`
**Phase**: Phase 2 - Full-Stack Web Application

## Summary

Transform Phase 1 console Todo application into a secure, multi-user web application with persistent storage. Users signup/login via Better Auth, manage personal tasks through a responsive Next.js dashboard, and all data persists in Neon PostgreSQL with strict user isolation enforced by JWT-verified backend API.

**Primary requirement**: Multi-user task management with authentication and persistent storage
**Technical approach**: Monorepo with Next.js frontend + FastAPI backend + Better Auth JWT + Neon PostgreSQL

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16+ (App Router)
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16+, Better Auth, Tailwind CSS 3.x, TypeScript 5.x
- Backend: FastAPI 0.1 04+, SQLModel 0.0.14+, Pydantic 2.x, python-jose (JWT), passlib (password hashing)

**Storage**: Neon Serverless PostgreSQL (cloud-hosted, connection pooling enabled)

**Testing**:
- Frontend: Jest + React Testing Library (unit/integration), Playwright or Cypress (E2E)
- Backend: pytest + TestClient (FastAPI built-in)

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge - modern versions)
- Backend: Python server (local development, deployable to Railway/Render/Vercel Functions)

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- Signup/login flows: < 1 minute total
- Task CRUD operations: < 1 second response time
- Dashboard page load: < 2 seconds
- Support 10 concurrent users without degradation

**Constraints**:
- No Docker/Kubernetes (per Phase 2 constitution)
- No console/CLI remnants from Phase 1
- JWT tokens stored in httpOnly cookies only (no localStorage)
- All database queries MUST filter by user_id (no cross-user data access)
- No external libraries beyond prescribed tech stack

**Scale/Scope**:
- MVP for 10-100 users
- Single-region deployment
- No real-time features (WebSockets out of scope)
- No file uploads or attachments

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase 2 Core Constraints Compliance

| Constraint | Status | Evidence |
|------------|--------|----------|
| **Frontend: Next.js 16+ with App Router** | ✅ PASS | Planned Next.js 16+ with App Router, TypeScript, Tailwind CSS |
| **Backend: Python FastAPI** | ✅ PASS | Planned FastAPI with Python 3.13+ |
| **ORM: SQLModel** | ✅ PASS | Planned SQLModel for database models |
| **Database: Neon PostgreSQL** | ✅ PASS | Planned Neon Serverless PostgreSQL |
| **Authentication: Better Auth + JWT** | ✅ PASS | Planned Better Auth with JWT tokens, shared BETTER_AUTH_SECRET |
| **No console/CLI remnants** | ✅ PASS | Pure web application, no CLI code |
| **No prohibited tech (Docker, K8s, etc.)** | ✅ PASS | No Docker, Kubernetes, Kafka, Dapr, MCP tools |
| **No unauthorized external libraries** | ✅ PASS | Only prescribed stack dependencies |

### Architecture & Security Standards Compliance

| Standard | Status | Evidence |
|----------|--------|----------|
| **Monorepo structure (/frontend, /backend, /specs)** | ✅ PASS | Planned monorepo layout |
| **Stateless JWT authentication** | ✅ PASS | JWT tokens with no server-side session storage |
| **Backend JWT verification on every request** | ✅ PASS | Planned global middleware |
| **User isolation (all queries filter by user_id)** | ✅ PASS | Database schema includes user_id FK, all queries scoped |
| **Protected API endpoints (401 without token)** | ✅ PASS | Middleware returns 401 for invalid/missing JWT |
| **Environment variables for secrets** | ✅ PASS | BETTER_AUTH_SECRET, DATABASE_URL in .env |
| **No hardcoded secrets** | ✅ PASS | .env files with .env.example templates |

### Code Quality & Testing Standards Compliance

| Standard | Status | Evidence |
|----------|--------|----------|
| **Full type safety (TS frontend, Pydantic backend)** | ✅ PASS | TypeScript + SQLModel/Pydantic models |
| **Modular design with separation of concerns** | ✅ PASS | Frontend (components/lib/app), Backend (models/routes/middleware) |
| **Server Components by default (Next.js)** | ✅ PASS | App Router defaults to Server Components |
| **Clean API client abstraction (/lib/api.ts)** | ✅ PASS | Planned centralized API client |
| **Comprehensive error handling** | ✅ PASS | HTTP status codes, try/catch, error boundaries |
| **Defensive input validation** | ✅ PASS | Pydantic models, frontend form validation |
| **TDD with 80%+ coverage** | ✅ PASS | Jest/Playwright (frontend), pytest (backend) |

**Constitution Gate**: ✅ **PASS** - All Phase 2 constraints satisfied

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions, best practices)
├── data-model.md        # Phase 1 output (database schema, entity relationships)
├── quickstart.md        # Phase 1 output (local dev setup instructions)
├── contracts/           # Phase 1 output (API endpoint specifications)
│   ├── auth-endpoints.md     # Signup, login, logout endpoints
│   └── task-endpoints.md     # Task CRUD endpoints
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todo_app/
├── frontend/            # Next.js 16+ App Router application
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx        # Login page
│   │   │   └── signup/
│   │   │       └── page.tsx        # Signup page
│   │   ├── (protected)/
│   │   │   └── dashboard/
│   │   │       └── page.tsx        # Protected dashboard (requires JWT)
│   │   ├── layout.tsx              # Root layout with Better Auth provider
│   │   ├── page.tsx                # Landing page (redirects to login/dashboard)
│   │   └── middleware.ts           # Route protection middleware
│   ├── components/
│   │   ├── TaskList.tsx            # Task list component
│   │   ├── TaskForm.tsx            # Add/edit task form
│   │   ├── TaskItem.tsx            # Individual task display
│   │   └── ui/                     # Reusable UI components (Button, Input, etc.)
│   ├── lib/
│   │   ├── api.ts                  # API client with JWT attachment
│   │   ├── auth.ts                 # Better Auth configuration
│   │   └── types.ts                # TypeScript type definitions
│   ├── public/                     # Static assets
│   ├── tests/
│   │   ├── unit/                   # Jest + React Testing Library tests
│   │   └── e2e/                    # Playwright/Cypress tests
│   ├── .env.local.example          # Environment variable template
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── CLAUDE.md                   # Frontend agent instructions
├── backend/             # FastAPI application
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py             # User SQLModel (managed by Better Auth)
│   │   │   └── task.py             # Task SQLModel with user_id FK
│   │   ├── routes/
│   │   │   ├── auth.py             # /api/auth endpoints (signup, login, logout)
│   │   │   └── tasks.py            # /api/tasks endpoints (CRUD)
│   │   ├── middleware/
│   │   │   └── jwt_auth.py         # JWT verification middleware
│   │   ├── schemas/
│   │   │   ├── auth.py             # Pydantic models for auth requests/responses
│   │   │   └── task.py             # Pydantic models for task requests/responses
│   │   ├── core/
│   │   │   ├── config.py           # Settings (DATABASE_URL, BETTER_AUTH_SECRET)
│   │   │   └── security.py         # Password hashing, JWT utilities
│   │   ├── database.py             # Database connection and session factory
│   │   ├── dependencies.py         # Dependency injection (get_db, get_current_user)
│   │   └── main.py                 # FastAPI app initialization
│   ├── tests/
│   │   ├── test_auth.py            # Auth endpoint tests
│   │   ├── test_tasks.py           # Task endpoint tests
│   │   └── test_user_isolation.py  # User isolation security tests
│   ├── alembic/                    # Database migrations (optional for Phase 2)
│   ├── .env.example                # Environment variable template
│   ├── requirements.txt            # Python dependencies
│   ├── pyproject.toml              # Python project configuration
│   └── CLAUDE.md                   # Backend agent instructions
├── src/                 # Phase 1 code (archived, not used in Phase 2)
│   └── todo_app/        # Keep for reference but don't import
├── .gitignore
├── README.md            # Root project documentation
└── CLAUDE.md            # Root agent instructions
```

**Structure Decision**: Monorepo with separate frontend/ and backend/ directories. Frontend uses Next.js App Router with route groups for organization ((auth) for public routes, (protected) for authenticated routes). Backend follows FastAPI best practices with models/routes/schemas separation.

## Complexity Tracking

> **No constitutional violations requiring justification**

All technologies and patterns align with Phase 2 constitution requirements.

## Phase 0: Research & Technology Decisions

### Overview

Research phase resolves all technology-specific questions and establishes best practices for the prescribed stack. Since the constitution mandates specific technologies (Next.js 16+, FastAPI, Better Auth, SQLModel, Neon PostgreSQL), research focuses on **how to use these technologies correctly** rather than **which technologies to choose**.

### Research Tasks

1. **Better Auth Integration with Next.js App Router**
   - Question: How to configure Better Auth for JWT tokens with Next.js 16+ App Router?
   - Research: Better Auth documentation, JWT plugin configuration, httpOnly cookie setup
   - Output: Configuration pattern for lib/auth.ts

2. **JWT Token Sharing Between Frontend and Backend**
   - Question: How to securely share JWT tokens between Next.js and FastAPI?
   - Research: BETTER_AUTH_SECRET synchronization, JWT verification in FastAPI
   - Output: Environment variable setup and middleware implementation pattern

3. **SQLModel with Neon PostgreSQL**
   - Question: How to connect SQLModel to Neon Serverless PostgreSQL?
   - Research: Neon connection strings, connection pooling, async vs sync sessions
   - Output: Database connection configuration in database.py

4. **User Isolation Patterns**
   - Question: Best practices for enforcing user_id filtering in all database queries?
   - Research: SQLModel query patterns, dependency injection for current user
   - Output: Dependency pattern for get_current_user and query filtering

5. **Next.js Middleware for Route Protection**
   - Question: How to protect routes with JWT verification in App Router middleware?
   - Research: middleware.ts patterns, redirect logic, token extraction from cookies
   - Output: Middleware implementation pattern

6. **TypeScript Types for API Responses**
   - Question: How to maintain type safety between frontend API calls and backend responses?
   - Research: Shared type definitions, Pydantic schema conversion to TypeScript
   - Output: Type generation or manual type definition approach

### Research Deliverable

See [research.md](./research.md) for consolidated findings with decisions, rationale, and implementation patterns.

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions, field specifications, and relationship mappings.

**Key Entities**:

1. **User**
   - Managed by Better Auth
   - Fields: id (UUID/int), email (unique), hashed_password, created_at
   - Relationships: One user → Many tasks

2. **Task**
   - User-specific todo item
   - Fields: id (int), user_id (FK), title (str, 1-200), description (str, 0-1000, nullable), completed (bool), created_at, updated_at
   - Relationships: Many tasks → One user
   - Constraints: user_id NOT NULL, cascade delete on user deletion

### API Contracts

See [contracts/auth-endpoints.md](./contracts/auth-endpoints.md) and [contracts/task-endpoints.md](./contracts/task-endpoints.md) for OpenAPI-style endpoint specifications.

**Authentication Endpoints** (`/api/auth`):

1. `POST /api/auth/signup`
   - Request: `{ email: string, password: string }`
   - Response 201: `{ user_id: int, email: string, message: "Account created" }`
   - Errors: 400 (validation), 409 (email exists)

2. `POST /api/auth/login`
   - Request: `{ email: string, password: string }`
   - Response 200: `{ token: string (JWT), user_id: int, email: string }` + httpOnly cookie set
   - Errors: 401 (invalid credentials)

3. `POST /api/auth/logout`
   - Request: None (requires valid JWT)
   - Response 200: `{ message: "Logged out" }` + httpOnly cookie cleared
   - Errors: 401 (no valid token)

**Task Endpoints** (`/api/tasks` - all require JWT):

1. `GET /api/tasks`
   - Request: None (JWT contains user_id)
   - Response 200: `{ tasks: Task[] }` (only authenticated user's tasks)
   - Errors: 401 (no token)

2. `POST /api/tasks`
   - Request: `{ title: string, description?: string }`
   - Response 201: `{ task: Task }`
   - Errors: 400 (validation), 401 (no token)

3. `PUT /api/tasks/{id}`
   - Request: `{ title?: string, description?: string }`
   - Response 200: `{ task: Task }`
   - Errors: 400 (validation), 401 (no token), 403 (not owner), 404 (not found)

4. `PATCH /api/tasks/{id}/complete`
   - Request: None
   - Response 200: `{ task: Task }` (with toggled completed status)
   - Errors: 401 (no token), 403 (not owner), 404 (not found)

5. `DELETE /api/tasks/{id}`
   - Request: None
   - Response 204: No content
   - Errors: 401 (no token), 403 (not owner), 404 (not found)

### Local Development Quickstart

See [quickstart.md](./quickstart.md) for step-by-step setup instructions.

**Prerequisites**:
- Node.js 20+ and npm
- Python 3.13+
- Neon PostgreSQL account (free tier)

**Environment Setup**:

```bash
# Frontend (.env.local)
BETTER_AUTH_SECRET=your-secret-here
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (.env)
BETTER_AUTH_SECRET=your-secret-here  # MUST match frontend
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/dbname
```

**Running Locally**:

```bash
# Terminal 1: Frontend
cd frontend
npm install
npm run dev  # http://localhost:3000

# Terminal 2: Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload  # http://localhost:8000
```

## Implementation Sequence

### Phase 0: Research (Current Phase Output)

✅ Document technology decisions in [research.md](./research.md)

### Phase 1: Design (Current Phase Output)

✅ Define data models in [data-model.md](./data-model.md)
✅ Specify API contracts in [contracts/](./contracts/)
✅ Create quickstart guide in [quickstart.md](./quickstart.md)

### Phase 2: Task Breakdown (Next Command: `/sp.tasks`)

After this plan is approved, run `/sp.tasks` to generate atomic implementation tasks covering:

1. **Monorepo Setup**
   - Initialize frontend/ and backend/ directories
   - Configure package managers and build tools
   - Create CLAUDE.md files for agent context

2. **Database & Models**
   - Create SQLModel models (User, Task)
   - Configure Neon PostgreSQL connection
   - Set up dependency injection for database sessions

3. **Authentication**
   - Configure Better Auth in frontend
   - Implement signup/login/logout pages
   - Implement JWT verification middleware in backend
   - Create protected route middleware in frontend

4. **Backend API**
   - Implement /api/auth endpoints
   - Implement /api/tasks endpoints with user_id filtering
   - Add request/response validation
   - Implement error handling

5. **Frontend UI**
   - Create dashboard page layout
   - Implement task list component
   - Implement task form (add/edit)
   - Implement task actions (toggle, delete)
   - Add loading states and error handling

6. **Testing**
   - Write backend tests (pytest + TestClient)
   - Write frontend unit tests (Jest + RTL)
   - Write E2E tests (Playwright)
   - Verify user isolation security

7. **Documentation & Deployment**
   - Update README with full setup instructions
   - Create environment variable examples
   - Document deployment process

## Risk Analysis and Mitigation

### Top 3 Risks

1. **JWT Secret Mismatch Between Frontend and Backend**
   - **Impact**: Authentication completely broken, users cannot login
   - **Probability**: Medium (manual environment setup)
   - **Mitigation**:
     - Validate secret synchronization in early local testing
     - Add startup check in backend to verify secret is set
     - Document environment variable setup clearly in quickstart.md
   - **Kill Switch**: None needed (development-only issue)

2. **User Isolation Breach (Cross-User Data Access)**
   - **Impact**: CRITICAL - data leak between users, disqualifying security failure
   - **Probability**: Low (if query filters are consistently applied)
   - **Mitigation**:
     - Mandatory user_id filter in ALL database queries
     - Dependency injection pattern forces current user context
     - Dedicated security tests verify isolation (test_user_isolation.py)
     - Code review checklist item for user_id filtering
   - **Kill Switch**: Manual review of all database queries before deployment

3. **Token Expiry Handling Edge Cases**
   - **Impact**: User experience degradation (unexpected logouts, lost work)
   - **Probability**: Medium (token expiry is standard but must be handled gracefully)
   - **Mitigation**:
     - Configure reasonable token expiry (e.g., 24 hours)
     - Frontend API client catches 401 and redirects to login
     - Display "Session expired" message before redirect
     - Better Auth auto-refresh tokens if configured
   - **Kill Switch**: Increase token expiry duration in emergency

## Evaluation and Validation

### Definition of Done

**Code Completion**:
- [ ] All frontend pages and components implemented
- [ ] All backend endpoints implemented and tested
- [ ] Database models created and migrations applied (if using Alembic)
- [ ] Environment variable examples created

**Testing**:
- [ ] Backend tests: 80%+ coverage (pytest)
- [ ] Frontend unit tests: 80%+ coverage (Jest)
- [ ] E2E tests: Critical flows covered (signup → login → CRUD → logout)
- [ ] User isolation tests: Verify User A cannot access User B's tasks

**Security**:
- [ ] No SQL injection vulnerabilities (parameterized queries only)
- [ ] No XSS vulnerabilities (Next.js auto-escaping verified)
- [ ] JWT tokens stored in httpOnly cookies (not localStorage)
- [ ] All /api endpoints protected with JWT verification
- [ ] User_id filtering applied to all database queries

**Documentation**:
- [ ] README.md updated with Phase 2 setup instructions
- [ ] Environment variable examples created (.env.example files)
- [ ] API documentation available at /api/docs (FastAPI auto-generated)
- [ ] quickstart.md validated with fresh local setup

**Performance**:
- [ ] Signup/login flows complete in < 1 minute
- [ ] Task CRUD operations respond in < 1 second
- [ ] Dashboard loads in < 2 seconds
- [ ] Tested with 10 concurrent users (load testing optional)

### Output Validation

**Format Validation**:
- All API responses follow JSON format specified in contracts
- HTTP status codes match specifications (201 for create, 204 for delete, etc.)
- Error responses include descriptive messages

**Requirement Validation**:
- All 30 functional requirements from spec.md implemented
- All 12 success criteria met
- All edge cases handled

**Safety Validation**:
- No hardcoded secrets in codebase (git grep for BETTER_AUTH_SECRET, DATABASE_URL)
- No console.log of sensitive data in production builds
- CORS configured correctly (frontend origin allowed, others blocked)

## Architecture Decision Records (ADRs)

**Significant Decisions Requiring Documentation**:

1. **Monorepo Structure**: Frontend and backend in same repository
   - **Decision**: Use monorepo with /frontend and /backend directories
   - **Rationale**: Shared specifications, easier local development, single git repo
   - **Alternatives**: Separate repositories (rejected due to coordination overhead)
   - **Run**: `/sp.adr monorepo-structure-decision`

2. **JWT Storage Strategy**: httpOnly Cookies vs localStorage
   - **Decision**: Store JWT in httpOnly cookies set by Better Auth
   - **Rationale**: XSS protection (cookies not accessible via JavaScript)
   - **Alternatives**: localStorage (rejected due to XSS vulnerability)
   - **Run**: `/sp.adr jwt-storage-httponly-cookies`

3. **Better Auth vs Custom JWT Implementation**
   - **Decision**: Use Better Auth library for authentication
   - **Rationale**: Constitution mandates Better Auth; provides JWT plugin and secure defaults
   - **Alternatives**: Custom JWT implementation (rejected, not allowed by constitution)
   - **Run**: `/sp.adr better-auth-for-authentication`

**Note**: Run `/sp.adr <title>` after plan approval to formally document these architectural decisions.

## Next Steps

After approval of this implementation plan:

1. ✅ Run `/sp.tasks` to generate atomic task breakdown with acceptance criteria
2. ✅ Approve tasks before beginning implementation
3. ✅ Follow TDD workflow: Write tests → Implement → Verify → Refactor
4. ✅ Create ADRs for significant architectural decisions
5. ✅ Track progress using TodoWrite tool for task completion

---

**Plan Status**: ✅ Ready for Task Breakdown
**Constitutional Compliance**: ✅ All Phase 2 constraints satisfied
**Next Command**: `/sp.tasks`
