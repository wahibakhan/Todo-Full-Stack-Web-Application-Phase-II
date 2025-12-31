---
id: 002
title: phase-2-implementation-plan
stage: plan
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-fullstack-web
branch: 002-fullstack-web
user: user
command: /sp.plan
labels: ["planning", "architecture", "phase-2", "fullstack-web", "nextjs", "fastapi", "better-auth"]
links:
  spec: specs/002-fullstack-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-fullstack-web/plan.md
  - specs/002-fullstack-web/research.md
  - specs/002-fullstack-web/data-model.md
  - specs/002-fullstack-web/contracts/auth-endpoints.md
  - specs/002-fullstack-web/contracts/task-endpoints.md
  - specs/002-fullstack-web/quickstart.md
  - specs/002-fullstack-web/checklists/requirements.md
tests:
  - None (planning phase)
---

## Prompt

User requested implementation plan for Phase 2 using `/sp.plan` command with the following architectural overview:

```
# speckit.plan
## Implementation Plan for Phase 2: Full-Stack Web Application

### Architectural Overview
Monorepo with clear separation of concerns:

- **Frontend (Next.js)**: Handles authentication UI, protected routes, responsive Todo dashboard, API client with JWT attachment
- **Backend (FastAPI)**: Provides secure REST API, JWT verification middleware, user-filtered CRUD operations, database integration
- **Shared Specs**: Centralized specifications driving both sides
- **Authentication Flow**: Better Auth (frontend) issues JWT → Frontend attaches to headers → Backend verifies and extracts user_id

### Component Breakdown & Implementation Sequence

1. **Monorepo Foundation**
   - Create /frontend and /backend directories
   - Initialize Next.js app (App Router, TypeScript, Tailwind)
   - Initialize FastAPI project structure
   - Add root, frontend, and backend CLAUDE.md files
   - Configure .spec-kit if used

2. **Database Schema & Models**
   - Define SQLModel models reflecting schema (User managed by Better Auth, Task with user_id FK)
   - Create database connection module using Neon DATABASE_URL
   - Implement session dependency injection

3. **Authentication Integration**
   - Configure Better Auth in frontend with JWT plugin enabled
   - Set shared BETTER_AUTH_SECRET in both environments
   - Implement login/signup pages
   - Configure httpOnly cookie for JWT storage

4. **Backend Security Layer**
   - Implement JWT verification middleware
   - Extract and validate user_id from token
   - Apply middleware globally to /api routes
   - Create authenticated dependency returning current user

5. **REST API Implementation (User-Filtered)**
   - Create task routes under /api/tasks
   - All operations filter/query by authenticated user_id
   - Proper HTTP status codes and error handling
   - Use Pydantic models for request/response

6. **Frontend API Client**
   - Create /lib/api.ts with JWT attachment to every request
   - Handle 401 redirects to login
   - Type-safe fetch wrappers

7. **Todo Dashboard UI**
   - Protected /dashboard route
   - Task list with status indicators
   - Forms for add/update/delete/toggle
   - Loading and error states
   - Responsive design with Tailwind

8. **Integration & Polish**
   - End-to-end testing: signup → login → CRUD → logout → new user
   - Environment configuration documentation
   - README with local run instructions (npm run dev + uvicorn)

### Risk Mitigation
- JWT secret mismatch → Early local testing
- User isolation breaches → Strict filtering in all queries
- Token expiry → Graceful redirect to login
- Database connection issues → Use Neon connection pooler URL

### Deployment Preparation
- Frontend ready for Vercel
- Backend ready for Railway/Render
- Environment variables documented

### Compliance Summary
- Full adherence to Phase 2 constitution
- All changes traceable to updated speckit.specify
- Secure, professional, production-grade patterns
```

## Response snapshot

Successfully executed the `/sp.plan` workflow and created comprehensive Phase 2 implementation plan with the following artifacts:

### Phase 0: Research & Technology Decisions (research.md)
Resolved all technical unknowns with implementation patterns:
1. **Better Auth Integration**: JWT plugin configuration with httpOnly cookies
2. **JWT Token Sharing**: Shared BETTER_AUTH_SECRET between Next.js and FastAPI
3. **SQLModel + Neon Connection**: Connection pooler with sync engine
4. **User Isolation Patterns**: Dependency injection with mandatory user_id filtering
5. **Route Protection**: Next.js middleware.ts for JWT verification
6. **TypeScript Types**: Manual type definitions matching Pydantic schemas

### Phase 1: Design & Contracts Artifacts Created:

1. **plan.md** (100+ sections):
   - Technical context with exact versions
   - Constitution compliance checks
   - Project structure (monorepo: /frontend, /backend, /specs)
   - 7 implementation phases with acceptance criteria

2. **data-model.md** (363 lines):
   - User entity (managed by Better Auth)
   - Task entity with user_id foreign key
   - Validation rules and state transitions
   - Database schema DDL
   - User isolation enforcement patterns

3. **contracts/auth-endpoints.md** (300 lines):
   - POST /api/auth/signup (email/password → user creation)
   - POST /api/auth/login (credentials → JWT cookie)
   - POST /api/auth/logout (clear JWT)
   - Security considerations (password hashing, httpOnly cookies)
   - Testing checklist (15 items)

4. **contracts/task-endpoints.md** (501 lines):
   - GET /api/tasks (list user's tasks)
   - POST /api/tasks (create task)
   - PUT /api/tasks/{id} (update task)
   - PATCH /api/tasks/{id}/complete (toggle completion)
   - DELETE /api/tasks/{id} (delete task)
   - User isolation enforcement examples
   - Testing checklist (16 items)

5. **quickstart.md** (501 lines):
   - Prerequisites (Node 20+, Python 3.13+, Neon PostgreSQL)
   - Step-by-step Neon database setup
   - Frontend setup (npm install, .env.local)
   - Backend setup (pip install, .env)
   - Running instructions (parallel terminals)
   - Verification steps (signup → CRUD → user isolation test)
   - Common issues and solutions (CORS, port conflicts, JWT errors)

### Constitution Compliance:
✅ All Phase 2 constraints satisfied:
- Next.js 16+ with App Router
- FastAPI backend
- SQLModel ORM
- Neon Serverless PostgreSQL
- Better Auth with JWT tokens
- Monorepo structure
- No Phase 1 console remnants
- Security-first architecture

### Technology Stack Confirmed:
- **Frontend**: Next.js 16+, TypeScript 5.x, Tailwind CSS 3.x, Better Auth 1.x
- **Backend**: FastAPI 0.104+, SQLModel 0.0.14+, python-jose 3.x, passlib 1.7+
- **Database**: Neon PostgreSQL with connection pooling
- **Testing**: Jest + RTL + Playwright (FE), pytest (BE)

## Outcome

- ✅ Impact: Created comprehensive Phase 2 implementation plan with 7 artifacts (1 plan, 1 research, 1 data model, 2 API contracts, 1 quickstart guide, 1 requirements checklist)
- 🧪 Tests: No tests run (planning phase)
- 📁 Files: 7 files created in specs/002-fullstack-web/
- 🔁 Next prompts: `/sp.tasks` to generate atomic task breakdown based on approved plan
- 🧠 Reflection: Successfully completed all planning artifacts without errors. All technical unknowns resolved through research. Constitution compliance verified. Ready for task generation phase.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (planning phase, no code generated)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
