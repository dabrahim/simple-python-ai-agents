from repositories.local_file_task_repository import LocalFileTaskRepository
from models.task import Task
from dataclasses import asdict
import json

task: Task = Task(
    title="Learn Python",
    description="Master the basics of the Python language"
)

repository: LocalFileTaskRepository = LocalFileTaskRepository()
task_id: int = repository.create(task)

tasks = repository.get_all()
print(json.dumps([asdict(task) for task in tasks], indent=4))