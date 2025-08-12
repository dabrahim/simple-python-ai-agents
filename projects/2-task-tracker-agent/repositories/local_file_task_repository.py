from typing import List
from pathlib import Path
import json

from contracts.TaskRepositoryInterface import TaskRepository
from models.task import Task
from config import TASKS_FILE_PATH


class LocalFileTaskRepository(TaskRepository):

    def __init__(self) -> None:
        self._tasks_file_path: Path = TASKS_FILE_PATH

    def create(self, task: Task) -> int:
        tasks = self._load_tasks()

        # Generate new ID (max existing ID + 1, or 1 if no tasks)
        new_id = max([t.id for t in tasks], default=0) + 1
        task.id = new_id

        tasks.append(task)
        self._save_tasks(tasks)

        return new_id

    def update(self, task: Task) -> None:
        pass

    def mark_done(self, task: Task) -> None:
        pass

    def get_all(self) -> List[Task]:
        return self._load_tasks()

    def _load_tasks(self) -> List[Task]:
        if not self._tasks_file_path.exists():
            return []

        with open(self._tasks_file_path, 'r') as file:
            data = json.load(file)
            return [Task(**task_data) for task_data in data]

    def _save_tasks(self, tasks: List[Task]) -> None:
        with open(self._tasks_file_path, 'w') as file:
            task_dicts = [task.__dict__ for task in tasks]
            json.dump(task_dicts, file, indent=2)
