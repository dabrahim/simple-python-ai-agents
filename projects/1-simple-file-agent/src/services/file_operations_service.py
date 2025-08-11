import os
from typing import List, Union


class FileOperationsService:
    """
    Service class dedicated to handling all file system operations.
    Returns standard Python types - agnostic to agent architecture.
    """

    @staticmethod
    def list_files(path: str) -> List[str]:
        """List files and directories in the specified path."""
        result = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path):
                result.append(f"[DIR] {name}")  # Mark directories
            else:
                result.append(f"     {name}")  # Plain files
        return result

    @staticmethod
    def read_file(path: str) -> str:
        """Read and return file contents as string."""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """Write content to file, creating directory if needed."""
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def append_to_file(path: str, content: str) -> None:
        """Append content to file, creating directory if needed."""
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def file_exists(path: str) -> bool:
        """Check if file exists at path."""
        return os.path.isfile(path)

    @staticmethod
    def directory_exists(path: str) -> bool:
        """Check if directory exists at path."""
        return os.path.isdir(path)

    @staticmethod
    def get_file_size(path: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(path)