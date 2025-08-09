from src.contracts.communication_interface import CommunicationInterface
from src.contracts.logger_interface import LoggerInterface
from src.services.console_logger_service import ConsoleLoggerService


class ConsoleCommunicationService(CommunicationInterface):
    """
    Console-based implementation of user communication.
    Handles user interaction through standard input/output with proper formatting.
    """

    def __init__(self, logger: LoggerInterface = None):
        """
        Initialize with optional logger for consistent formatting.
        
        Args:
            logger: Logger service for formatted output (defaults to ConsoleLoggerService)
        """
        self.__logger = logger or ConsoleLoggerService()

    def ask_user(self, message: str) -> str:
        """
        Ask user for input via console with formatted prompt.
        
        Args:
            message: Question or prompt to show the user
            
        Returns:
            User's response from console input
        """
        self.__logger.log('Asking for clarification...', log_type='progress')
        response: str = input(f"\n❓ {message} \n\nResponse: ")
        return response

    def respond_to_user(self, message: str) -> None:
        """
        Display formatted response to user via console.
        
        Args:
            message: Final response message to display
        """
        self.__logger.log(message, log_type='agent_response')