"""
Pydantic schemas for task requests and responses.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Request schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }


class TaskUpdate(BaseModel):
    """Request schema for updating an existing task."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="New task title (optional)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="New task description (optional)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and fruits",
                "description": "Milk, eggs, bread, apples"
            }
        }


class TaskResponse(BaseModel):
    """Response schema for a single task."""

    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow SQLModel to Pydantic conversion
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2025-12-29T10:05:00Z",
                "updated_at": "2025-12-29T10:05:00Z"
            }
        }


class TaskListResponse(BaseModel):
    """Response schema for list of tasks."""

    tasks: list[TaskResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "user_id": 123,
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "completed": False,
                        "created_at": "2025-12-29T10:05:00Z",
                        "updated_at": "2025-12-29T10:05:00Z"
                    },
                    {
                        "id": 2,
                        "user_id": 123,
                        "title": "Fix bug in app",
                        "description": None,
                        "completed": True,
                        "created_at": "2025-12-29T10:10:00Z",
                        "updated_at": "2025-12-29T12:00:00Z"
                    }
                ]
            }
        }


class TaskSingleResponse(BaseModel):
    """Response schema for single task operations (create, update, toggle)."""

    task: TaskResponse

    class Config:
        json_schema_extra = {
            "example": {
                "task": {
                    "id": 1,
                    "user_id": 123,
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "completed": False,
                    "created_at": "2025-12-29T10:05:00Z",
                    "updated_at": "2025-12-29T10:05:00Z"
                }
            }
        }
