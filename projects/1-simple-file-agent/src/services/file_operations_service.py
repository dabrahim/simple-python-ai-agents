import os
from typing import List, Union


class FileOperationsService:
    """
    Service class dedicated to handling all file system operations.
    Returns standard Python types - agnostic to agent architecture.
    """

    @staticmethod
    def list_files(path: str) -> List[str]:
        """
        List all files and directories in the specified path.
        
        Args:
            path: Directory path to list contents from
            
        Returns:
            List of files with [DIR] markers for directories
            
        Raises:
            FileNotFoundError: If directory doesn't exist
            PermissionError: If no permission to access directory
        """
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
        """
        Read and return the complete contents of a file.
        
        Args:
            path: File path to read from
            
        Returns:
            File contents as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If no permission to read file
            UnicodeDecodeError: If file cannot be decoded as text
        """
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """
        Write content to a file, creating it if it doesn't exist or overwriting if it does.
        
        Args:
            path: File path to write to
            content: Content to write to the file
            
        Raises:
            PermissionError: If no permission to write to file/directory
            OSError: If other file system error occurs
        """
        # Create directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def append_to_file(path: str, content: str) -> None:
        """
        Append content to an existing file.
        
        Args:
            path: File path to append to
            content: Content to append to the file
            
        Raises:
            PermissionError: If no permission to write to file/directory
            OSError: If other file system error occurs
        """
        # Create directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def file_exists(path: str) -> bool:
        """
        Check if a file exists at the given path.
        
        Args:
            path: File path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return os.path.isfile(path)

    @staticmethod
    def directory_exists(path: str) -> bool:
        """
        Check if a directory exists at the given path.
        
        Args:
            path: Directory path to check
            
        Returns:
            True if directory exists, False otherwise
        """
        return os.path.isdir(path)

    @staticmethod
    def get_file_size(path: str) -> int:
        """
        Get the size of a file in bytes.
        
        Args:
            path: File path to check
            
        Returns:
            File size in bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
            OSError: If other file system error occurs
        """
        return os.path.getsize(path)