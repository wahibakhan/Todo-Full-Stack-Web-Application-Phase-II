# Implemented from Task ID: T-013, T-058, T-059, T-060
"""
Integration tests for complete workflows
TDD: These tests are written FIRST and should FAIL until implementation
"""

import io
import sys
from unittest.mock import patch
import pytest
from src.todo_app.main import main
from src.todo_app.storage import TaskStorage
from datetime import datetime


class TestMainLoop:
    """Test main application loop"""

    @patch('builtins.input', side_effect=['6'])
    def test_main_loop_exit(self, mock_input: any) -> None:
        """Test that selecting exit (6) terminates the loop"""
        output = io.StringIO()
        with patch('sys.stdout', output):
            main()

        result = output.getvalue()
        assert "Thank you" in result or "Goodbye" in result or "goodbye" in result


class TestFullCRUDWorkflow:
    """Test complete CRUD workflow in sequence"""

    def test_add_list_update_toggle_delete_workflow(self) -> None:
        """Test full CRUD workflow: add → list → update → toggle → delete"""
        storage = TaskStorage()

        # Add task
        task1 = storage.add_task("Buy groceries", "Milk, eggs")
        assert task1.id == 1
        assert task1.title == "Buy groceries"
        assert task1.completed is False

        # List tasks
        tasks = storage.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"

        # Update task
        updated = storage.update_task(1, title="Buy groceries and fruits")
        assert updated.title == "Buy groceries and fruits"
        assert updated.description == "Milk, eggs"  # Preserved

        # Toggle complete
        toggled = storage.toggle_complete(1)
        assert toggled.completed is True

        # Delete task
        deleted = storage.delete_task(1)
        assert deleted.id == 1
        assert len(storage.get_all_tasks()) == 0


class TestValidationErrorRecovery:
    """Test recovery from validation errors"""

    def test_empty_title_then_valid_title(self) -> None:
        """Test adding task fails with empty title, then succeeds with valid title"""
        storage = TaskStorage()

        # Empty title should fail
        with pytest.raises(Exception):  # ValidationError
            storage.add_task("", "Description")

        # Valid title should succeed
        task = storage.add_task("Valid title", "Description")
        assert task.title == "Valid title"
        assert len(storage.get_all_tasks()) == 1

    def test_title_too_long_then_valid(self) -> None:
        """Test title exceeding 200 chars fails, then valid succeeds"""
        storage = TaskStorage()

        # Title too long (>200 chars)
        long_title = "a" * 201
        with pytest.raises(Exception):  # ValidationError
            storage.add_task(long_title, "")

        # Valid title
        task = storage.add_task("Valid title", "")
        assert task.title == "Valid title"

    def test_description_too_long_then_valid(self) -> None:
        """Test description exceeding 1000 chars fails, then valid succeeds"""
        storage = TaskStorage()

        # Description too long (>1000 chars)
        long_desc = "a" * 1001
        with pytest.raises(Exception):  # ValidationError
            storage.add_task("Title", long_desc)

        # Valid description
        task = storage.add_task("Title", "Valid description")
        assert task.description == "Valid description"


class TestPerformanceWith100Tasks:
    """Test performance with 100 tasks"""

    def test_add_100_tasks_performance(self) -> None:
        """Test adding 100 tasks completes reasonably fast"""
        storage = TaskStorage()
        start_time = datetime.now()

        for i in range(100):
            storage.add_task(f"Task {i + 1}", f"Description {i + 1}")

        elapsed = (datetime.now() - start_time).total_seconds()
        assert elapsed < 10  # Should complete in under 10 seconds

        tasks = storage.get_all_tasks()
        assert len(tasks) == 100

    def test_list_100_tasks_performance(self) -> None:
        """Test listing 100 tasks completes in under 1 second"""
        storage = TaskStorage()

        # Add 100 tasks
        for i in range(100):
            storage.add_task(f"Task {i + 1}", "")

        # Time the list operation
        start_time = datetime.now()
        tasks = storage.get_all_tasks()
        elapsed = (datetime.now() - start_time).total_seconds()

        assert elapsed < 1  # Should complete in under 1 second
        assert len(tasks) == 100

    def test_operations_on_100_tasks(self) -> None:
        """Test various operations remain fast with 100 tasks"""
        storage = TaskStorage()

        # Add 100 tasks
        for i in range(100):
            storage.add_task(f"Task {i + 1}", "")

        # Get by ID (should be O(1))
        start_time = datetime.now()
        task = storage.get_task_by_id(50)
        elapsed = (datetime.now() - start_time).total_seconds()
        assert elapsed < 0.1  # Should be nearly instant
        assert task.title == "Task 50"

        # Update task
        storage.update_task(75, title="Updated Task 75")
        updated = storage.get_task_by_id(75)
        assert updated.title == "Updated Task 75"

        # Toggle complete
        storage.toggle_complete(25)
        toggled = storage.get_task_by_id(25)
        assert toggled.completed is True

        # Delete task
        storage.delete_task(100)
        tasks = storage.get_all_tasks()
        assert len(tasks) == 99
