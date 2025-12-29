# Implemented from Task ID: T-023, T-024, T-039, T-040, T-046, T-052
"""
In-memory task storage with CRUD operations
Manages the collection of tasks and provides data validation
"""

from datetime import datetime
from typing import Optional
from src.todo_app.models import Task, TaskNotFoundError, ValidationError


class TaskStorage:
    """
    Manages in-memory collection of tasks with CRUD operations

    Attributes:
        _tasks: Dictionary mapping task IDs to Task instances
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize empty task storage"""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create and add a new task to storage

        Args:
            title: Task title (1-200 characters, required)
            description: Task description (0-1000 characters, optional)

        Returns:
            The newly created Task instance

        Raises:
            ValidationError: If title is empty or exceeds 200 characters
            ValidationError: If description exceeds 1000 characters
        """
        # Strip whitespace from title
        title = title.strip()

        # Validate title
        if not title:
            raise ValidationError("Title cannot be empty")
        if len(title) > 200:
            raise ValidationError("Title exceeds maximum length of 200 characters")

        # Validate description
        if len(description) > 1000:
            raise ValidationError("Description exceeds maximum length of 1000 characters")

        # Create task with auto-generated ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now()
        )

        # Add to storage and increment ID counter
        self._tasks[task.id] = task
        self._next_id += 1

        return task

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks in storage, ordered by ID

        Returns:
            List of Task instances, sorted by ID (creation order)
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve a specific task by its ID

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task instance with the specified ID

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id=task_id)

        return self._tasks[task_id]

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update title and/or description of an existing task

        Args:
            task_id: ID of the task to update
            title: New title (or None to keep current), 1-200 characters
            description: New description (or None to keep current), 0-1000 characters

        Returns:
            The updated Task instance

        Raises:
            TaskNotFoundError: If no task exists with the given ID
            ValidationError: If provided title/description violates constraints
        """
        # Get existing task
        task = self.get_task_by_id(task_id)

        # Update title if provided
        if title is not None:
            title = title.strip()
            if not title:
                raise ValidationError("Title cannot be empty")
            if len(title) > 200:
                raise ValidationError("Title exceeds maximum length of 200 characters")
            task.title = title

        # Update description if provided
        if description is not None:
            if len(description) > 1000:
                raise ValidationError("Description exceeds maximum length of 1000 characters")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> Task:
        """
        Permanently remove a task from storage

        Args:
            task_id: ID of the task to delete

        Returns:
            The deleted Task instance (for confirmation display)

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        # Get task to verify it exists
        task = self.get_task_by_id(task_id)

        # Remove from storage (ID will not be reused)
        del self._tasks[task_id]

        return task

    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggle the completion status of a task

        Args:
            task_id: ID of the task to toggle

        Returns:
            The task with updated completion status

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self.get_task_by_id(task_id)
        task.completed = not task.completed
        return task
