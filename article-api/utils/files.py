import os
from typing import List


def get_paths_from_dir(directory: str) -> List[str]:
    """
    Get a list of file paths from a directory inside the _path_ directory.

    Args:
    - directory (str): The directory to search for files.

    Returns:
    - List[str]: A list of file paths.
    """

    file_paths = []

    for dir_path, _, file_names in os.walk("_data_/" + directory):
        for file_name in file_names:
            if file_name.endswith(".pdf"):
                file_paths.append(dir_path + "/" + file_name)

    return file_paths


def get_folders_from_dir(directory: str) -> List[str]:
    """
    Get a list of folder paths from a directory inside the _path_ directory.

    Args:
    - directory (str): The directory to search for folders.

    Returns:
    - List[str]: A list of folder paths.
    """
    return os.listdir("_data_/" + directory)
