import os  # For handling file system operations
import json  # For working with JSON data

def chunk_text(text, chunk_size=1000):
    """
    Splits a given text into smaller chunks of a specified size.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): The size of each chunk. Defaults to 1000 characters.

    Returns:
        list: A list of text chunks.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def save_json(data, file_path):
    """
    Saves data as a JSON file at the specified file path.

    Args:
        data (dict or list): The data to be saved.
        file_path (str): The path where the JSON file will be saved.

    Behavior:
        - Creates any necessary parent directories if they do not exist.
        - Writes the JSON data with an indentation of 4 for readability.
        - Ensures non-ASCII characters are preserved in their original form.
    """
    # Create parent directories if they do not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save data to a JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
