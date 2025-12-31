# Tasks: Full-Stack Web Todo Application with Authentication

**Input**: Design documents from `/specs/002-fullstack-web/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification - focusing on implementation tasks
**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- All tasks include exact file paths

## Path Conventions

- **Monorepo structure**: `frontend/` and `backend/` at repository root
- Frontend: Next.js App Router with `app/`, `components/`, `lib/`
- Backend: FastAPI with `app/models/`, `app/routes/`, `app/middleware/`, `app/schemas/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Monorepo initialization and basic project structure

- [ ] T001 Create monorepo directory structure (frontend/, backend/, specs/)
- [ ] T002 Initialize Next.js 16+ project in frontend/ with TypeScript and Tailwind CSS
- [ ] T003 Initialize FastAPI project structure in backend/ with Python 3.13+
- [ ] T004 [P] Create frontend/.env.local.example with BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL, DATABASE_URL
- [ ] T005 [P] Create backend/.env.example with BETTER_AUTH_SECRET, DATABASE_URL
- [ ] T006 [P] Create frontend/package.json with Next.js 16+, Better Auth, Tailwind CSS dependencies
- [ ] T007 [P] Create backend/requirements.txt with FastAPI, SQLModel, python-jose, passlib, psycopg2-binary
- [ ] T008 [P] Configure TypeScript (frontend/tsconfig.json) with strict mode
- [ ] T009 [P] Configure Tailwind CSS (frontend/tailwind.config.ts)
- [ ] T010 [P] Create root README.md with monorepo structure overview
- [ ] T011 [P] Create frontend/CLAUDE.md with frontend agent instructions
- [ ] T012 [P] Create backend/CLAUDE.md with backend agent instructions
- [ ] T013 [P] Add .gitignore entries for .env files, node_modules/, __pycache__/, venv/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Models Foundation

- [ ] T014 Create User SQLModel in backend/app/models/user.py (id, email, hashed_password, created_at)
- [ ] T015 Create Task SQLModel in backend/app/models/task.py (id, user_id FK, title, description, completed, created_at, updated_at)
- [ ] T016 Create database connection module in backend/app/database.py with Neon PostgreSQL engine
- [ ] T017 Create database session dependency in backend/app/dependencies.py (get_session function)

### Authentication Infrastructure

- [ ] T018 Configure Better Auth in frontend/lib/auth.ts with JWT plugin and httpOnly cookies
- [ ] T019 Create backend/app/core/security.py with password hashing (passlib bcrypt) and JWT utilities (python-jose)
- [ ] T020 Create backend/app/core/config.py with settings (BETTER_AUTH_SECRET, DATABASE_URL from env)
- [ ] T021 Create JWT verification middleware in backend/app/middleware/jwt_auth.py (extract user_id from token)
- [ ] T022 Create get_current_user dependency in backend/app/dependencies.py (uses JWT middleware)

### API Structure

- [ ] T023 Create FastAPI app initialization in backend/app/main.py with CORS middleware
- [ ] T024 Configure CORS to allow frontend origin (http://localhost:3000)
- [ ] T025 Create Pydantic schemas for auth in backend/app/schemas/auth.py (SignupRequest, LoginRequest, AuthResponse)
- [ ] T026 Create Pydantic schemas for tasks in backend/app/schemas/task.py (TaskCreate, TaskUpdate, TaskResponse)

### Frontend Structure

- [ ] T027 [P] Create API client in frontend/lib/api.ts with credentials: "include" for cookies
- [ ] T028 [P] Create TypeScript types in frontend/lib/types.ts (User, Task, TaskCreateRequest, TaskUpdateRequest)
- [ ] T029 [P] Create root layout in frontend/app/layout.tsx with Better Auth provider
- [ ] T030 [P] Create middleware in frontend/app/middleware.ts for route protection (check auth-token cookie)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication & Session Management (Priority: P1) 🎯 MVP

**Goal**: Users can signup, login, view protected dashboard, and logout securely with JWT tokens

**Independent Test**: Create account → Login → Access dashboard → Logout → Verify protected routes redirect to login

### Backend Implementation for US1

- [ ] T031 [P] [US1] Implement POST /api/auth/signup endpoint in backend/app/routes/auth.py (hash password, create user, return 201)
- [ ] T032 [P] [US1] Implement POST /api/auth/login endpoint in backend/app/routes/auth.py (verify password, issue JWT, set httpOnly cookie)
- [ ] T033 [P] [US1] Implement POST /api/auth/logout endpoint in backend/app/routes/auth.py (clear httpOnly cookie)
- [ ] T034 [US1] Add authentication routes to FastAPI app in backend/app/main.py (router for /api/auth)
- [ ] T035 [US1] Add error handling for auth endpoints (400 validation, 401 invalid credentials, 409 duplicate email)

### Frontend Pages for US1

- [ ] T036 [P] [US1] Create signup page in frontend/app/(auth)/signup/page.tsx with email/password form
- [ ] T037 [P] [US1] Create login page in frontend/app/(auth)/login/page.tsx with email/password form
- [ ] T038 [P] [US1] Create dashboard page in frontend/app/(protected)/dashboard/page.tsx (protected route, displays user email)
- [ ] T039 [US1] Create landing page in frontend/app/page.tsx (redirects to /login or /dashboard based on auth status)
- [ ] T040 [US1] Implement logout button component in frontend/components/LogoutButton.tsx (calls /api/auth/logout)

### Frontend API Integration for US1

- [ ] T041 [US1] Implement signup API call in frontend/lib/api.ts (POST /api/auth/signup)
- [ ] T042 [US1] Implement login API call in frontend/lib/api.ts (POST /api/auth/login)
- [ ] T043 [US1] Implement logout API call in frontend/lib/api.ts (POST /api/auth/logout)
- [ ] T044 [US1] Add 401 error handling in frontend/lib/api.ts (redirect to /login on unauthorized)

### Validation & Error Handling for US1

- [ ] T045 [US1] Add frontend form validation (email format, password min 8 chars) in signup/login pages
- [ ] T046 [US1] Add error toast/message component in frontend/components/ErrorMessage.tsx
- [ ] T047 [US1] Add success toast/message component in frontend/components/SuccessMessage.tsx
- [ ] T048 [US1] Display error messages on signup/login failures (invalid credentials, email exists)

**Checkpoint**: User Story 1 complete - users can signup, login, access dashboard, logout

---

## Phase 4: User Story 3 - Multi-User Data Isolation (Priority: P1) ⚠️ SECURITY CRITICAL

**Goal**: Enforce strict user isolation - each user sees ONLY their own tasks, zero data leaks

**Independent Test**: Create 2 users → Add tasks to each → Verify User A cannot see/modify User B's tasks

**Note**: Implemented alongside US2 as a cross-cutting security concern affecting all task operations

### Backend Security Enforcement for US3

- [ ] T049 [US3] Add user_id extraction to get_current_user dependency in backend/app/dependencies.py
- [ ] T050 [US3] Create user isolation test in backend/tests/test_user_isolation.py (verify cross-user access fails)
- [ ] T051 [US3] Add database index on tasks.user_id in backend/app/models/task.py for query performance
- [ ] T052 [US3] Document user_id filtering requirement in backend/CLAUDE.md (all task queries MUST filter by user_id)

**Checkpoint**: User isolation framework ready - all task endpoints will enforce user_id filtering

---

## Phase 5: User Story 2 - Personal Task Management Dashboard (Priority: P2)

**Goal**: Authenticated users can view, create, update, toggle, and delete their personal tasks

**Independent Test**: Login → Create task → View in list → Update title → Toggle complete → Delete task

**Depends on**: US1 (authentication) and US3 (user isolation framework)

### Backend API for US2

- [ ] T053 [P] [US2] Implement GET /api/tasks endpoint in backend/app/routes/tasks.py (filter by user_id from JWT)
- [ ] T054 [P] [US2] Implement POST /api/tasks endpoint in backend/app/routes/tasks.py (auto-assign user_id, validate title 1-200 chars)
- [ ] T055 [P] [US2] Implement PUT /api/tasks/{id} endpoint in backend/app/routes/tasks.py (verify ownership via user_id filter)
- [ ] T056 [P] [US2] Implement PATCH /api/tasks/{id}/complete endpoint in backend/app/routes/tasks.py (toggle completed boolean)
- [ ] T057 [P] [US2] Implement DELETE /api/tasks/{id} endpoint in backend/app/routes/tasks.py (verify ownership, return 204)
- [ ] T058 [US2] Add task routes to FastAPI app in backend/app/main.py (router for /api/tasks with JWT dependency)
- [ ] T059 [US2] Add error handling for task endpoints (400 validation, 401 unauthorized, 404 not found/not owned)

### Frontend Components for US2

- [ ] T060 [P] [US2] Create TaskList component in frontend/components/TaskList.tsx (displays array of tasks)
- [ ] T061 [P] [US2] Create TaskItem component in frontend/components/TaskItem.tsx (single task with toggle/edit/delete buttons)
- [ ] T062 [P] [US2] Create TaskForm component in frontend/components/TaskForm.tsx (add/edit task with title and description inputs)
- [ ] T063 [US2] Create EmptyState component in frontend/components/EmptyState.tsx ("Add your first task" message)

### Frontend API Integration for US2

- [ ] T064 [P] [US2] Implement getTasks API call in frontend/lib/api.ts (GET /api/tasks)
- [ ] T065 [P] [US2] Implement createTask API call in frontend/lib/api.ts (POST /api/tasks)
- [ ] T066 [P] [US2] Implement updateTask API call in frontend/lib/api.ts (PUT /api/tasks/{id})
- [ ] T067 [P] [US2] Implement toggleTaskComplete API call in frontend/lib/api.ts (PATCH /api/tasks/{id}/complete)
- [ ] T068 [P] [US2] Implement deleteTask API call in frontend/lib/api.ts (DELETE /api/tasks/{id})

### Dashboard Integration for US2

- [ ] T069 [US2] Integrate TaskList into dashboard page in frontend/app/(protected)/dashboard/page.tsx
- [ ] T070 [US2] Add task creation functionality to dashboard (TaskForm component with submit handler)
- [ ] T071 [US2] Add loading state to dashboard (display spinner during API calls)
- [ ] T072 [US2] Add empty state to dashboard (show when no tasks exist)
- [ ] T073 [US2] Add delete confirmation dialog in frontend/components/ConfirmDialog.tsx

### Validation & UX for US2

- [ ] T074 [US2] Add frontend validation for task title (1-200 chars, required) in TaskForm
- [ ] T075 [US2] Add frontend validation for task description (max 1000 chars, optional) in TaskForm
- [ ] T076 [US2] Add real-time UI updates after create/update/delete (refresh task list)
- [ ] T077 [US2] Add visual completion status indicators ([ ] incomplete, [x] complete) in TaskItem
- [ ] T078 [US2] Add responsive design with Tailwind CSS (mobile to desktop) in all components

**Checkpoint**: User Story 2 complete - users can perform full CRUD operations on tasks

---

## Phase 6: User Story 4 - Task Persistence Across Sessions (Priority: P2)

**Goal**: Tasks persist in Neon PostgreSQL across browser sessions and server restarts

**Independent Test**: Create tasks → Close browser → Reopen and login → Verify tasks still exist

**Note**: Automatically satisfied by Phase 2 foundation (SQLModel + Neon PostgreSQL)

### Database Verification for US4

- [ ] T079 [US4] Run database migration/table creation in backend/app/main.py (SQLModel.metadata.create_all on startup)
- [ ] T080 [US4] Verify Neon connection pooling in backend/app/database.py (use pooler URL from quickstart.md)
- [ ] T081 [US4] Add database connection retry logic in backend/app/database.py (handle temporary connection failures)

### Persistence Validation for US4

- [ ] T082 [US4] Test task persistence across server restarts (restart backend, verify tasks remain)
- [ ] T083 [US4] Test JWT cookie persistence settings in frontend/lib/auth.ts (configure Max-Age for cookie)
- [ ] T084 [US4] Add updated_at timestamp auto-update in backend/app/models/task.py (set on modification)

**Checkpoint**: User Story 4 complete - all data persists reliably in database

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

### Documentation

- [ ] T085 [P] Update root README.md with Phase 2 setup instructions (link to quickstart.md)
- [ ] T086 [P] Create frontend/README.md with frontend-specific setup and commands
- [ ] T087 [P] Create backend/README.md with backend-specific setup and commands
- [ ] T088 [P] Validate quickstart.md by following steps on fresh machine

### Code Quality

- [ ] T089 [P] Add TypeScript strict mode checks and fix any errors in frontend/
- [ ] T090 [P] Add Python type hints to all functions in backend/app/
- [ ] T091 [P] Run linting on frontend (npm run lint) and fix issues
- [ ] T092 [P] Run linting on backend (ruff or pylint) and fix issues

### Security Hardening

- [ ] T093 [P] Verify no hardcoded secrets in codebase (git grep BETTER_AUTH_SECRET, DATABASE_URL)
- [ ] T094 [P] Verify all user inputs are validated on backend (Pydantic models enforce constraints)
- [ ] T095 [P] Verify SQL injection protection (SQLModel parameterized queries only)
- [ ] T096 [P] Verify XSS protection (Next.js auto-escaping, no dangerouslySetInnerHTML)

### Performance & UX

- [ ] T097 Add loading spinners to all async operations in frontend/components/
- [ ] T098 Add error boundaries in frontend/app/layout.tsx for graceful error handling
- [ ] T099 Optimize task list rendering (React.memo for TaskItem if needed)
- [ ] T100 Add success feedback for all user actions (toast messages on create/update/delete)

### Final Validation

- [ ] T101 Run full user flow test: Signup → Login → Create 5 tasks → Update → Toggle → Delete → Logout
- [ ] T102 Run multi-user isolation test: User A and User B with separate task lists
- [ ] T103 Test persistence: Create tasks → Close browser → Reopen → Verify tasks exist
- [ ] T104 Test error scenarios: Invalid login, duplicate email, unauthorized access, network errors
- [ ] T105 Verify all 12 success criteria from spec.md are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Story 1 (Phase 3)**: Depends on Foundational - Can start after Phase 2
- **User Story 3 (Phase 4)**: Depends on Foundational - Can start after Phase 2 (security framework)
- **User Story 2 (Phase 5)**: Depends on US1 (auth) and US3 (isolation) - Can start after Phase 3 & 4
- **User Story 4 (Phase 6)**: Depends on Foundational - Mostly satisfied by Phase 2, validation only
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Authentication)**: No dependencies on other stories - Can implement after Foundation
- **US3 (User Isolation)**: No dependencies on other stories - Security framework parallel to US1
- **US2 (Task Management)**: Depends on US1 (needs auth) and US3 (needs isolation) - Sequential after US1 + US3
- **US4 (Persistence)**: No dependencies on other stories - Automatic from Foundation

### Critical Path (Sequential Implementation)

1. Phase 1: Setup (T001-T013)
2. Phase 2: Foundational (T014-T030) ⚠️ MUST complete before user stories
3. Phase 3: US1 Authentication (T031-T048)
4. Phase 4: US3 User Isolation (T049-T052) - Can overlap with US1
5. Phase 5: US2 Task Management (T053-T078) - Requires US1 + US3
6. Phase 6: US4 Persistence (T079-T084) - Validation only
7. Phase 7: Polish (T085-T105)

### Parallel Opportunities

#### Within Setup (Phase 1)
- T004-T012 can all run in parallel (different config files)

#### Within Foundational (Phase 2)
- Models (T014-T015) in parallel
- Auth config (T018-T022) can overlap with database setup
- Frontend structure (T027-T030) in parallel with backend structure

#### Within US1 (Phase 3)
- Backend endpoints (T031-T033) in parallel
- Frontend pages (T036-T038) in parallel
- API integration (T041-T043) after pages

#### Within US2 (Phase 5)
- Backend endpoints (T053-T057) in parallel
- Frontend components (T060-T062) in parallel
- API calls (T064-T068) in parallel

#### Within Polish (Phase 7)
- Documentation (T085-T088) in parallel
- Code quality (T089-T092) in parallel
- Security checks (T093-T096) in parallel

---

## Parallel Execution Examples

### Example 1: Setup Phase
```bash
# Launch all config files in parallel:
Task T004: Create frontend/.env.local.example
Task T005: Create backend/.env.example
Task T006: Create frontend/package.json
Task T007: Create backend/requirements.txt
Task T008: Configure frontend/tsconfig.json
```

### Example 2: User Story 1 Backend
```bash
# Launch all auth endpoints in parallel:
Task T031: POST /api/auth/signup in backend/app/routes/auth.py
Task T032: POST /api/auth/login in backend/app/routes/auth.py
Task T033: POST /api/auth/logout in backend/app/routes/auth.py
```

### Example 3: User Story 2 Components
```bash
# Launch all UI components in parallel:
Task T060: TaskList component in frontend/components/TaskList.tsx
Task T061: TaskItem component in frontend/components/TaskItem.tsx
Task T062: TaskForm component in frontend/components/TaskForm.tsx
Task T063: EmptyState component in frontend/components/EmptyState.tsx
```

---

## Implementation Strategy

### MVP First (User Story 1 + 3 Only)

**Minimum Viable Product**: Authentication + User Isolation (no task management yet)

1. ✅ Complete Phase 1: Setup (T001-T013)
2. ✅ Complete Phase 2: Foundational (T014-T030)
3. ✅ Complete Phase 3: US1 Authentication (T031-T048)
4. ✅ Complete Phase 4: US3 User Isolation framework (T049-T052)
5. **STOP and VALIDATE**: Test signup → login → dashboard → logout flow
6. Deploy/demo authentication system

### MVP + Core Features (US1 + US3 + US2)

**Full Phase 2 Deliverable**: Add task management to authentication MVP

1. ✅ Complete MVP (US1 + US3)
2. ✅ Complete Phase 5: US2 Task Management (T053-T078)
3. **STOP and VALIDATE**: Test full CRUD operations with user isolation
4. Deploy/demo complete Phase 2 application

### Complete Phase 2 (All User Stories)

1. ✅ Complete MVP + Core Features
2. ✅ Complete Phase 6: US4 Persistence validation (T079-T084)
3. ✅ Complete Phase 7: Polish (T085-T105)
4. **FINAL VALIDATION**: Run all acceptance scenarios from spec.md
5. Deploy production-ready application

### Incremental Delivery Timeline

- **Week 1**: Setup + Foundational → Foundation ready for development
- **Week 2**: US1 (Auth) + US3 (Isolation) → MVP deployable (users can signup/login)
- **Week 3**: US2 (Task CRUD) → Full feature complete
- **Week 4**: US4 (Persistence validation) + Polish → Production ready

---

## Task Summary

- **Total Tasks**: 105
- **Setup Phase**: 13 tasks
- **Foundational Phase**: 17 tasks (BLOCKS all user stories)
- **User Story 1 (Authentication)**: 18 tasks
- **User Story 3 (User Isolation)**: 4 tasks
- **User Story 2 (Task Management)**: 26 tasks
- **User Story 4 (Persistence)**: 6 tasks
- **Polish Phase**: 21 tasks

### Tasks by User Story

- **US1 (P1 - Authentication)**: 18 tasks
- **US2 (P2 - Task Management)**: 26 tasks
- **US3 (P1 - User Isolation)**: 4 tasks
- **US4 (P2 - Persistence)**: 6 tasks

### Parallelizable Tasks

- **Setup**: 9 parallel tasks (T004-T012)
- **Foundational**: 6 parallel tasks
- **US1**: 9 parallel tasks
- **US2**: 15 parallel tasks
- **Polish**: 14 parallel tasks

**Total Parallel Opportunities**: ~53 tasks can run concurrently with proper coordination

---

## Notes

- **[P] marker**: Tasks marked [P] operate on different files with no dependencies - can run simultaneously
- **[Story] label**: Maps each task to specific user story for traceability and independent validation
- **Independent Testing**: Each user story phase ends with checkpoint - can validate story independently
- **Foundational Phase Critical**: Phase 2 (T014-T030) MUST complete before any user story work begins
- **Security Priority**: US3 (user isolation) is P1 alongside US1 (auth) - both critical for multi-user security
- **No Tests Included**: Specification did not explicitly request TDD approach - focusing on implementation
- **File Paths**: All tasks include exact file paths for clarity
- **Checkpoint Validation**: Stop at each phase checkpoint to validate independently before proceeding
- **Constitution Compliance**: All tasks align with Phase 2 technology stack (Next.js 16+, FastAPI, SQLModel, Better Auth, Neon PostgreSQL)
