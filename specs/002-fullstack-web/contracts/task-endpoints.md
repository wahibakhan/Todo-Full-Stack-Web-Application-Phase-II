# API Contract: Task Endpoints

**Feature**: Full-Stack Web Todo Application with Authentication
**Date**: 2025-12-29
**Phase**: Phase 1 - Design & Contracts
**Base URL**: `/api/tasks`

## Overview

Task endpoints provide CRUD operations for todo items. **All endpoints require JWT authentication** and automatically filter by the authenticated user's ID to enforce user isolation.

## Common Headers

All requests to task endpoints must include the JWT token cookie:

```
Cookie: auth-token=<JWT>
```

## Common Responses

### 401 Unauthorized (Missing/Invalid Token)

```json
{
  "detail": "Not authenticated"
}
```

## Endpoints

### 1. GET /api/tasks

**Purpose**: List all tasks belonging to the authenticated user

**Authentication**: Required (JWT)

**Request**: No body

**Query Parameters**: None (Phase 2 MVP - no pagination, filtering, or sorting)

**Responses**:

**Success (200 OK)**:

```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": 123,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-12-29T10:05:00Z",
      "updated_at": "2025-12-29T10:05:00Z"
    },
    {
      "id": 2,
      "user_id": 123,
      "title": "Fix bug in app",
      "description": null,
      "completed": true,
      "created_at": "2025-12-29T10:10:00Z",
      "updated_at": "2025-12-29T12:00:00Z"
    }
  ]
}
```

**Success (200 OK) - Empty list**:

```json
{
  "tasks": []
}
```

**Example**:

```bash
curl http://localhost:8000/api/tasks \
  --cookie cookies.txt
```

---

### 2. POST /api/tasks

**Purpose**: Create a new task for the authenticated user

**Authentication**: Required (JWT)

**Request**:

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Request Schema**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | Yes | 1-200 characters | Task title |
| `description` | string | No | 0-1000 characters | Task description (optional) |

**Responses**:

**Success (201 Created)**:

```json
{
  "task": {
    "id": 3,
    "user_id": 123,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-29T14:30:00Z",
    "updated_at": "2025-12-29T14:30:00Z"
  }
}
```

**Error (400 Bad Request)** - Validation failure:

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Error (400 Bad Request)** - Title too long:

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

**Example**:

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}' \
  --cookie cookies.txt
```

---

### 3. PUT /api/tasks/{id}

**Purpose**: Update an existing task (title and/or description)

**Authentication**: Required (JWT)

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Task ID to update |

**Request**:

```json
{
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread, apples"
}
```

**Request Schema**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | No | 1-200 characters | New task title (optional) |
| `description` | string | No | 0-1000 characters | New task description (optional) |

**Notes**:
- At least one field must be provided
- Providing neither field returns 400
- Null description clears the description

**Responses**:

**Success (200 OK)**:

```json
{
  "task": {
    "id": 1,
    "user_id": 123,
    "title": "Buy groceries and fruits",
    "description": "Milk, eggs, bread, apples",
    "completed": false,
    "created_at": "2025-12-29T10:05:00Z",
    "updated_at": "2025-12-29T14:45:00Z"
  }
}
```

**Error (400 Bad Request)** - No fields provided:

```json
{
  "detail": "At least one field (title or description) must be provided"
}
```

**Error (404 Not Found)** - Task doesn't exist or user doesn't own it:

```json
{
  "detail": "Task not found"
}
```

**Notes**:
- 404 is returned for both non-existent tasks and tasks owned by other users
- This prevents revealing the existence of other users' tasks

**Example**:

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and fruits"}' \
  --cookie cookies.txt
```

---

### 4. PATCH /api/tasks/{id}/complete

**Purpose**: Toggle task completion status

**Authentication**: Required (JWT)

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Task ID to toggle |

**Request**: Empty body

**Behavior**:
- If task is incomplete (false) → set to complete (true)
- If task is complete (true) → set to incomplete (false)

**Responses**:

**Success (200 OK)** - Task toggled to complete:

```json
{
  "task": {
    "id": 1,
    "user_id": 123,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2025-12-29T10:05:00Z",
    "updated_at": "2025-12-29T15:00:00Z"
  }
}
```

**Error (404 Not Found)** - Task doesn't exist or user doesn't own it:

```json
{
  "detail": "Task not found"
}
```

**Example**:

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  --cookie cookies.txt
```

---

### 5. DELETE /api/tasks/{id}

**Purpose**: Delete a task

**Authentication**: Required (JWT)

**URL Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Task ID to delete |

**Request**: Empty body

**Responses**:

**Success (204 No Content)**: Empty response body

**Error (404 Not Found)** - Task doesn't exist or user doesn't own it:

```json
{
  "detail": "Task not found"
}
```

**Example**:

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  --cookie cookies.txt
```

---

## User Isolation Enforcement

**CRITICAL**: All task endpoints MUST filter by authenticated user_id to prevent cross-user data access.

### Backend Implementation Pattern

```python
from fastapi import Depends
from sqlmodel import Session, select

@router.get("/tasks")
def list_tasks(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user) # Extracts user_id from JWT
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
    # Query MUST filter by BOTH task_id AND user_id
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id # CRITICAL: prevents cross-user access
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task...
```

### Security Test Scenarios

1. **User A cannot list User B's tasks**:
   - User A logs in → GET /api/tasks → Only User A's tasks returned
   - User B logs in → GET /api/tasks → Only User B's tasks returned

2. **User A cannot update User B's task**:
   - User B creates task (ID 5)
   - User A attempts PUT /api/tasks/5 → 404 Not Found

3. **User A cannot delete User B's task**:
   - User B creates task (ID 5)
   - User A attempts DELETE /api/tasks/5 → 404 Not Found

4. **User A cannot toggle User B's task**:
   - User B creates task (ID 5)
   - User A attempts PATCH /api/tasks/5/complete → 404 Not Found

## Error Response Patterns

### 400 Bad Request (Validation Errors)

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

### 401 Unauthorized (Missing/Invalid JWT)

```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found (Task Not Found or Not Owned)

```json
{
  "detail": "Task not found"
}
```

**Note**: Same 404 response for both scenarios (security by obscurity)

## Frontend API Client Pattern

```typescript
// lib/api.ts
export async function getTasks(): Promise<Task[]> {
  const response = await apiClient("/api/tasks", {
    method: "GET"
  })
  const data = await response.json()
  return data.tasks
}

export async function createTask(
  taskData: { title: string; description?: string }
): Promise<Task> {
  const response = await apiClient("/api/tasks", {
    method: "POST",
    body: JSON.stringify(taskData)
  })
  const data = await response.json()
  return data.task
}

export async function updateTask(
  taskId: number,
  updates: { title?: string; description?: string }
): Promise<Task> {
  const response = await apiClient(`/api/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(updates)
  })
  const data = await response.json()
  return data.task
}

export async function toggleTaskComplete(taskId: number): Promise<Task> {
  const response = await apiClient(`/api/tasks/${taskId}/complete`, {
    method: "PATCH"
  })
  const data = await response.json()
  return data.task
}

export async function deleteTask(taskId: number): Promise<void> {
  await apiClient(`/api/tasks/${taskId}`, {
    method: "DELETE"
  })
}
```

## Testing Checklist

- [ ] GET /api/tasks returns only authenticated user's tasks
- [ ] GET /api/tasks returns empty array if user has no tasks
- [ ] POST /api/tasks creates task with correct user_id from JWT
- [ ] POST /api/tasks requires title (400 if missing)
- [ ] POST /api/tasks validates title length (400 if >200 chars)
- [ ] POST /api/tasks validates description length (400 if >1000 chars)
- [ ] PUT /api/tasks/{id} updates task if user owns it
- [ ] PUT /api/tasks/{id} returns 404 if task owned by other user
- [ ] PUT /api/tasks/{id} returns 404 if task doesn't exist
- [ ] PATCH /api/tasks/{id}/complete toggles completion status
- [ ] PATCH /api/tasks/{id}/complete returns 404 for other user's task
- [ ] DELETE /api/tasks/{id} deletes task if user owns it
- [ ] DELETE /api/tasks/{id} returns 404 for other user's task
- [ ] All endpoints return 401 without valid JWT
- [ ] User A cannot access User B's tasks (isolation test)

---

**Task Endpoints Contracts**: ✅ **COMPLETE**
**Next Artifact**: Quickstart Guide (quickstart.md)
