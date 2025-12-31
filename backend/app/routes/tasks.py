"""
Task routes: CRUD operations for todo items.
All endpoints require JWT authentication and filter by user_id.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models.task import Task
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskListResponse,
    TaskSingleResponse,
    TaskResponse,
)
from app.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=TaskListResponse)
def list_tasks(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    """
    List all tasks belonging to the authenticated user.

    Returns:
        TaskListResponse: List of tasks filtered by user_id

    Security:
        - Requires valid JWT token
        - Only returns tasks owned by authenticated user
    """
    # CRITICAL: Filter by user_id from JWT
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    return TaskListResponse(tasks=[TaskResponse.from_orm(task) for task in tasks])


@router.post("", response_model=TaskSingleResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Title and optional description

    Returns:
        TaskSingleResponse: Created task

    Security:
        - Requires valid JWT token
        - Automatically assigns user_id from JWT (user cannot spoof this)
    """
    # Create task with user_id from JWT (NOT from request body)
    new_task = Task(
        user_id=user_id,  # CRITICAL: Use user_id from JWT, not user input
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return TaskSingleResponse(task=TaskResponse.from_orm(new_task))


@router.put("/{task_id}", response_model=TaskSingleResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    """
    Update an existing task (title and/or description).

    Args:
        task_id: ID of task to update
        task_data: New title and/or description

    Returns:
        TaskSingleResponse: Updated task

    Raises:
        400 Bad Request: No fields provided
        404 Not Found: Task doesn't exist or user doesn't own it

    Security:
        - Requires valid JWT token
        - Filters by BOTH task_id AND user_id (prevents cross-user access)
    """
    # Validate at least one field provided
    if task_data.title is None and task_data.description is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (title or description) must be provided"
        )

    # CRITICAL: Filter by BOTH task_id AND user_id
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # Prevents User A from updating User B's task
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"  # Same message for non-existent and not-owned
        )

    # Update fields
    if task_data.title is not None:
        task.title = task_data.title.strip()

    if task_data.description is not None:
        task.description = task_data.description.strip() if task_data.description else None

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskSingleResponse(task=TaskResponse.from_orm(task))


@router.patch("/{task_id}/complete", response_model=TaskSingleResponse)
def toggle_task_complete(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    """
    Toggle task completion status.

    Args:
        task_id: ID of task to toggle

    Returns:
        TaskSingleResponse: Task with toggled completion status

    Raises:
        404 Not Found: Task doesn't exist or user doesn't own it

    Security:
        - Requires valid JWT token
        - Filters by BOTH task_id AND user_id
    """
    # CRITICAL: Filter by BOTH task_id AND user_id
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskSingleResponse(task=TaskResponse.from_orm(task))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
):
    """
    Delete a task.

    Args:
        task_id: ID of task to delete

    Returns:
        204 No Content on success

    Raises:
        404 Not Found: Task doesn't exist or user doesn't own it

    Security:
        - Requires valid JWT token
        - Filters by BOTH task_id AND user_id
    """
    # CRITICAL: Filter by BOTH task_id AND user_id
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    # No content returned for 204
    return None
