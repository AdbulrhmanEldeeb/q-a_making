import os
from tqdm import tqdm
from config import MARKDOWN_DIR, PROCESSED_DIR
from markdown_processor import process_markdown_file
from utils import save_json
from logger import setup_logger

logger = setup_logger()

def main():
    markdown_files = [
        os.path.join(MARKDOWN_DIR, f) 
        for f in os.listdir(MARKDOWN_DIR) if f.endswith(".md")
    ]

    logger.info("Processing started.")
    
    for md_file in tqdm(markdown_files, desc="Processing Markdown Files"):
        output_data = process_markdown_file(md_file)
        if output_data:
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            output_path = os.path.join(PROCESSED_DIR, f"{base_name}_output.json")
            save_json(output_data, output_path)
            logger.info(f"Saved output to {output_path}")

    logger.info("Processing completed.")

if __name__ == "__main__":
    main()
