import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEYS = [
    os.getenv('GROQ_API_KEY_1'),
    os.getenv('GROQ_API_KEY_2'),
    os.getenv('GROQ_API_KEY_3'),
]

GROQ_MODELS = [
    'llama3-groq-70b-8192-tool-use-preview',
    'llama3-groq-8b-8192-tool-use-preview',
    'llama-3.2-3b-preview',
    'llama3-70b-8192',
    'llama3-8b-8192',
    'mixtral-8x7b-32768',
]

MARKDOWN_DIR = "./parsed_data"
PROCESSED_DIR = "./processed"
