from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class EventType(Enum):
    SYSTEM_MESSAGE = auto()
    USER_MESSAGE = auto()
    ASSISTANT_MESSAGE = auto()
    TOOL_CALL = auto()
    TOOL_RESULT = auto()
    TOOL_ERROR = auto()
    SYSTEM_ERROR = auto()


@dataclass
class Event:
    type: EventType
    content: Any
