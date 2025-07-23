import os
from typing import List, Dict


# def list_files(path: str) -> list:
#    directory = os.listdir(path)
#    return directory

def list_files(path: str) -> list:
    result = []
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            result.append(f"[DIR] {name}")  # Mark directories
        else:
            result.append(f"     {name}")  # Plain files
    return result


def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, 'w') as f:
        f.write(content)


def append_to_file(path: str, content: str) -> None:
    with open(path, 'a') as f:
        f.write(content)


def ask_for_clarification(message: str) -> str:
    return input(f"{message} \n")


def submit_final_response(message: str) -> None:
    print(message)


tools: List[Dict] = [
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
    }
]
