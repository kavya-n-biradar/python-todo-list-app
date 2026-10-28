# To-Do List App (Python Mini Project)

A command-line To-Do List application built for the CodeMore Python Programming Internship (Week 4, Task 2). It saves tasks to a JSON file and uses the concepts learned across the earlier tasks.

## Features

- Add tasks with a priority (high, medium, low) and an optional due date
- View all, pending or completed tasks
- Mark tasks as complete and delete tasks
- Search tasks by keyword
- Summary of total, completed, pending and overdue tasks
- Tasks are saved automatically and loaded when the program starts
- Input validation and error handling

## Project Structure

```
python-todo-list-app/
├── README.md
├── .gitignore
├── src/
│   ├── main.py        # menu and user interaction
│   ├── models.py      # Task class and validation
│   ├── manager.py     # TaskManager class
│   └── storage.py     # saving and loading JSON
├── tests/
│   └── test_manager.py
└── docs/
    ├── project_explanation.md
    └── screenshots/
```

## Requirements

- Python 3.8 or newer. No external libraries.

## Setup and How to Run

```bash
git clone https://github.com/kavya-n-biradar/python-todo-list-app.git
cd python-todo-list-app
python src/main.py
```

Tasks are stored in `data/tasks.json`, which is created automatically the first time you add a task.

## Run the Tests

```bash
python -m unittest discover tests
```

## Sample Session

```
Choose an option (1-9): 1
Task title: Submit internship report
Priority (high/medium/low) [medium]: high
Due date YYYY-MM-DD (optional): 2030-11-30
Added: [ ] #1 Submit internship report (high) - due 2030-11-30

Choose an option (1-9): 5
Task number to complete: 1
Completed: [x] #1 Submit internship report (high) - due 2030-11-30

Choose an option (1-9): 8
Total: 1 | Completed: 1 | Pending: 0 | Overdue: 0
```

## Concepts Used

| Concept | Where |
|---|---|
| Conditionals and loops | Menu loop and filtering |
| Functions | One function per menu action |
| Lists and dictionaries | Task list; tasks saved as dictionaries |
| File handling | JSON saving and loading |
| Error handling | Invalid input, missing tasks, damaged files |
| OOP | `Task` and `TaskManager` classes |
| Modules | Code split into `models`, `manager`, `storage` and `main` |

A fuller explanation is in [`docs/project_explanation.md`](docs/project_explanation.md).

## Screenshots

Full screenshots are in [`docs/screenshots/`](docs/screenshots/):
- `add_tasks.png`: adding tasks
- `invalid_input.png`: invalid input handled
- `view_and_complete.png`: completing and viewing tasks
- `search_summary_delete.png`: search, summary and delete
- `persistence_after_restart.png`: tasks still there after restarting
- `tasks_json_file.png`: the saved JSON file
- `unit_tests_pass.png`: all unit tests passing

## What I Learned

- How to combine functions, classes, files and error handling in one program
- How to split a program into modules with a single job each
- How to save and load data with JSON
- How to validate user input and keep a program from crashing
- How to write unit tests and document a project

## Author

Kavya Biradar