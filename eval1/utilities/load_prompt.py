import os

def load_prompt(file_name):
    """Load the content of a specified file from the 'config' directory.

    This function reads the file content from a path constructed from the base
    directory and the provided filename. 

    Args:
        file_name (str): The name of the file to load.

    Returns:
        str: The content of the file or a placeholder string.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'templates', file_name)

    with open(file_path, 'r') as file:
        return file.read()
