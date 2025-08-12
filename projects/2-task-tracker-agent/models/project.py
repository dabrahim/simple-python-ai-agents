from dataclasses import dataclass
from typing import List
from .task import Task


@dataclass
class Project:
    title: str
    description: str
    tasks: List[Task]