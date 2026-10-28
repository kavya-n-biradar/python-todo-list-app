"""TaskManager: the logic for adding, finding and changing tasks."""

from models import (Task, validate_due_date, validate_priority,
                    validate_title)

STATUSES = ("all", "pending", "completed")


class TaskNotFoundError(Exception):
    """Raised when no task has the requested ID."""


class TaskManager:
    """Keeps a list of tasks and provides operations on it."""

    def __init__(self, tasks=None):
        """Create a manager, optionally starting with existing tasks."""
        self.tasks = list(tasks or [])

    def _next_id(self):
        """Return an ID one higher than any existing ID."""
        return max((task.task_id for task in self.tasks), default=0) + 1

    def add_task(self, title, priority="medium", due_date=""):
        """Create and store a new task.

        Args:
            title (str): What needs to be done.
            priority (str): "high", "medium" or "low".
            due_date (str): Due date as YYYY-MM-DD, or empty for none.

        Returns:
            Task: The task that was added.

        Raises:
            ValueError: If the title, priority or date is invalid.
        """
        task = Task(
            self._next_id(),
            validate_title(title),
            validate_priority(priority),
            validate_due_date(due_date),
        )
        self.tasks.append(task)
        return task

    def find_task(self, task_id):
        """Return the task with the given ID.

        Raises:
            TaskNotFoundError: If there is no such task.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise TaskNotFoundError(f"No task with ID {task_id}.")

    def complete_task(self, task_id):
        """Mark a task as done and return it.

        Raises:
            TaskNotFoundError: If there is no such task.
            ValueError: If the task is already complete.
        """
        task = self.find_task(task_id)
        if task.completed:
            raise ValueError(f"Task #{task_id} is already complete.")
        task.mark_complete()
        return task

    def delete_task(self, task_id):
        """Remove a task and return it.

        Raises:
            TaskNotFoundError: If there is no such task.
        """
        task = self.find_task(task_id)
        self.tasks.remove(task)
        return task

    def list_tasks(self, status="all"):
        """Return tasks filtered by status.

        Args:
            status (str): "all", "pending" or "completed".

        Raises:
            ValueError: If the status is not recognised.
        """
        if status not in STATUSES:
            raise ValueError(f"Status must be one of {STATUSES}.")
        if status == "pending":
            return [task for task in self.tasks if not task.completed]
        if status == "completed":
            return [task for task in self.tasks if task.completed]
        return list(self.tasks)

    def search_tasks(self, keyword):
        """Return tasks whose title contains the keyword (ignoring case)."""
        keyword = keyword.strip().lower()
        if not keyword:
            return []
        return [task for task in self.tasks if keyword in task.title.lower()]

    def stats(self):
        """Return a dictionary of task counts."""
        completed = sum(1 for task in self.tasks if task.completed)
        overdue = sum(1 for task in self.tasks if task.is_overdue())
        return {
            "total": len(self.tasks),
            "completed": completed,
            "pending": len(self.tasks) - completed,
            "overdue": overdue,
        }