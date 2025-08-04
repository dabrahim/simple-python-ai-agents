import json
import os
from typing import Dict, List


class ChatHistoryService:
    __DEFAULT_MEMORY_FOLDER: str = ".memory"
    __DEFAULT_CHAT_HISTORY_FILE_NAME: str = "chat-history.json"

    # Constructor
    def __init__(self) -> None:
        self.__memory_folder_path = os.getenv('MEMORY_FOLDER') or self.__DEFAULT_MEMORY_FOLDER

        # Create folder if it doesn't exist
        if not os.path.exists(self.__memory_folder_path):
            os.mkdir(self.__memory_folder_path)

        history_file_name: str = os.getenv('CHAT_HISTORY_FILE') or self.__DEFAULT_CHAT_HISTORY_FILE_NAME
        self.__chat_history_file_path = os.path.join(self.__memory_folder_path, history_file_name)

    def save_chat_history(self, chat_messages: List[Dict]) -> None:
        with open(self.__chat_history_file_path, "w") as chat_history_file:
            json.dump(chat_messages, chat_history_file)

    def load_chat_history(self) -> List[Dict]:
        if os.path.exists(self.__chat_history_file_path):
            with open(self.__chat_history_file_path, 'r') as f:
                chat_messages: List[Dict] = json.load(f)
                return chat_messages
        else:
            return []
