# Project Explanation: To-Do List App

## Overview

This mini project is a command-line **To-Do List** application written in Python. It lets a user add tasks with a priority and an optional due date, view them, mark them complete, delete them, search them and see a summary. Tasks are saved to a JSON file, so they are still there the next time the program runs.

I chose it because it combines everything from the earlier tasks: conditionals and loops, functions, lists and dictionaries, file handling, error handling, classes and modules.

## Features

- Add a task with a title, priority (high, medium or low) and optional due date
- View all, pending or completed tasks
- Mark a task as complete
- Delete a task
- Search tasks by keyword
- Summary of total, completed, pending and overdue tasks
- Automatic saving after every change
- Input validation and friendly error messages

## Project Structure

```
python-todo-list-app/
├── README.md
├── .gitignore
├── src/
│   ├── main.py        # menu and user interaction
│   ├── models.py      # Task class and validation
│   ├── manager.py     # TaskManager class (the logic)
│   └── storage.py     # saving and loading JSON
├── tests/
│   └── test_manager.py
└── docs/
    ├── project_explanation.md
    └── screenshots/
```

## How it works

The program is split into four modules, each with one job. This is called **separation of concerns**.

- **`models.py`** defines the `Task` class (ID, title, priority, due date, completed) and validation functions. A task can mark itself complete, check whether it is overdue, and convert itself to and from a dictionary.
- **`manager.py`** defines `TaskManager`, which holds a list of `Task` objects and provides `add_task`, `complete_task`, `delete_task`, `list_tasks`, `search_tasks` and `stats`. It knows nothing about printing or input.
- **`storage.py`** saves the task list to `data/tasks.json` and loads it back. Each task becomes a dictionary, and the list of dictionaries is written as JSON.
- **`main.py`** shows the menu, reads the user's input, calls the manager and prints the results.

Because the logic is separate from the input and output, the manager and storage code can be tested without typing anything, which is what `tests/test_manager.py` does.

## Concepts used

| Concept | Where it appears |
|---|---|
| Conditionals (`if / elif / else`) | Menu choice, validation, filtering by status |
| Loops | The `while True` menu loop, `for` loops over tasks |
| Functions | One function per menu action, with docstrings |
| Lists | `TaskManager.tasks` is a list of `Task` objects |
| Dictionaries | `Task.to_dict()` and `Task.from_dict()`, and the `stats()` result |
| File handling | `open()` in read and write modes, JSON with `json.load` and `json.dump` |
| Error handling | `try / except` for bad input, missing tasks, damaged files; custom `TaskNotFoundError` and `StorageError` |
| OOP | `Task` and `TaskManager` classes with attributes, methods and `__str__` |
| Modules | Code split into four files imported by name |
| Standard library | `datetime` for dates, `json` for saving, `pathlib` for file paths |

## Error handling and edge cases

- Empty title, invalid priority, or a date that is not a real `YYYY-MM-DD` date is rejected with a clear message.
- Completing or deleting a task that does not exist gives "No task with ID ...", and completing a task twice is reported.
- A non-numeric task number is caught instead of crashing.
- An invalid menu choice is reported and the menu is shown again.
- If the tasks file does not exist yet, the app starts with an empty list. If it is damaged, the app shows a warning and starts empty instead of crashing.
- Saving problems are shown as warnings, so a write error cannot crash the program.

## Testing

`tests/test_manager.py` has 11 unit tests using Python's built-in `unittest`. They cover adding tasks, ID numbering, invalid input, completing, deleting, searching, overdue and summary counts, saving and loading, a missing file and a damaged file. Run them with:
```
python -m unittest discover tests
```

## Challenges and what I learned

- Deciding how to split the program into modules so each file has one clear job
- Converting objects to dictionaries and back so they could be stored as JSON
- Handling every kind of bad input without letting the program crash
- Writing tests so changes can be checked quickly

## Possible improvements

- Edit an existing task's title, priority or due date
- Sort tasks by priority or due date
- Recurring tasks and reminders
- A graphical or web interface