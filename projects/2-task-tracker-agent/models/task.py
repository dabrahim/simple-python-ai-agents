from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    title: str
    description: str
    done: bool = False
    id: Optional[int] = None
