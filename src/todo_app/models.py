# Implemented from Task ID: T-007, T-008, T-009
"""
Data models and custom exceptions for Console Todo Application
Defines Task dataclass and validation exceptions
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single todo task

    Attributes:
        id: Unique task identifier (auto-generated, never reused)
        title: Brief description of the task (1-200 characters)
        description: Optional detailed information (0-1000 characters)
        completed: Whether the task has been marked complete
        created_at: Timestamp when the task was created (immutable)
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    def __str__(self) -> str:
        """Return readable string representation of task"""
        status = "complete" if self.completed else "incomplete"
        return f"Task(id={self.id}, title=\"{self.title}\", status={status})"


class TaskNotFoundError(Exception):
    """
    Raised when an operation references a non-existent task ID

    Attributes:
        task_id: The ID that was not found
    """

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class ValidationError(Exception):
    """
    Raised when user input violates data validation rules

    Attributes:
        message: Specific validation error description
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
