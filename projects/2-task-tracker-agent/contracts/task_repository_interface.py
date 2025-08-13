from abc import ABC, abstractmethod
from typing import List

from models.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def create(self, task: Task) -> int:
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        pass

    @abstractmethod
    def mark_done(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Task:
        pass
