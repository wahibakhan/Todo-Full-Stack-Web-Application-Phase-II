# Quickstart Guide: Phase 2 Local Development

**Feature**: Full-Stack Web Todo Application with Authentication
**Date**: 2025-12-29
**Phase**: Phase 1 - Design & Contracts

## Overview

This guide provides step-by-step instructions for setting up and running the Phase 2 full-stack web application locally. You'll have both the Next.js frontend and FastAPI backend running simultaneously.

## Prerequisites

### Required Software

| Software | Version | Download Link |
|----------|---------|---------------|
| **Node.js** | 20.x or later | https://nodejs.org/ |
| **npm** | 10.x or later | Included with Node.js |
| **Python** | 3.13 or later | https://python.org/ |
| **pip** | Latest | Included with Python |
| **Git** | Latest | https://git-scm.com/ |

### Cloud Services

| Service | Purpose | Signup Link |
|---------|---------|-------------|
| **Neon PostgreSQL** | Database hosting | https://neon.tech/ (Free tier available) |

### Verify Installations

```bash
# Check Node.js version
node --version
# Expected: v20.x.x or higher

# Check npm version
npm --version
# Expected: 10.x.x or higher

# Check Python version
python --version
# Expected: Python 3.13.x or higher

# Check pip version
pip --version
# Expected: pip 24.x or higher
```

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd todo_app
git checkout 002-fullstack-web
```

## Step 2: Create Neon PostgreSQL Database

### 2.1. Sign Up for Neon

1. Visit https://neon.tech/
2. Click "Sign Up" (free tier available)
3. Create account with email or GitHub

### 2.2. Create New Project

1. Click "New Project"
2. Project name: `todo-app-phase2`
3. Region: Choose closest to your location
4. PostgreSQL version: 15 or later
5. Click "Create Project"

### 2.3. Get Connection String

1. In project dashboard, click "Connection Details"
2. Copy the **Pooler** connection string (recommended for serverless):

   ```
   postgresql://user:password@ep-xxx-pooler.neon.tech/dbname?sslmode=require
   ```

3. Save this for environment variable setup

**Note**: Use the **pooler** URL (ends with `-pooler.neon.tech`) for better performance with SQLModel.

## Step 3: Generate Shared Secret

Generate a secure random secret for JWT token signing (shared between frontend and backend):

```bash
# On Linux/Mac
openssl rand -base64 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32|ForEach-Object{Get-Random -Minimum 0 -Maximum 256}))

# Example output:
# 8Zq3t6w9z$C&F)J@NcRfUjXn2r5u7x!A%D*G-KaPd
```

Save this secret - you'll use it in both frontend and backend `.env` files.

## Step 4: Frontend Setup

### 4.1. Navigate to Frontend Directory

```bash
cd frontend
```

### 4.2. Install Dependencies

```bash
npm install
```

Expected dependencies:
- next (16.x)
- react (19.x)
- better-auth
- tailwindcss (3.x)
- typescript (5.x)

### 4.3. Create Environment File

Create `frontend/.env.local`:

```bash
# Copy example
cp .env.local.example .env.local

# Or create manually
touch .env.local
```

Add the following content to `.env.local`:

```env
# Better Auth - JWT Secret (MUST match backend)
BETTER_AUTH_SECRET=your-secret-from-step-3

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database URL (same as backend - Better Auth needs it)
DATABASE_URL=your-neon-connection-string-from-step-2
```

**IMPORTANT**:
- Replace `your-secret-from-step-3` with the generated secret
- Replace `your-neon-connection-string-from-step-2` with your Neon pooler URL
- `BETTER_AUTH_SECRET` MUST be identical in frontend and backend

### 4.4. Run Frontend

```bash
npm run dev
```

Expected output:
```
   ▲ Next.js 16.0.0
   - Local:        http://localhost:3000
   - Ready in 2.1s
```

**Frontend is now running at http://localhost:3000**

Keep this terminal open and proceed to backend setup in a new terminal.

## Step 5: Backend Setup

### 5.1. Navigate to Backend Directory

Open a **new terminal window** and:

```bash
cd todo_app/backend
```

### 5.2. Create Virtual Environment (Recommended)

```bash
# On Linux/Mac
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

Your prompt should show `(venv)` prefix.

### 5.3. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected dependencies:
- fastapi (0.104+)
- uvicorn (0.24+)
- sqlmodel (0.0.14+)
- python-jose (3.3+)
- passlib (1.7+)
- python-multipart
- psycopg2-binary (for PostgreSQL)

### 5.4. Create Environment File

Create `backend/.env`:

```bash
# Copy example
cp .env.example .env

# Or create manually
touch .env
```

Add the following content to `.env`:

```env
# Better Auth - JWT Secret (MUST match frontend)
BETTER_AUTH_SECRET=your-secret-from-step-3

# Neon PostgreSQL Connection
DATABASE_URL=your-neon-connection-string-from-step-2

# Environment
ENVIRONMENT=development
```

**IMPORTANT**:
- Replace values with same secret and database URL as frontend
- `BETTER_AUTH_SECRET` MUST be identical in both frontend and backend

### 5.5. Run Database Migrations (Optional)

If using Alembic:

```bash
alembic upgrade head
```

If using SQLModel auto-creation (recommended for Phase 2):

Tables will be created automatically on first run (see Step 5.6).

### 5.6. Run Backend

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

**Backend is now running at http://localhost:8000**

### 5.7. Verify Backend

Open http://localhost:8000/docs in your browser to see the auto-generated API documentation (FastAPI Swagger UI).

You should see endpoints:
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/tasks
- POST /api/tasks
- PUT /api/tasks/{id}
- PATCH /api/tasks/{id}/complete
- DELETE /api/tasks/{id}

## Step 6: Verify Full Stack

### 6.1. Access Frontend

Visit http://localhost:3000 in your browser.

You should see:
- Landing page with login/signup options
- OR automatic redirect to login page

### 6.2. Create Test Account

1. Click "Sign Up" (or navigate to http://localhost:3000/signup)
2. Enter email: `test@example.com`
3. Enter password: `TestPass123`
4. Click "Sign Up"

Expected result:
- Account created
- Redirected to dashboard at http://localhost:3000/dashboard

### 6.3. Test Task Management

In the dashboard:

1. **Add Task**:
   - Enter title: "Buy groceries"
   - Enter description: "Milk, eggs, bread"
   - Click "Add"
   - Task should appear in list

2. **Toggle Completion**:
   - Click checkbox next to task
   - Status should change from [ ] to [x]

3. **Edit Task**:
   - Click "Edit" button
   - Change title to "Buy groceries and fruits"
   - Click "Save"
   - Updated title should display

4. **Delete Task**:
   - Click "Delete" button
   - Confirm deletion
   - Task should disappear from list

### 6.4. Test User Isolation

1. **Logout**:
   - Click "Logout" button
   - Redirected to login page

2. **Create Second Account**:
   - Click "Sign Up"
   - Email: `test2@example.com`
   - Password: `TestPass456`
   - Sign up

3. **Verify Isolation**:
   - New user should see empty task list
   - Tasks from first user (`test@example.com`) should NOT be visible

4. **Login as First User**:
   - Logout
   - Login with `test@example.com`
   - Original tasks should still be visible

## Common Issues & Solutions

### Issue 1: "Module not found" (Frontend)

**Error**:
```
Module not found: Can't resolve 'better-auth'
```

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue 2: "Connection refused" (Backend cannot reach database)

**Error**:
```
sqlalchemy.exc.OperationalError: connection refused
```

**Solution**:
1. Verify `DATABASE_URL` in `backend/.env` is correct
2. Check Neon project is active (not paused)
3. Ensure using **pooler** URL (ends with `-pooler.neon.tech`)
4. Check internet connection (Neon is cloud-hosted)

### Issue 3: "Invalid token" (JWT verification failing)

**Error**:
Frontend shows "Session expired" or backend returns 401.

**Solution**:
1. Verify `BETTER_AUTH_SECRET` is **identical** in both `.env` files
2. Check for extra spaces or newlines in secret
3. Restart both frontend and backend servers

### Issue 4: "Port already in use"

**Error**:
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution**:

Frontend (port 3000):
```bash
# Find process using port 3000
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process or use different port
PORT=3001 npm run dev
```

Backend (port 8000):
```bash
# Use different port
uvicorn app.main:app --reload --port 8001

# Update frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Issue 5: CORS Errors

**Error**:
```
Access to fetch at 'http://localhost:8000/api/tasks' blocked by CORS policy
```

**Solution**:
Ensure backend has CORS middleware configured in `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

## Running Tests

### Frontend Tests

```bash
cd frontend
npm test              # Run all tests
npm run test:watch    # Watch mode
npm run test:coverage # With coverage report
```

### Backend Tests

```bash
cd backend
pytest                     # Run all tests
pytest -v                  # Verbose output
pytest --cov=app          # With coverage
pytest tests/test_auth.py  # Specific test file
```

### E2E Tests (Playwright)

```bash
cd frontend
npx playwright test              # Run E2E tests
npx playwright test --ui         # Interactive mode
npx playwright test --debug      # Debug mode
```

## Environment Variables Reference

### Frontend (.env.local)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `BETTER_AUTH_SECRET` | ✅ Yes | `8Zq3t6w...` | JWT signing secret (matches backend) |
| `NEXT_PUBLIC_API_URL` | ✅ Yes | `http://localhost:8000` | Backend API URL |
| `DATABASE_URL` | ✅ Yes | `postgresql://...` | Neon PostgreSQL connection (for Better Auth) |

### Backend (.env)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `BETTER_AUTH_SECRET` | ✅ Yes | `8Zq3t6w...` | JWT signing secret (matches frontend) |
| `DATABASE_URL` | ✅ Yes | `postgresql://...` | Neon PostgreSQL connection |
| `ENVIRONMENT` | No | `development` | Environment name (development/production) |

## Next Steps

After local development environment is working:

1. ✅ Run `/sp.tasks` to generate atomic implementation tasks
2. ✅ Follow TDD workflow: Write tests → Implement → Verify
3. ✅ Implement authentication (signup, login, logout)
4. ✅ Implement task CRUD operations
5. ✅ Verify user isolation security
6. ✅ Achieve 80%+ test coverage

---

**Quickstart Guide**: ✅ **COMPLETE**
**Local Environment**: ✅ **READY**
**Next Command**: `/sp.tasks`
