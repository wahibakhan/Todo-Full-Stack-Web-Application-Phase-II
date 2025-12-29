# Implemented from Task ID: T-019, T-020, T-021, T-028, T-036, T-037, T-044, T-050
"""
Unit tests for TaskStorage class and CRUD operations
TDD: These tests are written FIRST and should FAIL until implementation
"""

from datetime import datetime
import pytest
from src.todo_app.storage import TaskStorage
from src.todo_app.models import Task, TaskNotFoundError, ValidationError


class TestTaskStorageInitialization:
    """Test TaskStorage initialization"""

    def test_storage_initialization_empty(self) -> None:
        """Test that new storage starts empty with next_id=1"""
        storage = TaskStorage()
        tasks = storage.get_all_tasks()
        assert len(tasks) == 0
        assert storage._next_id == 1

    def test_storage_initialization_creates_dict(self) -> None:
        """Test that storage uses dict internally"""
        storage = TaskStorage()
        assert isinstance(storage._tasks, dict)
        assert len(storage._tasks) == 0


class TestAddTask:
    """Test TaskStorage.add_task() method"""

    def test_add_task_with_title_and_description(self) -> None:
        """Test adding task with both title and description"""
        storage = TaskStorage()
        task = storage.add_task("Buy groceries", "Milk, eggs, bread")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

    def test_add_task_with_title_only(self) -> None:
        """Test adding task with title and empty description"""
        storage = TaskStorage()
        task = storage.add_task("Complete homework")

        assert task.id == 1
        assert task.title == "Complete homework"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_increments_id(self) -> None:
        """Test that IDs increment for each new task"""
        storage = TaskStorage()

        task1 = storage.add_task("Task 1", "")
        task2 = storage.add_task("Task 2", "")
        task3 = storage.add_task("Task 3", "")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_strips_title_whitespace(self) -> None:
        """Test that title whitespace is trimmed"""
        storage = TaskStorage()
        task = storage.add_task("  Title with spaces  ", "")

        assert task.title == "Title with spaces"

    def test_add_task_empty_title_raises_error(self) -> None:
        """Test that empty title raises ValidationError"""
        storage = TaskStorage()

        with pytest.raises(ValidationError) as exc_info:
            storage.add_task("", "Description")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_add_task_whitespace_only_title_raises_error(self) -> None:
        """Test that whitespace-only title raises ValidationError"""
        storage = TaskStorage()

        with pytest.raises(ValidationError) as exc_info:
            storage.add_task("   ", "Description")

        assert "cannot be empty" in str(exc_info.value).lower()

    def test_add_task_title_too_long_raises_error(self) -> None:
        """Test that title >200 chars raises ValidationError"""
        storage = TaskStorage()
        long_title = "a" * 201

        with pytest.raises(ValidationError) as exc_info:
            storage.add_task(long_title, "")

        assert "200" in str(exc_info.value)

    def test_add_task_title_exactly_200_chars(self) -> None:
        """Test that title with exactly 200 chars is accepted"""
        storage = TaskStorage()
        title_200 = "a" * 200

        task = storage.add_task(title_200, "")
        assert len(task.title) == 200

    def test_add_task_description_too_long_raises_error(self) -> None:
        """Test that description >1000 chars raises ValidationError"""
        storage = TaskStorage()
        long_desc = "a" * 1001

        with pytest.raises(ValidationError) as exc_info:
            storage.add_task("Title", long_desc)

        assert "1000" in str(exc_info.value)

    def test_add_task_description_exactly_1000_chars(self) -> None:
        """Test that description with exactly 1000 chars is accepted"""
        storage = TaskStorage()
        desc_1000 = "a" * 1000

        task = storage.add_task("Title", desc_1000)
        assert len(task.description) == 1000


class TestGetAllTasks:
    """Test TaskStorage.get_all_tasks() method"""

    def test_get_all_tasks_empty_storage(self) -> None:
        """Test getting all tasks from empty storage"""
        storage = TaskStorage()
        tasks = storage.get_all_tasks()

        assert isinstance(tasks, list)
        assert len(tasks) == 0

    def test_get_all_tasks_single_task(self) -> None:
        """Test getting all tasks with one task"""
        storage = TaskStorage()
        added = storage.add_task("Task 1", "")

        tasks = storage.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == added.id
        assert tasks[0].title == "Task 1"

    def test_get_all_tasks_multiple_tasks(self) -> None:
        """Test getting all tasks with multiple tasks"""
        storage = TaskStorage()
        storage.add_task("Task 1", "")
        storage.add_task("Task 2", "")
        storage.add_task("Task 3", "")

        tasks = storage.get_all_tasks()
        assert len(tasks) == 3

    def test_get_all_tasks_sorted_by_id(self) -> None:
        """Test that tasks are returned sorted by ID (ascending)"""
        storage = TaskStorage()
        storage.add_task("Task 1", "")
        storage.add_task("Task 2", "")
        storage.add_task("Task 3", "")

        tasks = storage.get_all_tasks()
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3


class TestGetTaskById:
    """Test TaskStorage.get_task_by_id() method"""

    def test_get_task_by_id_valid_id(self) -> None:
        """Test retrieving task with valid ID"""
        storage = TaskStorage()
        added = storage.add_task("Task 1", "Description 1")

        task = storage.get_task_by_id(1)
        assert task.id == 1
        assert task.title == "Task 1"
        assert task.description == "Description 1"

    def test_get_task_by_id_multiple_tasks(self) -> None:
        """Test retrieving specific task when multiple exist"""
        storage = TaskStorage()
        storage.add_task("Task 1", "")
        storage.add_task("Task 2", "")
        task3 = storage.add_task("Task 3", "")

        retrieved = storage.get_task_by_id(3)
        assert retrieved.id == task3.id
        assert retrieved.title == "Task 3"

    def test_get_task_by_id_invalid_id_raises_error(self) -> None:
        """Test that invalid ID raises TaskNotFoundError"""
        storage = TaskStorage()
        storage.add_task("Task 1", "")

        with pytest.raises(TaskNotFoundError) as exc_info:
            storage.get_task_by_id(999)

        assert exc_info.value.task_id == 999
        assert "999" in str(exc_info.value)

    def test_get_task_by_id_empty_storage_raises_error(self) -> None:
        """Test that getting from empty storage raises TaskNotFoundError"""
        storage = TaskStorage()

        with pytest.raises(TaskNotFoundError):
            storage.get_task_by_id(1)


class TestUpdateTask:
    """Test TaskStorage.update_task() method"""

    def test_update_task_title_only(self) -> None:
        """Test updating title while preserving description"""
        storage = TaskStorage()
        storage.add_task("Old title", "Original description")

        updated = storage.update_task(1, title="New title")
        assert updated.title == "New title"
        assert updated.description == "Original description"

    def test_update_task_description_only(self) -> None:
        """Test updating description while preserving title"""
        storage = TaskStorage()
        storage.add_task("Title", "Old description")

        updated = storage.update_task(1, description="New description")
        assert updated.title == "Title"
        assert updated.description == "New description"

    def test_update_task_both_fields(self) -> None:
        """Test updating both title and description"""
        storage = TaskStorage()
        storage.add_task("Old title", "Old description")

        updated = storage.update_task(1, title="New title", description="New description")
        assert updated.title == "New title"
        assert updated.description == "New description"

    def test_update_task_preserves_id(self) -> None:
        """Test that update preserves task ID"""
        storage = TaskStorage()
        original = storage.add_task("Title", "")

        updated = storage.update_task(1, title="New title")
        assert updated.id == original.id

    def test_update_task_preserves_completed(self) -> None:
        """Test that update preserves completed status"""
        storage = TaskStorage()
        task = storage.add_task("Title", "")
        storage.toggle_complete(task.id)  # Mark complete

        updated = storage.update_task(1, title="New title")
        assert updated.completed is True

    def test_update_task_preserves_created_at(self) -> None:
        """Test that update preserves creation timestamp"""
        storage = TaskStorage()
        original = storage.add_task("Title", "")
        original_time = original.created_at

        updated = storage.update_task(1, title="New title")
        assert updated.created_at == original_time

    def test_update_task_invalid_id_raises_error(self) -> None:
        """Test that updating non-existent task raises TaskNotFoundError"""
        storage = TaskStorage()

        with pytest.raises(TaskNotFoundError) as exc_info:
            storage.update_task(999, title="Title")

        assert exc_info.value.task_id == 999

    def test_update_task_title_validation(self) -> None:
        """Test that update validates new title"""
        storage = TaskStorage()
        storage.add_task("Original", "")

        # Empty title should fail
        with pytest.raises(ValidationError):
            storage.update_task(1, title="")

        # Too long title should fail
        with pytest.raises(ValidationError):
            storage.update_task(1, title="a" * 201)

    def test_update_task_description_validation(self) -> None:
        """Test that update validates new description"""
        storage = TaskStorage()
        storage.add_task("Title", "Original")

        # Too long description should fail
        with pytest.raises(ValidationError):
            storage.update_task(1, description="a" * 1001)


class TestDeleteTask:
    """Test TaskStorage.delete_task() method"""

    def test_delete_task_valid_id(self) -> None:
        """Test deleting task with valid ID"""
        storage = TaskStorage()
        added = storage.add_task("Task to delete", "")

        deleted = storage.delete_task(1)
        assert deleted.id == added.id
        assert deleted.title == "Task to delete"

        tasks = storage.get_all_tasks()
        assert len(tasks) == 0

    def test_delete_task_removes_from_storage(self) -> None:
        """Test that deleted task is removed from storage"""
        storage = TaskStorage()
        storage.add_task("Task 1", "")
        storage.add_task("Task 2", "")
        storage.add_task("Task 3", "")

        storage.delete_task(2)

        tasks = storage.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 3

    def test_delete_task_id_not_reused(self) -> None:
        """Test that deleted task ID is never reused"""
        storage = TaskStorage()
        storage.add_task("Task 1", "")
        storage.delete_task(1)

        # Add new task - should get ID 2, not reuse ID 1
        new_task = storage.add_task("Task 2", "")
        assert new_task.id == 2

    def test_delete_task_invalid_id_raises_error(self) -> None:
        """Test that deleting non-existent task raises TaskNotFoundError"""
        storage = TaskStorage()

        with pytest.raises(TaskNotFoundError) as exc_info:
            storage.delete_task(999)

        assert exc_info.value.task_id == 999


class TestToggleComplete:
    """Test TaskStorage.toggle_complete() method"""

    def test_toggle_complete_false_to_true(self) -> None:
        """Test toggling incomplete task to complete"""
        storage = TaskStorage()
        task = storage.add_task("Task", "")
        assert task.completed is False

        toggled = storage.toggle_complete(1)
        assert toggled.completed is True

    def test_toggle_complete_true_to_false(self) -> None:
        """Test toggling complete task to incomplete"""
        storage = TaskStorage()
        task = storage.add_task("Task", "")
        storage.toggle_complete(task.id)  # Make it complete

        toggled = storage.toggle_complete(task.id)  # Toggle back
        assert toggled.completed is False

    def test_toggle_complete_multiple_times(self) -> None:
        """Test toggling task multiple times"""
        storage = TaskStorage()
        task = storage.add_task("Task", "")

        # False → True → False → True
        storage.toggle_complete(task.id)
        result1 = storage.get_task_by_id(task.id)
        assert result1.completed is True

        storage.toggle_complete(task.id)
        result2 = storage.get_task_by_id(task.id)
        assert result2.completed is False

        storage.toggle_complete(task.id)
        result3 = storage.get_task_by_id(task.id)
        assert result3.completed is True

    def test_toggle_complete_invalid_id_raises_error(self) -> None:
        """Test that toggling non-existent task raises TaskNotFoundError"""
        storage = TaskStorage()

        with pytest.raises(TaskNotFoundError) as exc_info:
            storage.toggle_complete(999)

        assert exc_info.value.task_id == 999
