from abc import ABC, abstractmethod
from typing import Dict, Any


class LoggerInterface(ABC):
    """
    Specialized logging interface for AI agent interactions.
    Provides dedicated methods for each specific agent logging scenario.
    """

    @abstractmethod
    def log_tool_call(self, tool_name: str, tool_args: Dict[str, Any] = None) -> None:
        """Log when a tool is being called."""
        pass

    @abstractmethod
    def log_tool_result(self, content: Any) -> None:
        """Log the result of a tool call."""
        pass

    @abstractmethod
    def log_agent_response(self, message: str) -> None:
        """Log the final response from the agent to the user."""
        pass

    @abstractmethod
    def log_progress(self, message: str) -> None:
        """Log progress updates or status information."""
        pass

    @abstractmethod
    def log_error(self, message: str) -> None:
        """Log error messages."""
        pass

    @abstractmethod
    def log_user_prompt(self, message: str) -> None:
        """Log user interaction prompts."""
        pass