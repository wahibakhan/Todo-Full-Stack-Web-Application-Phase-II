# Implemented from Task ID: T-005, T-006
"""
Unit tests for Task dataclass and custom exceptions
TDD: These tests are written FIRST and should FAIL until implementation
"""

from datetime import datetime
import pytest
from src.todo_app.models import Task, TaskNotFoundError, ValidationError


class TestTaskDataclass:
    """Test Task dataclass structure and behavior"""

    def test_task_creation_with_all_fields(self) -> None:
        """Test creating a task with all fields populated"""
        created_time = datetime.now()
        task = Task(
            id=1,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False,
            created_at=created_time
        )

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.completed is False
        assert task.created_at == created_time

    def test_task_creation_minimal_fields(self) -> None:
        """Test creating a task with minimal required fields"""
        created_time = datetime.now()
        task = Task(
            id=2,
            title="Complete homework",
            description="",
            completed=False,
            created_at=created_time
        )

        assert task.id == 2
        assert task.title == "Complete homework"
        assert task.description == ""
        assert task.completed is False

    def test_task_field_types(self) -> None:
        """Test that task fields have correct types"""
        task = Task(
            id=1,
            title="Test",
            description="Description",
            completed=True,
            created_at=datetime.now()
        )

        assert isinstance(task.id, int)
        assert isinstance(task.title, str)
        assert isinstance(task.description, str)
        assert isinstance(task.completed, bool)
        assert isinstance(task.created_at, datetime)

    def test_task_string_representation(self) -> None:
        """Test Task __str__ method produces readable output"""
        task = Task(
            id=5,
            title="Test Task",
            description="Test description",
            completed=False,
            created_at=datetime.now()
        )

        task_str = str(task)
        assert "5" in task_str
        assert "Test Task" in task_str
        assert "False" in task_str or "incomplete" in task_str.lower()

    def test_task_completed_toggle(self) -> None:
        """Test that completed status can be toggled"""
        task = Task(
            id=1,
            title="Test",
            description="",
            completed=False,
            created_at=datetime.now()
        )

        # Initially incomplete
        assert task.completed is False

        # Simulate toggle (will be done by storage layer)
        task.completed = True
        assert task.completed is True


class TestCustomExceptions:
    """Test custom exception classes"""

    def test_task_not_found_error_creation(self) -> None:
        """Test TaskNotFoundError can be created with task_id"""
        error = TaskNotFoundError(task_id=42)
        assert error.task_id == 42
        assert "42" in str(error)

    def test_task_not_found_error_message(self) -> None:
        """Test TaskNotFoundError has descriptive message"""
        error = TaskNotFoundError(task_id=10)
        error_msg = str(error)
        assert "10" in error_msg
        assert "not found" in error_msg.lower()

    def test_task_not_found_error_is_exception(self) -> None:
        """Test TaskNotFoundError inherits from Exception"""
        error = TaskNotFoundError(task_id=1)
        assert isinstance(error, Exception)

    def test_validation_error_creation(self) -> None:
        """Test ValidationError can be created with message"""
        error = ValidationError(message="Title cannot be empty")
        assert error.message == "Title cannot be empty"
        assert "Title cannot be empty" in str(error)

    def test_validation_error_various_messages(self) -> None:
        """Test ValidationError with different validation messages"""
        error1 = ValidationError(message="Title exceeds maximum length of 200 characters")
        assert "Title exceeds" in str(error1)

        error2 = ValidationError(message="Description exceeds maximum length of 1000 characters")
        assert "Description exceeds" in str(error2)

    def test_validation_error_is_exception(self) -> None:
        """Test ValidationError inherits from Exception"""
        error = ValidationError(message="Test error")
        assert isinstance(error, Exception)
