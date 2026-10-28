"""Unit tests for the To-Do List app. Run: python -m unittest discover tests"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from manager import TaskManager, TaskNotFoundError  # noqa: E402
from storage import StorageError, load_tasks, save_tasks  # noqa: E402


class TestTaskManager(unittest.TestCase):
    """Tests for TaskManager."""

    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        task = self.manager.add_task("Buy milk", "HIGH", "2030-01-05")
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.due_date, "2030-01-05")

    def test_ids_increase(self):
        self.manager.add_task("A")
        second = self.manager.add_task("B")
        self.assertEqual(second.task_id, 2)

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("   ")
        with self.assertRaises(ValueError):
            self.manager.add_task("A", "urgent")
        with self.assertRaises(ValueError):
            self.manager.add_task("A", "low", "31-12-2026")
        with self.assertRaises(ValueError):
            self.manager.add_task("A", "low", "2026-02-30")

    def test_complete_task(self):
        self.manager.add_task("A")
        self.manager.complete_task(1)
        self.assertEqual(len(self.manager.list_tasks("completed")), 1)
        with self.assertRaises(ValueError):
            self.manager.complete_task(1)

    def test_missing_task(self):
        with self.assertRaises(TaskNotFoundError):
            self.manager.complete_task(99)
        with self.assertRaises(TaskNotFoundError):
            self.manager.delete_task(99)

    def test_delete_task(self):
        self.manager.add_task("A")
        self.manager.delete_task(1)
        self.assertEqual(self.manager.list_tasks(), [])

    def test_search(self):
        self.manager.add_task("Buy milk")
        self.manager.add_task("Call mom")
        self.assertEqual(len(self.manager.search_tasks("BUY")), 1)
        self.assertEqual(self.manager.search_tasks(""), [])

    def test_stats_and_overdue(self):
        self.manager.add_task("Old", "low", "2000-01-01")
        self.manager.add_task("Done", "low")
        self.manager.complete_task(2)
        stats = self.manager.stats()
        self.assertEqual(stats, {"total": 2, "completed": 1,
                                 "pending": 1, "overdue": 1})


class TestStorage(unittest.TestCase):
    """Tests for saving and loading."""

    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data" / "tasks.json"
            manager = TaskManager()
            manager.add_task("Save me", "high", "2030-05-01")
            save_tasks(manager.tasks, path)
            loaded = load_tasks(path)
            self.assertEqual(loaded[0].title, "Save me")
            self.assertEqual(loaded[0].due_date, "2030-05-01")

    def test_missing_file_gives_empty_list(self):
        self.assertEqual(load_tasks("no_such_folder/none.json"), [])

    def test_corrupt_file_raises(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"
            path.write_text("{not valid json", encoding="utf-8")
            with self.assertRaises(StorageError):
                load_tasks(path)


if __name__ == "__main__":
    unittest.main()