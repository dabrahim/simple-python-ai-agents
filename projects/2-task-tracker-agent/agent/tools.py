from pydantic import BaseModel
from typing import Any, Literal
from abc import ABC, abstractmethod
from models.task import Task
from repositories.local_file_task_repository import LocalFileTaskRepository


class BaseTool(ABC, BaseModel):
    @abstractmethod
    def execute(self) -> Any:
        pass


class CreateTasksArgs(BaseModel):
    title: str
    description: str


class CreateTask(BaseTool):
    name: Literal["create_task"]
    args: CreateTasksArgs

    def execute(self) -> Any:
        task: Task = Task(title=self.args.title, description=self.args.description)
        task_repo: LocalFileTaskRepository = LocalFileTaskRepository()

        # store the task
        task_id: int = task_repo.create(task)
        task.id = task_id

        return task


class MessageUser(BaseTool):
    name: Literal["message_user"]
    message: str

    def execute(self) -> Any:
        print(f"\n{self.message}")
        user_input = input(f"\nYou: ")
        return f"User input: {user_input}"

# Tool executor — tools need dependencies, how to handle them ? Since openai is parsing the tool object
