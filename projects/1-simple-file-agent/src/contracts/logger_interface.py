from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    """
    Simple logging interface for displaying well-formatted messages.
    Keeps logging unified and easily replaceable across the project.
    """

    @abstractmethod
    def log(self, message: str, **kwargs) -> None:
        """
        Display a well-formatted, easy-to-read message.
        
        Args:
            message: The message to log/display
            **kwargs: Additional formatting options (implementation-specific)
        """
        pass