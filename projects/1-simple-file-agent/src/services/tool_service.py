from typing import List, Dict, Any

from src.contracts.tool_service_interface import ToolServiceInterface
from src.contracts.communication_interface import CommunicationInterface
from src.contracts.logger_interface import LoggerInterface
from src.models.tool_call_request import ToolCallRequest
from src.models.tool_call_response import ToolCallResult
from src.services.file_operations_service import FileOperationsService
from src.services.console_communication_service import ConsoleCommunicationService
from src.services.console_logger_service import ConsoleLoggerService
from src.services.memory_service import MemoryService


class AgentToolService(ToolServiceInterface):

    def __init__(self, communication_service: CommunicationInterface = None, logger: LoggerInterface = None) -> None:
        self.__file_service = FileOperationsService()
        self.__logger = logger or ConsoleLoggerService()
        self.__communication_service = communication_service or ConsoleCommunicationService(self.__logger)
        self.__memory_service = MemoryService(self.__logger)
        self.__tools_mapping: dict = {
            "list_files": self.__list_files,
            "read_file": self.__read_file,
            "write_file": self.__write_file,
            "append_to_file": self.__append_to_file,
            "ask_for_clarification": self.__ask_for_clarification,
            "submit_final_response": self.__submit_final_response,
            "update_memories": self.__save_user_preferences,
            "load_memories": self.__load_user_preferences
        }

    def invoke(self, tool_call: ToolCallRequest) -> ToolCallResult:
        tool_name: str = tool_call.tool_name
        tool_args: dict = tool_call.tool_arguments

        if tool_name not in self.__tools_mapping:
            raise Exception(f'Tool {tool_name} not found.')

        try:
            return self.__tools_mapping[tool_name](**tool_args)
        except TypeError as error:
            self.__logger.log_error(f"Tool call failed {tool_name}: {error}")
            raise Exception("Invalid tool arguments")

    def __list_files(self, path: str) -> ToolCallResult:
        try:
            result = self.__file_service.list_files(path)
            return ToolCallResult(content=result)
        except FileNotFoundError:
            return ToolCallResult(content=f"Error: Directory '{path}' not found")
        except PermissionError:
            return ToolCallResult(content=f"Error: Permission denied to access '{path}'")
        except Exception as e:
            return ToolCallResult(content=f"Error listing files: {str(e)}")

    def __read_file(self, path: str) -> ToolCallResult:
        try:
            content = self.__file_service.read_file(path)
            return ToolCallResult(content=content)
        except FileNotFoundError:
            return ToolCallResult(content=f"Error: File '{path}' not found")
        except PermissionError:
            return ToolCallResult(content=f"Error: Permission denied to read '{path}'")
        except UnicodeDecodeError:
            return ToolCallResult(
                content=f"Error: Cannot read '{path}' - file may be binary or use unsupported encoding")
        except Exception as e:
            return ToolCallResult(content=f"Error reading file: {str(e)}")

    def __write_file(self, path: str, content: str) -> ToolCallResult:
        try:
            self.__file_service.write_file(path, content)
            return ToolCallResult(content=f"Successfully wrote to '{path}'")
        except PermissionError:
            return ToolCallResult(content=f"Error: Permission denied to write to '{path}'")
        except Exception as e:
            return ToolCallResult(content=f"Error writing file: {str(e)}")

    def __append_to_file(self, path: str, content: str) -> ToolCallResult:
        try:
            self.__file_service.append_to_file(path, content)
            return ToolCallResult(content=f"Successfully appended to '{path}'")
        except PermissionError:
            return ToolCallResult(content=f"Error: Permission denied to write to '{path}'")
        except Exception as e:
            return ToolCallResult(content=f"Error appending to file: {str(e)}")

    def __ask_for_clarification(self, message: str) -> ToolCallResult:
        try:
            response = self.__communication_service.ask_user(message)
            return ToolCallResult(content=response)
        except Exception as e:
            return ToolCallResult(content=f"Error getting user input: {str(e)}")

    def __submit_final_response(self, message: str) -> ToolCallResult:
        try:
            self.__communication_service.respond_to_user(message)
            return ToolCallResult(exit_loop=True)
        except Exception as e:
            return ToolCallResult(content=f"Error displaying response: {str(e)}")

    def __save_user_preferences(self, memories: List[str]) -> ToolCallResult:
        """Save user preferences/memories using the memory service."""
        try:
            self.__memory_service.save_user_preferences(memories)
            return ToolCallResult(content=f"User preferences saved successfully. Total preferences: {len(memories)}")
        except Exception as e:
            return ToolCallResult(content=f"Error saving user preferences: {str(e)}")

    def __load_user_preferences(self) -> ToolCallResult:
        """Load user preferences/memories using the memory service."""
        try:
            preferences = self.__memory_service.load_user_preferences()
            return ToolCallResult(content=preferences)
        except Exception as e:
            return ToolCallResult(content=f"Error loading user preferences: {str(e)}")

    def get_tools_definition(self) -> List[Dict]:
        tools_definition: List[Dict] = [
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "Lists all the files inside a given folder.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "path to folder."
                            }
                        },
                        "required": ["path"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Reads and returns the content of a single file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "path to file."
                            }
                        },
                        "required": ["path"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Writes text to a file. If the file already exists, it will be overwritten. If it doesn't exist than it will be created.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "path to file."
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write inside the file."
                            }
                        },
                        "required": ["path", "content"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "append_to_file",
                    "description": "Appends new text to a file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "path to file."
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to append to the file."
                            }
                        },
                        "required": ["path", "content"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ask_for_clarification",
                    "description": "Used to send a message to the user and waits for his written input",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message to display to the user."
                            }
                        },
                        "required": ["message"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "submit_final_response",
                    "description": "Send the final response to the user without waiting for his written input",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Final response to to display to the user."
                            }
                        },
                        "required": ["message"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_memories",
                    "description": "COMPLETELY REPLACE all stored memories with new list. WARNING: This overwrites ALL existing memories. You must include existing memories you want to keep plus any new ones.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "memories": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "COMPLETE list of ALL memories to store (existing + new). This will replace everything previously stored."
                            }
                        },
                        "required": ["memories"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "load_memories",
                    "description": "Load previously saved user preferences and memories",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]

        return tools_definition
