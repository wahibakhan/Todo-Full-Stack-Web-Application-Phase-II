# Implemented from Task ID: T-017, T-018, T-026, T-035, T-042, T-049, T-054
"""
Main entry point for Console Todo Application
Orchestrates the application loop and command routing
"""

import sys
from src.todo_app.storage import TaskStorage
from src.todo_app.cli import (
    display_welcome,
    display_menu,
    get_menu_choice,
    add_task_ui,
    list_tasks_ui,
    update_task_ui,
    delete_task_ui,
    toggle_complete_ui
)


def main() -> None:
    """
    Main application loop
    Displays menu, routes commands, and handles exit
    """
    # Initialize storage
    storage = TaskStorage()

    # Display welcome banner
    display_welcome()

    # Main loop
    while True:
        try:
            # Display menu and get choice
            display_menu()
            choice = get_menu_choice()

            # Route to appropriate handler
            if choice == 1:
                add_task_ui(storage)
            elif choice == 2:
                list_tasks_ui(storage)
            elif choice == 3:
                update_task_ui(storage)
            elif choice == 4:
                delete_task_ui(storage)
            elif choice == 5:
                toggle_complete_ui(storage)
            elif choice == 6:
                # Exit
                print("\nThank you for using Console Todo App!")
                print("All data has been cleared from memory.")
                break

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nThank you for using Console Todo App!")
            print("All data has been cleared from memory.")
            sys.exit(0)


if __name__ == "__main__":
    main()
