from abc import ABC, abstractmethod
from typing import Any, List, Dict


class ToolServiceContract(ABC):

    @abstractmethod
    def invoke(self, tool_name: str, tool_args: dict) -> Any:
        pass

    @abstractmethod
    def get_tools_definition(self) -> List[Dict]:
        pass
