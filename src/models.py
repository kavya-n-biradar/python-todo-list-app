"""Task model and validation helpers for the To-Do List app."""

from datetime import date, datetime

PRIORITIES = ("high", "medium", "low")
DATE_FORMAT = "%Y-%m-%d"


def validate_title(title):
    """Return a cleaned task title.

    Args:
        title (str): The title typed by the user.

    Returns:
        str: The title without surrounding spaces.

    Raises:
        ValueError: If the title is empty.
    """
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    return title


def validate_priority(priority):
    """Return a valid lowercase priority.

    Args:
        priority (str): The priority typed by the user.

    Returns:
        str: One of "high", "medium" or "low".

    Raises:
        ValueError: If the priority is not one of the allowed values.
    """
    priority = priority.strip().lower()
    if priority not in PRIORITIES:
        raise ValueError("Priority must be high, medium or low.")
    return priority


def validate_due_date(text):
    """Return a due date as YYYY-MM-DD, or None if left blank.

    Args:
        text (str): The date typed by the user (may be empty).

    Returns:
        str or None: The normalised date, or None if no date was given.

    Raises:
        ValueError: If the text is not a real date in YYYY-MM-DD format.
    """
    text = text.strip()
    if not text:
        return None
    try:
        parsed = datetime.strptime(text, DATE_FORMAT)
    except ValueError:
        raise ValueError("Due date must be a real date like 2026-12-31.")
    return parsed.strftime(DATE_FORMAT)


class Task:
    """A single to-do item."""

    def __init__(self, task_id, title, priority="medium", due_date=None,
                 completed=False):
        """Create a task.

        Args:
            task_id (int): The unique ID of the task.
            title (str): What needs to be done.
            priority (str): "high", "medium" or "low".
            due_date (str or None): Due date as YYYY-MM-DD, if any.
            completed (bool): Whether the task is done.
        """
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def mark_complete(self):
        """Mark the task as done."""
        self.completed = True

    def is_overdue(self, today=None):
        """Check whether the task is past its due date and not complete.

        Args:
            today (date or None): The date to compare with (default: today).

        Returns:
            bool: True if the task is overdue.
        """
        if self.completed or not self.due_date:
            return False
        today = today or date.today()
        due = datetime.strptime(self.due_date, DATE_FORMAT).date()
        return due < today

    def to_dict(self):
        """Return the task as a dictionary, ready to save as JSON."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a task from a dictionary loaded from JSON.

        Raises:
            KeyError: If a required field is missing.
        """
        return cls(
            data["task_id"],
            data["title"],
            data["priority"],
            data.get("due_date"),
            data.get("completed", False),
        )

    def __str__(self):
        """Return a one-line description of the task."""
        mark = "x" if self.completed else " "
        text = f"[{mark}] #{self.task_id} {self.title} ({self.priority})"
        if self.due_date:
            text += f" - due {self.due_date}"
        if self.is_overdue():
            text += " - OVERDUE"
        return text