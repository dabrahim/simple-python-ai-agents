import json
import os
from typing import List, Dict, Any

from src.contracts.tools.tool_service_contract import ToolServiceContract
from src.models.tool_call_response import ToolCallResult


class AgentToolService(ToolServiceContract):

    def __init__(self) -> None:
        self.__tools_mapping: dict = {
            "list_files": self.__list_files,
            "read_file": self.__read_file,
            "write_file": self.__write_file,
            "append_to_file": self.__append_to_file,
            "ask_for_clarification": self.__ask_for_clarification,
            "submit_final_response": self.__submit_final_response,
            "update_memories": self.__update_memories,
            "load_memories": self.__load_memories
        }

    def invoke(self, tool_name: str, tool_args: dict) -> ToolCallResult:
        if tool_name not in self.__tools_mapping:
            raise Exception(f'Tool {tool_name} not found.')

        try:
            return self.__tools_mapping[tool_name](**tool_args)
        except TypeError as error:
            print(f"Tool call failed {tool_name}: {error}")
            raise Exception("Invalid tool arguments")

    @staticmethod
    def __list_files(path: str) -> ToolCallResult:
        result = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path):
                result.append(f"[DIR] {name}")  # Mark directories
            else:
                result.append(f"     {name}")  # Plain files
        return ToolCallResult(content=result)

    @staticmethod
    def __read_file(path: str) -> ToolCallResult:
        with open(path, 'r') as f:
            return ToolCallResult(content=f.read())

    @staticmethod
    def __write_file(path: str, content: str) -> ToolCallResult:
        with open(path, 'w') as f:
            f.write(content)
        return ToolCallResult(exit_loop=False)

    @staticmethod
    def __append_to_file(path: str, content: str) -> ToolCallResult:
        with open(path, 'a') as f:
            f.write(content)
        return ToolCallResult(exit_loop=False)

    @staticmethod
    def __ask_for_clarification(message: str) -> ToolCallResult:
        print(f"\n{'*' * 20}")
        print('Asking for clarification...\n')
        response: str = input(f"{message} \n\nResponse: ")
        return ToolCallResult(content=response)

    @staticmethod
    def __submit_final_response(message: str) -> ToolCallResult:
        print(f"\n{'*' * 20}")
        print("AGENT RESPONSE\n")
        print(message)
        print(f"{'*' * 20}")

        # should_continue = input("\nDo you need help with something else?\nAnswer (y/n)>> ")
        # if should_continue.lower() in ("y", "yes"):
        #    follow_up_message: str = input("\nHow can I help you?\nYou>> ")
        #    return follow_up_message, True
        # else:
        #    return None, False
        return ToolCallResult(exit_loop=True)

    @staticmethod
    def __update_memories(memories: List[str]) -> ToolCallResult:
        memory_folder: str = ".memory"
        memory_file: str = ".memory/preferences.json"
        
        # Create memory folder if it doesn't exist
        if not os.path.exists(memory_folder):
            os.makedirs(memory_folder)
            
        with open(memory_file, 'w') as f:
            json.dump(memories, f, indent=2)
        return ToolCallResult(content="Memories updated successfully")

    @staticmethod
    def __load_memories() -> ToolCallResult:
        memory_file: str = ".memory/preferences.json"
        if os.path.exists(memory_file):
            with open(memory_file, 'r') as f:
                memories = json.load(f)
                return ToolCallResult(content=memories)
        else:
            return ToolCallResult(content=[])

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
