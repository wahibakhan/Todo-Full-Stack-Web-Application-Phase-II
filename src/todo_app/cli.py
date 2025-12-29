# Implemented from Task ID: T-014, T-015, T-016, T-025, T-032, T-033, T-034, T-041, T-047, T-048, T-053
"""
Command-line interface functions for user interaction
Handles display formatting, input prompts, and user feedback
"""

from typing import Optional
from src.todo_app.storage import TaskStorage
from src.todo_app.models import Task, TaskNotFoundError, ValidationError


def display_welcome() -> None:
    """Display welcome banner and in-memory notice"""
    print("=" * 40)
    print("    Console Todo App - Phase 1")
    print("=" * 40)
    print("In-memory only - data not saved between runs")
    print()


def display_menu() -> None:
    """Display main menu with all 6 options"""
    print("=== Main Menu ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Update task")
    print("4. Delete task")
    print("5. Toggle complete")
    print("6. Exit")
    print()


def get_menu_choice() -> int:
    """
    Prompt user for menu choice and validate input

    Returns:
        Valid menu choice (1-6)
    """
    while True:
        try:
            choice = input("Enter choice (1-6): ")
            choice_int = int(choice)

            if 1 <= choice_int <= 6:
                return choice_int
            else:
                print("X Invalid choice. Please enter a number between 1 and 6.")

        except ValueError:
            print("X Invalid input. Please enter a number between 1 and 6.")


def add_task_ui(storage: TaskStorage) -> None:
    """
    User interface for adding a new task

    Args:
        storage: TaskStorage instance to add task to
    """
    while True:
        try:
            print("\n=== Add New Task ===")
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")

            task = storage.add_task(title, description)

            print(f"\n[OK] Task added successfully!")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            if task.description:
                print(f"  Description: {task.description}")

            print()  # Empty line for spacing
            break

        except ValidationError as e:
            print(f"\n[ERROR] Validation error: {e.message}")
            print("Please try again.\n")


def format_task_list(tasks: list[Task]) -> str:
    """
    Format task list in tabular format

    Args:
        tasks: List of Task instances to format

    Returns:
        Formatted string with task table or empty message
    """
    if not tasks:
        return "No tasks found."

    # Build table
    lines = []
    lines.append("ID  Status  Title                Description")
    lines.append("--  ------  -------------------  ---------------------------")

    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        title_truncated = task.title[:19] if len(task.title) <= 19 else task.title[:19]
        desc_truncated = task.description[:27] if len(task.description) <= 27 else task.description[:24] + "..."

        lines.append(f"{task.id:<3} {status:<7} {title_truncated:<20} {desc_truncated}")

    return "\n".join(lines)


def display_task_summary(tasks: list[Task]) -> None:
    """
    Display summary of task counts

    Args:
        tasks: List of Task instances to summarize
    """
    total = len(tasks)
    completed = sum(1 for task in tasks if task.completed)
    incomplete = total - completed

    print(f"\nTotal: {total} tasks ({incomplete} incomplete, {completed} completed)")


def list_tasks_ui(storage: TaskStorage) -> None:
    """
    User interface for listing all tasks

    Args:
        storage: TaskStorage instance to list tasks from
    """
    print("\n=== Task List ===")
    tasks = storage.get_all_tasks()

    print(format_task_list(tasks))
    display_task_summary(tasks)

    print()  # Empty line for spacing


def update_task_ui(storage: TaskStorage) -> None:
    """
    User interface for updating a task

    Args:
        storage: TaskStorage instance to update task in
    """
    while True:
        try:
            print("\n=== Update Task ===")
            task_id_input = input("Enter task ID: ")
            task_id = int(task_id_input)

            # Show current task
            task = storage.get_task_by_id(task_id)
            print(f"\nCurrent task:")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description}")

            # Get new values
            print("\n(Press Enter to keep current value)")
            new_title_input = input("Enter new title: ")
            new_description_input = input("Enter new description: ")

            # Determine what to update
            new_title = new_title_input if new_title_input else None
            new_description = new_description_input if new_description_input else None

            # Update task
            updated = storage.update_task(task_id, title=new_title, description=new_description)

            print(f"\n[OK] Task updated successfully!")
            print(f"  ID: {updated.id}")
            print(f"  Title: {updated.title}")
            print(f"  Description: {updated.description}")

            print()  # Empty line for spacing
            break

        except ValueError:
            print("\n[ERROR] Invalid task ID: please enter a positive number")
            print("Please try again.\n")

        except TaskNotFoundError as e:
            print(f"\n[ERROR] Task not found: {e}")
            print("Please try again.\n")

        except ValidationError as e:
            print(f"\n[ERROR] Validation error: {e.message}")
            print("Please try again.\n")


def delete_task_ui(storage: TaskStorage) -> None:
    """
    User interface for deleting a task

    Args:
        storage: TaskStorage instance to delete task from
    """
    while True:
        try:
            print("\n=== Delete Task ===")
            task_id_input = input("Enter task ID: ")
            task_id = int(task_id_input)

            # Show task to be deleted
            task = storage.get_task_by_id(task_id)
            print(f"\nTask to delete:")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description}")

            # Confirm deletion
            confirmation = input("\nAre you sure you want to delete this task? (y/n): ")

            if confirmation.lower() == 'y':
                deleted = storage.delete_task(task_id)
                print(f"\n[OK] Task deleted successfully!")
                print(f"  ID: {deleted.id}")
                print(f"  Title: {deleted.title}")
            else:
                print("\n[CANCELLED] Deletion cancelled.")

            print()  # Empty line for spacing
            break

        except ValueError:
            print("\n[ERROR] Invalid task ID: please enter a positive number")
            print("Please try again.\n")

        except TaskNotFoundError as e:
            print(f"\n[ERROR] Task not found: {e}")
            print("Please try again.\n")


def toggle_complete_ui(storage: TaskStorage) -> None:
    """
    User interface for toggling task completion

    Args:
        storage: TaskStorage instance to toggle task in
    """
    while True:
        try:
            print("\n=== Toggle Task Completion ===")
            task_id_input = input("Enter task ID: ")
            task_id = int(task_id_input)

            # Toggle completion
            toggled = storage.toggle_complete(task_id)

            status = "complete" if toggled.completed else "incomplete"
            print(f"\n[OK] Task marked as {status}!")
            print(f"  ID: {toggled.id}")
            print(f"  Title: {toggled.title}")

            print()  # Empty line for spacing
            break

        except ValueError:
            print("\n[ERROR] Invalid task ID: please enter a positive number")
            print("Please try again.\n")

        except TaskNotFoundError as e:
            print(f"\n[ERROR] Task not found: {e}")
            print("Please try again.\n")
