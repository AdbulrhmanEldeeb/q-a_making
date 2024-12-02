import os  # For file and directory operations
from tqdm import tqdm  # For displaying progress bars
from config import MARKDOWN_DIR, PROCESSED_DIR  # Directories for input and output files
from markdown_processor import process_markdown_file  # Function to process markdown files
from utils import save_json  # Utility function to save data as JSON
from logger import setup_logger  # Logger setup for consistent logging

# Initialize the logger
logger = setup_logger()

def main():
    """
    Main function to process all Markdown files in the specified directory.
    Processes the files, generates outputs, and saves them as JSON.
    """
    # Get a list of all Markdown files in the specified directory
    markdown_files = [
        os.path.join(MARKDOWN_DIR, f) 
        for f in os.listdir(MARKDOWN_DIR) if f.endswith(".md")
    ]

    logger.info("Processing started.")  # Log the start of processing

    # Iterate over all Markdown files with a progress bar
    for md_file in tqdm(markdown_files, desc="Processing Markdown Files"):
        # Process the current Markdown file
        output_data = process_markdown_file(md_file)
        
        if output_data:  # If processing is successful and output data is available
            # Get the base name of the file without extension
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            # Define the output path for the JSON file
            output_path = os.path.join(PROCESSED_DIR, f"{base_name}_output.json")
            # Save the processed data as JSON
            save_json(output_data, output_path)
            logger.info(f"Saved output to {output_path}")  # Log the saved output path

    logger.info("Processing completed.")  # Log the completion of processing

# Entry point of the script
if __name__ == "__main__":
    main()
