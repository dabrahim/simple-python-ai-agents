from abc import ABC, abstractmethod


class CommunicationInterface(ABC):
    """
    Abstract interface for user communication methods.
    Allows different implementations for console, web, API, etc.
    """

    @abstractmethod
    def ask_user(self, message: str) -> str:
        """
        Request information from the user with a message.
        
        Args:
            message: Question or prompt to show the user
            
        Returns:
            User's response as string
        """
        pass

    @abstractmethod  
    def respond_to_user(self, message: str) -> None:
        """
        Display a response message to the user.
        
        Args:
            message: Final response message to display
        """
        pass