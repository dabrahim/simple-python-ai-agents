import json
import os
from typing import Dict, List
from src.services.file_operations_service import FileOperationsService
from src.contracts.logger_interface import LoggerInterface
from src.services.console_logger_service import ConsoleLoggerService


class MemoryService:
    """
    Comprehensive memory service handling both user preferences and chat history.
    Uses FileOperationsService for all file system operations.
    """

    __DEFAULT_MEMORY_FOLDER: str = ".memory"
    __DEFAULT_CHAT_HISTORY_FILE_NAME: str = "chat-history.json"
    __DEFAULT_PREFERENCES_FILE_NAME: str = "preferences.json"

    def __init__(self, logger: LoggerInterface | None = None) -> None:
        self.__file_service = FileOperationsService()
        self.__logger = logger or ConsoleLoggerService()
        self.__memory_folder_path = os.getenv('MEMORY_FOLDER') or self.__DEFAULT_MEMORY_FOLDER

        history_file_name: str = os.getenv('CHAT_HISTORY_FILE') or self.__DEFAULT_CHAT_HISTORY_FILE_NAME
        preferences_file_name: str = os.getenv('PREFERENCES_FILE') or self.__DEFAULT_PREFERENCES_FILE_NAME

        self.__chat_history_file_path = os.path.join(self.__memory_folder_path, history_file_name)
        self.__preferences_file_path = os.path.join(self.__memory_folder_path, preferences_file_name)

    def save_chat_history(self, chat_messages: List[Dict]) -> None:
        """Save conversation history to file."""
        try:
            history_content = json.dumps(chat_messages, indent=2)
            self.__file_service.write_file(self.__chat_history_file_path, history_content)
        except Exception as e:
            self.__logger.log_error(f"Failed to save chat history: {e}")

    def load_chat_history(self) -> List[Dict]:
        """Load conversation history from file."""
        try:
            if self.__file_service.file_exists(self.__chat_history_file_path):
                content = self.__file_service.read_file(self.__chat_history_file_path)
                return json.loads(content)
            else:
                return []
        except (json.JSONDecodeError, Exception) as e:
            self.__logger.log_error(f"Failed to load chat history: {e}")
            return []

    def save_user_preferences(self, preferences: List[str]) -> None:
        """Save user preferences/memories to file. Completely replaces existing preferences."""
        try:
            preferences_content = json.dumps(preferences, indent=2)
            self.__file_service.write_file(self.__preferences_file_path, preferences_content)
        except Exception as e:
            raise Exception(f"Failed to save user preferences: {e}")

    def load_user_preferences(self) -> List[str]:
        """Load user preferences/memories from file. Returns empty list if no preferences exist."""
        try:
            if self.__file_service.file_exists(self.__preferences_file_path):
                content = self.__file_service.read_file(self.__preferences_file_path)
                return json.loads(content)
            else:
                return []
        except json.JSONDecodeError as e:
            raise Exception(f"User preferences file contains invalid JSON: {e}")
        except Exception as e:
            raise Exception(f"Failed to load user preferences: {e}")
