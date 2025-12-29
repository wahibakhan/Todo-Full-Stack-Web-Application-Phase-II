# Implemented from Task ID: T-010, T-011, T-012, T-022, T-029, T-030, T-038, T-045, T-051
"""
Unit tests for CLI interface functions
TDD: These tests are written FIRST and should FAIL until implementation
"""

import io
import sys
from unittest.mock import patch
import pytest
from src.todo_app.cli import (
    display_welcome,
    display_menu,
    get_menu_choice,
    add_task_ui,
    format_task_list,
    display_task_summary,
    list_tasks_ui,
    update_task_ui,
    delete_task_ui,
    toggle_complete_ui
)
from src.todo_app.storage import TaskStorage
from src.todo_app.models import Task, TaskNotFoundError, ValidationError
from datetime import datetime


class TestDisplayWelcome:
    """Test welcome banner display"""

    def test_display_welcome_shows_banner(self) -> None:
        """Test that welcome message displays app title"""
        output = io.StringIO()
        with patch('sys.stdout', output):
            display_welcome()

        result = output.getvalue()
        assert "Console Todo App" in result
        assert "Phase 1" in result

    def test_display_welcome_shows_memory_warning(self) -> None:
        """Test that welcome shows in-memory notice"""
        output = io.StringIO()
        with patch('sys.stdout', output):
            display_welcome()

        result = output.getvalue()
        assert "in-memory" in result.lower() or "memory" in result.lower()
        assert "not saved" in result.lower() or "not persist" in result.lower()


class TestDisplayMenu:
    """Test main menu display"""

    def test_display_menu_shows_all_options(self) -> None:
        """Test that menu displays all 6 required options"""
        output = io.StringIO()
        with patch('sys.stdout', output):
            display_menu()

        result = output.getvalue()
        assert "1" in result and ("Add" in result or "add" in result)
        assert "2" in result and ("List" in result or "list" in result)
        assert "3" in result and ("Update" in result or "update" in result)
        assert "4" in result and ("Delete" in result or "delete" in result)
        assert "5" in result and ("Toggle" in result or "toggle" in result or "Complete" in result)
        assert "6" in result and ("Exit" in result or "exit" in result)

    def test_display_menu_has_clear_formatting(self) -> None:
        """Test that menu has clear structure"""
        output = io.StringIO()
        with patch('sys.stdout', output):
            display_menu()

        result = output.getvalue()
        assert "Menu" in result or "MENU" in result
        lines = result.strip().split('\n')
        assert len(lines) >= 6  # At least 6 menu options


class TestGetMenuChoice:
    """Test menu input validation"""

    @patch('builtins.input', return_value='1')
    def test_get_menu_choice_valid_input_1(self, mock_input: any) -> None:
        """Test valid menu choice 1"""
        choice = get_menu_choice()
        assert choice == 1

    @patch('builtins.input', return_value='6')
    def test_get_menu_choice_valid_input_6(self, mock_input: any) -> None:
        """Test valid menu choice 6"""
        choice = get_menu_choice()
        assert choice == 6

    @patch('builtins.input', side_effect=['abc', '2'])
    def test_get_menu_choice_invalid_then_valid(self, mock_input: any) -> None:
        """Test recovery from non-numeric input"""
        choice = get_menu_choice()
        assert choice == 2

    @patch('builtins.input', side_effect=['0', '3'])
    def test_get_menu_choice_out_of_range_low(self, mock_input: any) -> None:
        """Test recovery from out-of-range input (too low)"""
        choice = get_menu_choice()
        assert choice == 3

    @patch('builtins.input', side_effect=['7', '4'])
    def test_get_menu_choice_out_of_range_high(self, mock_input: any) -> None:
        """Test recovery from out-of-range input (too high)"""
        choice = get_menu_choice()
        assert choice == 4


class TestAddTaskUI:
    """Test add task user interface"""

    @patch('builtins.input', side_effect=['Buy groceries', 'Milk, eggs, bread'])
    def test_add_task_ui_with_description(self, mock_input: any) -> None:
        """Test adding task with title and description"""
        storage = TaskStorage()
        output = io.StringIO()

        with patch('sys.stdout', output):
            add_task_ui(storage)

        result = output.getvalue()
        assert "added successfully" in result.lower() or "created" in result.lower()
        assert "1" in result  # Task ID
        assert len(storage.get_all_tasks()) == 1

    @patch('builtins.input', side_effect=['Complete homework', ''])
    def test_add_task_ui_without_description(self, mock_input: any) -> None:
        """Test adding task with title only"""
        storage = TaskStorage()
        output = io.StringIO()

        with patch('sys.stdout', output):
            add_task_ui(storage)

        tasks = storage.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Complete homework"
        assert tasks[0].description == ""

    @patch('builtins.input', side_effect=['', 'description that wont be used', 'Valid title', ''])
    def test_add_task_ui_retry_on_empty_title(self, mock_input: any) -> None:
        """Test retry after empty title validation error"""
        storage = TaskStorage()
        output = io.StringIO()

        with patch('sys.stdout', output):
            add_task_ui(storage)

        result = output.getvalue()
        assert "cannot be empty" in result.lower() or "required" in result.lower()
        tasks = storage.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Valid title"


class TestFormatTaskList:
    """Test task list formatting"""

    def test_format_task_list_empty(self) -> None:
        """Test formatting empty task list"""
        result = format_task_list([])
        assert "No tasks" in result or "empty" in result.lower()

    def test_format_task_list_single_incomplete(self) -> None:
        """Test formatting single incomplete task"""
        task = Task(1, "Buy groceries", "Milk, eggs", False, datetime.now())
        result = format_task_list([task])

        assert "1" in result
        assert "Buy groceries" in result
        assert "[ ]" in result or "incomplete" in result.lower()

    def test_format_task_list_single_complete(self) -> None:
        """Test formatting single complete task"""
        task = Task(2, "Homework", "Math", True, datetime.now())
        result = format_task_list([task])

        assert "2" in result
        assert "Homework" in result
        assert "[x]" in result or "[X]" in result or "complete" in result.lower()

    def test_format_task_list_multiple_tasks(self) -> None:
        """Test formatting multiple tasks"""
        tasks = [
            Task(1, "Task 1", "", False, datetime.now()),
            Task(2, "Task 2", "Description", True, datetime.now()),
            Task(3, "Task 3", "", False, datetime.now())
        ]
        result = format_task_list(tasks)

        assert "1" in result and "Task 1" in result
        assert "2" in result and "Task 2" in result
        assert "3" in result and "Task 3" in result


class TestDisplayTaskSummary:
    """Test task summary display"""

    def test_display_task_summary_empty(self) -> None:
        """Test summary with no tasks"""
        output = io.StringIO()
        with patch('sys.stdout', output):
            display_task_summary([])

        result = output.getvalue()
        assert "0" in result
        assert "total" in result.lower()

    def test_display_task_summary_mixed(self) -> None:
        """Test summary with mix of complete/incomplete tasks"""
        tasks = [
            Task(1, "Task 1", "", False, datetime.now()),
            Task(2, "Task 2", "", True, datetime.now()),
            Task(3, "Task 3", "", False, datetime.now())
        ]

        output = io.StringIO()
        with patch('sys.stdout', output):
            display_task_summary(tasks)

        result = output.getvalue()
        assert "3" in result  # Total
        assert "2" in result  # Incomplete count
        assert "1" in result  # Complete count


class TestListTasksUI:
    """Test list tasks user interface"""

    def test_list_tasks_ui_empty(self) -> None:
        """Test listing when no tasks exist"""
        storage = TaskStorage()
        output = io.StringIO()

        with patch('sys.stdout', output):
            list_tasks_ui(storage)

        result = output.getvalue()
        assert "No tasks" in result or "empty" in result.lower()

    def test_list_tasks_ui_with_tasks(self) -> None:
        """Test listing when tasks exist"""
        storage = TaskStorage()
        storage.add_task("Task 1", "Description 1")
        storage.add_task("Task 2", "")

        output = io.StringIO()
        with patch('sys.stdout', output):
            list_tasks_ui(storage)

        result = output.getvalue()
        assert "Task 1" in result
        assert "Task 2" in result
        assert "2" in result  # Total count


class TestUpdateTaskUI:
    """Test update task user interface"""

    @patch('builtins.input', side_effect=['1', 'Updated title', 'Updated description'])
    def test_update_task_ui_both_fields(self, mock_input: any) -> None:
        """Test updating both title and description"""
        storage = TaskStorage()
        storage.add_task("Original title", "Original description")

        output = io.StringIO()
        with patch('sys.stdout', output):
            update_task_ui(storage)

        result = output.getvalue()
        assert "updated successfully" in result.lower()

        task = storage.get_task_by_id(1)
        assert task.title == "Updated title"
        assert task.description == "Updated description"

    @patch('builtins.input', side_effect=['1', 'New title only', ''])
    def test_update_task_ui_title_only(self, mock_input: any) -> None:
        """Test updating title only"""
        storage = TaskStorage()
        storage.add_task("Old title", "Keep this description")

        update_task_ui(storage)

        task = storage.get_task_by_id(1)
        assert task.title == "New title only"
        assert task.description == "Keep this description"

    @patch('builtins.input', side_effect=['999', '1', '', 'New description'])
    def test_update_task_ui_invalid_id_retry(self, mock_input: any) -> None:
        """Test retry after invalid task ID"""
        storage = TaskStorage()
        storage.add_task("Title", "Old description")

        output = io.StringIO()
        with patch('sys.stdout', output):
            update_task_ui(storage)

        result = output.getvalue()
        assert "not found" in result.lower()


class TestDeleteTaskUI:
    """Test delete task user interface"""

    @patch('builtins.input', side_effect=['1', 'y'])
    def test_delete_task_ui_confirm_yes(self, mock_input: any) -> None:
        """Test deleting task with confirmation 'y'"""
        storage = TaskStorage()
        storage.add_task("Task to delete", "")

        output = io.StringIO()
        with patch('sys.stdout', output):
            delete_task_ui(storage)

        result = output.getvalue()
        assert "deleted successfully" in result.lower()
        assert len(storage.get_all_tasks()) == 0

    @patch('builtins.input', side_effect=['1', 'n'])
    def test_delete_task_ui_confirm_no(self, mock_input: any) -> None:
        """Test canceling deletion with 'n'"""
        storage = TaskStorage()
        storage.add_task("Task to keep", "")

        output = io.StringIO()
        with patch('sys.stdout', output):
            delete_task_ui(storage)

        result = output.getvalue()
        assert "cancel" in result.lower() or "abort" in result.lower()
        assert len(storage.get_all_tasks()) == 1

    @patch('builtins.input', side_effect=['1', 'Y'])
    def test_delete_task_ui_confirm_case_insensitive(self, mock_input: any) -> None:
        """Test confirmation is case insensitive"""
        storage = TaskStorage()
        storage.add_task("Task", "")

        delete_task_ui(storage)

        assert len(storage.get_all_tasks()) == 0


class TestToggleCompleteUI:
    """Test toggle complete user interface"""

    @patch('builtins.input', return_value='1')
    def test_toggle_complete_ui_false_to_true(self, mock_input: any) -> None:
        """Test toggling incomplete task to complete"""
        storage = TaskStorage()
        storage.add_task("Task", "")

        output = io.StringIO()
        with patch('sys.stdout', output):
            toggle_complete_ui(storage)

        result = output.getvalue()
        assert "complete" in result.lower()

        task = storage.get_task_by_id(1)
        assert task.completed is True

    @patch('builtins.input', return_value='1')
    def test_toggle_complete_ui_true_to_false(self, mock_input: any) -> None:
        """Test toggling complete task to incomplete"""
        storage = TaskStorage()
        task = storage.add_task("Task", "")
        storage.toggle_complete(task.id)  # Make it complete first

        toggle_complete_ui(storage)

        task = storage.get_task_by_id(1)
        assert task.completed is False

    @patch('builtins.input', side_effect=['999', '1'])
    def test_toggle_complete_ui_invalid_id_retry(self, mock_input: any) -> None:
        """Test retry after invalid task ID"""
        storage = TaskStorage()
        storage.add_task("Task", "")

        output = io.StringIO()
        with patch('sys.stdout', output):
            toggle_complete_ui(storage)

        result = output.getvalue()
        assert "not found" in result.lower()
