"""To-Do List App: a menu-driven task manager that saves to a JSON file.

Usage:
    python src/main.py                (uses data/tasks.json)
    python src/main.py path/to/file   (uses a different tasks file)
"""

import sys

from manager import TaskManager, TaskNotFoundError
from storage import DEFAULT_PATH, StorageError, load_tasks, save_tasks

MENU = """
========== To-Do List ==========
1. Add task
2. View all tasks
3. View pending tasks
4. View completed tasks
5. Mark task as complete
6. Delete task
7. Search tasks
8. Summary
9. Exit
"""


def print_tasks(tasks):
    """Print a list of tasks, or a message if there are none."""
    if not tasks:
        print("No tasks to show.")
        return
    for task in tasks:
        print(task)


def ask_task_id(prompt):
    """Ask for a task ID.

    Returns:
        int or None: The ID entered, or None if it was not a whole number.
    """
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter the task number as a whole number.")
        return None


def save(manager, path):
    """Save the tasks and report a problem without crashing."""
    try:
        save_tasks(manager.tasks, path)
    except StorageError as error:
        print(f"Warning: {error}")


def handle_add(manager, path):
    """Ask for task details and add a new task."""
    title = input("Task title: ")
    priority = input("Priority (high/medium/low) [medium]: ") or "medium"
    due_date = input("Due date YYYY-MM-DD (optional): ")
    try:
        task = manager.add_task(title, priority, due_date)
    except ValueError as error:
        print(f"Could not add task: {error}")
        return
    save(manager, path)
    print(f"Added: {task}")


def handle_complete(manager, path):
    """Ask which task to complete and mark it done."""
    task_id = ask_task_id("Task number to complete: ")
    if task_id is None:
        return
    try:
        task = manager.complete_task(task_id)
    except (TaskNotFoundError, ValueError) as error:
        print(error)
        return
    save(manager, path)
    print(f"Completed: {task}")


def handle_delete(manager, path):
    """Ask which task to delete and remove it."""
    task_id = ask_task_id("Task number to delete: ")
    if task_id is None:
        return
    try:
        task = manager.delete_task(task_id)
    except TaskNotFoundError as error:
        print(error)
        return
    save(manager, path)
    print(f"Deleted: {task.title}")


def handle_summary(manager):
    """Print the task counts."""
    stats = manager.stats()
    print(f"Total: {stats['total']} | Completed: {stats['completed']} | "
          f"Pending: {stats['pending']} | Overdue: {stats['overdue']}")


def main():
    """Load tasks, then run the menu until the user exits."""
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    try:
        manager = TaskManager(load_tasks(path))
    except StorageError as error:
        print(f"Warning: {error}")
        print("Starting with an empty list.")
        manager = TaskManager()

    while True:
        print(MENU)
        choice = input("Choose an option (1-9): ").strip()
        if choice == "1":
            handle_add(manager, path)
        elif choice == "2":
            print_tasks(manager.list_tasks("all"))
        elif choice == "3":
            print_tasks(manager.list_tasks("pending"))
        elif choice == "4":
            print_tasks(manager.list_tasks("completed"))
        elif choice == "5":
            handle_complete(manager, path)
        elif choice == "6":
            handle_delete(manager, path)
        elif choice == "7":
            print_tasks(manager.search_tasks(input("Search for: ")))
        elif choice == "8":
            handle_summary(manager)
        elif choice == "9":
            print("Goodbye! Your tasks are saved.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Goodbye!")