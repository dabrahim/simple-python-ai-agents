from src.contracts.communication_interface import CommunicationInterface
from src.contracts.logger_interface import LoggerInterface
from src.services.console_logger_service import ConsoleLoggerService


class ConsoleCommunicationService(CommunicationInterface):
    """
    Console-based implementation of user communication.
    Handles user interaction through standard input/output with proper formatting.
    """

    def __init__(self, logger: LoggerInterface = None):
        self.__logger = logger or ConsoleLoggerService()

    def ask_user(self, message: str) -> str:
        """Ask user for input via console."""
        self.__logger.log_progress('Asking for clarification...')
        response: str = input(f"\n❓ {message} \n\nResponse: ")
        return response

    def respond_to_user(self, message: str) -> None:
        """Display response to user via console."""
        self.__logger.log_agent_response(message)