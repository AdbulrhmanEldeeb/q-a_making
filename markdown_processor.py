import os  # For handling file paths
from tqdm import tqdm  # For progress bar display
from logger import setup_logger  # Custom logger setup
from groq_api import initialize_client  # Importing Groq client initializer
from utils import chunk_text  # Function to split text into chunks
import time  # For sleep and time management

# Initialize the logger
logger = setup_logger()

def process_markdown_file(file_path):
    """
    Processes a Markdown file to generate actionable instructions and outputs using a Groq API client.
    
    Args:
        file_path (str): Path to the Markdown file to be processed.
    
    Returns:
        list: A list of dictionaries containing 'instruction' and 'output' for each processed text chunk.
    """
    try:
        # Initialize the Groq client and select the current model
        client, model_name = initialize_client()
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split the content into manageable chunks
        chunks = chunk_text(content)
        logger.info(f"Split {file_path} into {len(chunks)} chunks.")  # Log the number of chunks created
        
        output_data = []  # List to store results
        
        # Iterate through each chunk and process it
        for chunk_index, chunk in enumerate(tqdm(chunks, desc=f"Processing chunks in {os.path.basename(file_path)}")):
            while True:  # Retry loop for error handling
                try:
                    # Create a prompt using the chunk
                    prompt = f"""
                    Given the following context, generate an actionable instruction and output.
                    Context:
                    {chunk}

                    Instruction: [Generated instruction]
                    Output: [Generated output]
                    """
                    # Send the prompt to the Groq API
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_name,
                    )
                    
                    # Extract instruction and output from the response
                    result = response.choices[0].message.content
                    if "Instruction:" in result and "Output:" in result:
                        instruction = result.split("Instruction:")[1].split("Output:")[0].strip()
                        output = result.split("Output:")[1].strip()
                        output_data.append({"instruction": instruction, "output": output})  # Append to results
                        break  # Exit the retry loop if successful
                except Exception as e:
                    logger.error(f"Error processing chunk {chunk_index}: {e}")  # Log error details
                    if "429" in str(e):  # Handle rate-limiting errors
                        logger.info("Rotating API key and model.")
                        client, model_name = initialize_client()  # Rotate API key and model
                        time.sleep(3)  # Wait before retrying
                    else:
                        raise e  # Raise other exceptions
        
        return output_data  # Return the processed data
    except Exception as e:
        logger.error(f"Failed to process file {file_path}: {e}")  # Log any failures
        return []  # Return an empty list on failure
