import os
from typing import List

IGNORE_LIST: List[str] = [".git", "vendor","__pycache__"]

def read_file_content(file_path: str) -> str:
    """
    Reads the content of a file and returns a formatted string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return format_file_content(content=content, file_name=file_path)
    except UnicodeDecodeError:
        print(f"Error reading {file_path}: UnicodeDecodeError")
        return ''
    except FileNotFoundError:
        print(f"Error reading {file_path}: File not found")
        return ''
    except Exception as e:
        print(f"Unexpected error reading {file_path}: {e}")
        return ''

def format_file_content(content: str, file_name: str) -> str:
    """
    Formats the content of a file with a header including the filename.
    """
    return f"=========\nFileName: {file_name}\nContent:\n{content}\n========="

def read_directory(directory_path: str) -> List[str]:
    """
    Recursively collects all file paths within a directory, excluding those in the IGNORE_LIST.
    """
    collected_files: List[str] = []
    try:
        for root, _, files in os.walk(directory_path):
            if not any(ignored in root for ignored in IGNORE_LIST):
                for file in files:
                    full_path = os.path.join(root, file)
                    collected_files.append(full_path)
    except OSError as e:
        print(f"Error accessing directory {directory_path}: {e}")
    return collected_files
