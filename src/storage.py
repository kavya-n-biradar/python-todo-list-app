"""Saving and loading tasks as a JSON file."""

import json
from pathlib import Path

from models import Task

# Default file, found relative to this script so it works from any folder
DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


class StorageError(Exception):
    """Raised when the tasks file cannot be read or written."""


def load_tasks(path=DEFAULT_PATH):
    """Load tasks from a JSON file.

    Args:
        path (Path or str): The file to read.

    Returns:
        list: The tasks in the file. Empty if the file does not exist yet.

    Raises:
        StorageError: If the file is unreadable or has invalid contents.
    """
    path = Path(path)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Task.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError, TypeError):
        raise StorageError(f"'{path}' is damaged or not a valid tasks file.")
    except OSError as error:
        raise StorageError(f"Could not read '{path}': {error}")


def save_tasks(tasks, path=DEFAULT_PATH):
    """Save tasks to a JSON file, creating the folder if needed.

    Args:
        tasks (list): The Task objects to save.
        path (Path or str): The file to write.

    Raises:
        StorageError: If the file cannot be written.
    """
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=2)
    except OSError as error:
        raise StorageError(f"Could not save to '{path}': {error}")