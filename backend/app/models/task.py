"""
Task model for todo items.
Each task belongs to a specific user (user_id foreign key).
"""
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """
    Task model representing a todo item owned by a user.

    Fields:
        id: Auto-incrementing primary key
        user_id: Foreign key to users.id (CRITICAL for user isolation)
        title: Task title (required, 1-200 characters)
        description: Task description (optional, max 1000 characters)
        completed: Completion status (default: False)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp

    Foreign Key Constraint:
        ON DELETE CASCADE - Deleting a user deletes all their tasks
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id",
        nullable=False,
        index=True  # CRITICAL: Index for performance on user_id queries
    )
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        """SQLModel configuration"""
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
