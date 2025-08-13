from dataclasses import dataclass
from enum import Enum, auto


class EventType(Enum):
    USER_MESSAGE = auto()
    ASSISTANT_MESSAGE = auto()
    TOOL_CALL = auto()
    TOOL_RESULT = auto()
    TOOL_ERROR = auto()
    SYSTEM_ERROR = auto()


@dataclass
class Event:
    type: EventType
    """
        types:
            - message
            - tool_call
            - tool_response
            - tool_error
    """
