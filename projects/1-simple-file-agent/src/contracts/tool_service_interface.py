from abc import ABC, abstractmethod
from typing import Any, List, Dict

from src.models.tool_call_request import ToolCallRequest


class ToolServiceInterface(ABC):

    @abstractmethod
    def invoke(self, tool_call: ToolCallRequest) -> Any:
        pass

    @abstractmethod
    def get_tools_definition(self) -> List[Dict]:
        pass
