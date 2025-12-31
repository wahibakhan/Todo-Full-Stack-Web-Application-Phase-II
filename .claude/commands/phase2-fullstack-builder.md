---
description: Transform console Todo app into secure multi-user full-stack web application using Next.js + FastAPI + Better Auth + Neon DB
handoffs:
  - label: Review Implementation
    agent: sp.implement
    prompt: Review and validate the Phase 2 implementation
  - label: Run Tests
    agent: sp.implement
    prompt: Run all tests for Phase 2 implementation
  - label: Create PR
    agent: sp.git.commit_pr
    prompt: Commit Phase 2 changes and create pull request
---

## User Input

```text
$ARGUMENTS
```

**Parameters**:
- `project_name`: Name of the project (default: hackathon-todo)
- `auth_secret`: Shared BETTER_AUTH_SECRET value (used in both frontend and backend)
- `database_url`: Neon PostgreSQL connection string

**Example**:
```
/phase2-fullstack-builder project_name="hackathon-todo" auth_secret="your-super-secret-key-min-32-chars" database_url="postgresql://user:pass@neon-host/db"
```

## Overview

You are a **Senior Full-Stack Engineer** implementing Phase 2 of Panaversity Hackathon II - transforming the Phase 1 console Todo application into a production-ready, secure, multi-user web application.

**Phase 2 Goals**:
- ✅ Multi-user authentication with Better Auth
- ✅ Full-stack web application (Next.js + FastAPI)
- ✅ Persistent database storage (Neon PostgreSQL)
- ✅ Secure REST API with JWT authentication
- ✅ User-specific data isolation
- ✅ Responsive modern UI with Tailwind CSS

## Professional Standards

**CRITICAL**: Follow strict Spec-Driven Development methodology:

1. **Specs First** - Update `/specs` folder BEFORE implementation
2. **Incremental Progress** - Implement one component at a time
3. **Clear Reporting** - Report progress after each component
4. **Type Safety** - TypeScript (frontend) + Pydantic/SQLModel (backend)
5. **Security First** - JWT validation, user data isolation, environment secrets
6. **Production Ready** - Error handling, validation, logging

## Implementation Workflow

### Phase 0: Specifications (MANDATORY FIRST STEP)

**Create/Update these specification files**:

1. **`specs/002-phase2-fullstack/spec.md`**
   - User stories for authentication, web UI, multi-user CRUD
   - Functional requirements (login, signup, JWT, user-filtered tasks)
   - Success criteria (response times, security, UX)
   - Out of scope items

2. **`specs/002-phase2-fullstack/features/authentication.md`**
   - Better Auth configuration
   - JWT token structure (payload, expiry)
   - Login/signup flows
   - Session management

3. **`specs/002-phase2-fullstack/api/rest-endpoints.md`**
   - `POST /auth/login` - Credentials → JWT
   - `POST /auth/signup` - User registration
   - `GET /tasks` - List user's tasks (JWT protected)
   - `POST /tasks` - Create task (JWT protected)
   - `PUT /tasks/{id}` - Update task (JWT protected, ownership check)
   - `DELETE /tasks/{id}` - Delete task (JWT protected, ownership check)
   - `PATCH /tasks/{id}/toggle` - Toggle completion

4. **`specs/002-phase2-fullstack/database/schema.md`**
   - Users table (id, email, password_hash, created_at)
   - Tasks table (id, user_id FK, title, description, completed, created_at)
   - Indexes and constraints

5. **`specs/002-phase2-fullstack/ui/pages.md`**
   - `/login` - Login page
   - `/signup` - Signup page
   - `/dashboard` - Todo dashboard (protected)

6. **`specs/002-phase2-fullstack/ui/components.md`**
   - LoginForm, SignupForm, TaskList, TaskItem, AddTaskForm
   - Component props and behavior

**Wait for user approval of specs before proceeding to implementation.**

---

### Phase 1: Project Structure

**Create monorepo structure**:

```
todo_app/
├── frontend/               # Next.js 15+ (App Router)
│   ├── app/
│   │   ├── login/
│   │   ├── signup/
│   │   ├── dashboard/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── auth/
│   │   └── tasks/
│   ├── lib/
│   │   ├── auth.ts         # Better Auth config
│   │   └── api.ts          # API client
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── .env.local
│
├── backend/                # FastAPI + SQLModel
│   ├── app/
│   │   ├── main.py         # FastAPI app
│   │   ├── models.py       # SQLModel models
│   │   ├── database.py     # DB connection
│   │   ├── auth.py         # JWT middleware
│   │   └── routers/
│   │       ├── auth.py     # Login/signup routes
│   │       └── tasks.py    # CRUD routes
│   ├── requirements.txt
│   └── .env
│
└── src/                    # Phase 1 console app (preserved)
```

**Report**: "Project structure created. Frontend: Next.js. Backend: FastAPI."

---

### Phase 2: Backend Implementation

#### 2.1: Database Models (SQLModel)

**File**: `backend/app/models.py`

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

**Report**: "Database models created with user-task relationship."

#### 2.2: Database Connection

**File**: `backend/app/database.py`

```python
from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

**Report**: "Database connection configured with Neon PostgreSQL."

#### 2.3: JWT Authentication Middleware

**File**: `backend/app/auth.py`

```python
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from datetime import datetime, timedelta

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

security = HTTPBearer()

def create_jwt_token(user_id: int, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Report**: "JWT authentication middleware implemented with shared secret."

#### 2.4: Auth Routes (Login/Signup)

**File**: `backend/app/routers/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from ..database import get_session
from ..models import User
from ..auth import create_jwt_token

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(data: SignupRequest, session: Session = Depends(get_session)):
    # Check if user exists
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    password_hash = bcrypt.hash(data.password)
    user = User(email=data.email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Return JWT
    token = create_jwt_token(user.id, user.email)
    return {"token": token, "user": {"id": user.id, "email": user.email}}

@router.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    # Find user
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return JWT
    token = create_jwt_token(user.id, user.email)
    return {"token": token, "user": {"id": user.id, "email": user.email}}
```

**Report**: "Auth routes implemented with password hashing and JWT issuance."

#### 2.5: Task CRUD Routes (User-Filtered)

**File**: `backend/app/routers/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from ..database import get_session
from ..models import Task
from ..auth import verify_jwt_token

router = APIRouter(prefix="/tasks", tags=["tasks"])

class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""

class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None

@router.get("")
def get_tasks(session: Session = Depends(get_session), current_user: dict = Depends(verify_jwt_token)):
    user_id = current_user["user_id"]
    tasks = session.exec(select(Task).where(Task.user_id == user_id).order_by(Task.id)).all()
    return tasks

@router.post("")
def create_task(data: CreateTaskRequest, session: Session = Depends(get_session), current_user: dict = Depends(verify_jwt_token)):
    user_id = current_user["user_id"]
    task = Task(user_id=user_id, title=data.title, description=data.description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.put("/{task_id}")
def update_task(task_id: int, data: UpdateTaskRequest, session: Session = Depends(get_session), current_user: dict = Depends(verify_jwt_token)):
    user_id = current_user["user_id"]
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description

    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session), current_user: dict = Depends(verify_jwt_token)):
    user_id = current_user["user_id"]
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}

@router.patch("/{task_id}/toggle")
def toggle_task(task_id: int, session: Session = Depends(get_session), current_user: dict = Depends(verify_jwt_token)):
    user_id = current_user["user_id"]
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    session.commit()
    session.refresh(task)
    return task
```

**Report**: "Task CRUD routes implemented with user ownership verification."

#### 2.6: FastAPI Main App

**File**: `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from .routers import auth, tasks

app = FastAPI(title="Hackathon Todo API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hackathon Todo API - Phase 2"}
```

**Report**: "FastAPI app configured with CORS and route registration."

---

### Phase 3: Frontend Implementation

#### 3.1: Better Auth Configuration

**File**: `frontend/lib/auth.ts`

```typescript
import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  database: {
    // Using backend API for auth
    type: "custom"
  },
  plugins: [nextCookies()]
})

export type Session = typeof auth.$Infer.Session
```

**Report**: "Better Auth configured with shared secret."

#### 3.2: API Client

**File**: `frontend/lib/api.ts`

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function apiCall(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem("token")

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "API request failed")
  }

  return response.json()
}

export const api = {
  // Auth
  signup: (email: string, password: string) =>
    apiCall("/auth/signup", { method: "POST", body: JSON.stringify({ email, password }) }),

  login: (email: string, password: string) =>
    apiCall("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),

  // Tasks
  getTasks: () => apiCall("/tasks"),
  createTask: (title: string, description: string) =>
    apiCall("/tasks", { method: "POST", body: JSON.stringify({ title, description }) }),
  updateTask: (id: number, title?: string, description?: string) =>
    apiCall(`/tasks/${id}`, { method: "PUT", body: JSON.stringify({ title, description }) }),
  deleteTask: (id: number) =>
    apiCall(`/tasks/${id}`, { method: "DELETE" }),
  toggleTask: (id: number) =>
    apiCall(`/tasks/${id}/toggle`, { method: "PATCH" })
}
```

**Report**: "API client created with JWT token management."

#### 3.3: Login Page

**File**: `frontend/app/login/page.tsx`

```typescript
"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const data = await api.login(email, password)
      localStorage.setItem("token", data.token)
      router.push("/dashboard")
    } catch (err: any) {
      setError(err.message)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6">Login</h1>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded mb-4"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded mb-4"
            required
          />
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
            Login
          </button>
        </form>
        <p className="mt-4 text-center">
          Don't have an account? <a href="/signup" className="text-blue-500">Sign up</a>
        </p>
      </div>
    </div>
  )
}
```

**Report**: "Login page created with form validation and error handling."

#### 3.4: Dashboard Page

**File**: `frontend/app/dashboard/page.tsx`

```typescript
"use client"
import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { useRouter } from "next/navigation"

type Task = {
  id: number
  title: string
  description: string
  completed: boolean
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const router = useRouter()

  useEffect(() => {
    loadTasks()
  }, [])

  const loadTasks = async () => {
    try {
      const data = await api.getTasks()
      setTasks(data)
    } catch {
      router.push("/login")
    }
  }

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.createTask(title, description)
    setTitle("")
    setDescription("")
    loadTasks()
  }

  const handleToggle = async (id: number) => {
    await api.toggleTask(id)
    loadTasks()
  }

  const handleDelete = async (id: number) => {
    await api.deleteTask(id)
    loadTasks()
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-8">My Tasks</h1>

      <form onSubmit={handleAddTask} className="bg-white p-6 rounded-lg shadow mb-8">
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full p-2 border rounded mb-4"
          required
        />
        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-2 border rounded mb-4"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Add Task
        </button>
      </form>

      <div className="space-y-4">
        {tasks.map(task => (
          <div key={task.id} className="bg-white p-4 rounded-lg shadow flex justify-between items-center">
            <div>
              <h3 className={`font-bold ${task.completed ? 'line-through text-gray-500' : ''}`}>
                {task.title}
              </h3>
              <p className="text-gray-600">{task.description}</p>
            </div>
            <div className="flex gap-2">
              <button onClick={() => handleToggle(task.id)} className="bg-green-500 text-white px-3 py-1 rounded">
                {task.completed ? 'Undo' : 'Complete'}
              </button>
              <button onClick={() => handleDelete(task.id)} className="bg-red-500 text-white px-3 py-1 rounded">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Report**: "Dashboard page created with task CRUD operations."

---

### Phase 4: Environment Configuration

#### Backend `.env`

```bash
DATABASE_URL=postgresql://user:password@neon-host/db
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars
```

#### Frontend `.env.local`

```bash
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Report**: "Environment configuration created with shared secret."

---

### Phase 5: Dependencies

#### Backend `requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic[email]==2.5.0
```

#### Frontend `package.json`

```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "better-auth": "^1.0.0",
    "tailwindcss": "^3.4.0"
  }
}
```

**Report**: "Dependencies specified for both frontend and backend."

---

## Progress Reporting

After each phase, report:

```
✅ Phase X Complete: [Component Name]
- Files created: [list]
- Features implemented: [list]
- Next step: [description]
```

## Final Deliverables

1. ✅ Complete monorepo structure
2. ✅ Updated Phase 2 specifications
3. ✅ Working authentication system
4. ✅ Secure REST API with JWT
5. ✅ User-filtered task management
6. ✅ Responsive Next.js dashboard
7. ✅ Environment setup instructions
8. ✅ README with run/deploy steps

## Success Criteria

- [ ] User can sign up and log in
- [ ] JWT tokens are validated on all protected routes
- [ ] Tasks are filtered by user_id (data isolation)
- [ ] All CRUD operations work via web UI
- [ ] Frontend is responsive (mobile + desktop)
- [ ] No data leakage between users
- [ ] Environment variables properly configured
- [ ] Clear documentation for local setup

---

**Remember**: Spec-Driven Development is mandatory. Update specs first, implement incrementally, report progress clearly.
