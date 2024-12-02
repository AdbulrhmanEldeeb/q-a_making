# Markdown File Processor

This project processes Markdown files, extracts and processes their content, and saves the results as JSON files. It is designed to handle large-scale Markdown content efficiently, leveraging modular code structure, logging, and progress tracking.

## Features

- **Markdown Processing**: Extracts and processes content from Markdown files using a custom processing pipeline.
- **Chunking Support**: Splits large text into manageable chunks for better handling.
- **Error Handling**: Automatically retries with rotated API keys in case of rate limits or errors.
- **JSON Output**: Saves processed data as structured JSON files for downstream use.
- **Progress Tracking**: Displays a progress bar to monitor file processing status.
- **Logging**: Provides detailed logs for tracking the progress and diagnosing errors.

## Directory Structure

```plaintext
project/
├── config.py              # Configuration for file paths and other settings
├── logger.py              # Logger setup for consistent logging
├── markdown_processor.py  # Handles Markdown file processing logic
├── utils.py               # Utility functions (e.g., chunking, saving JSON)
├── main.py                # Entry point for the script
├── MARKDOWN_DIR/          # Input directory for Markdown files
└── PROCESSED_DIR/         # Output directory for JSON files
```

### Setup
Clone the repository:

```bash
git clone https://github.com/AdbulrhmanEldeeb/q-a_making
cd q-a_making/
```
### Install required dependencies:

```bash

pip install -r requirements.txt
Configure the project by updating paths in config.py:
```

```python
MARKDOWN_DIR = "parsed_data/"
PROCESSED_DIR = "processed/"
```

### Usage
Place the Markdown files to be processed in the MARKDOWN_DIR.

Run the script:

```bash
python main.py
The processed data will be saved in the PROCESSED_DIR as JSON files.
```



Example
Input Markdown file:

```markdown
# Sample Markdown

This is an example of content to be processed.
```
Output JSON file:


```json
[
    {
        "instruction": "Generate an actionable instruction for processing.",
        "output": "Extract key points from the markdown content."
    }
]
```
Logging
Logs are saved to track processing progress and errors. Configure the logger in logger.py for your requirements.