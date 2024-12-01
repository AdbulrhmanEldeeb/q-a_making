import os
from tqdm import tqdm
from logger import setup_logger
from groq_api import initialize_client, get_next_key_and_model
from utils import chunk_text, save_json
import time 
logger = setup_logger()

def process_markdown_file(file_path):
    try:
        # Initialize Groq client
        client, model_name = initialize_client()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        chunks = chunk_text(content)
        logger.info(f"Split {file_path} into {len(chunks)} chunks.")
        output_data = []
        
        for chunk_index, chunk in enumerate(tqdm(chunks, desc=f"Processing chunks in {os.path.basename(file_path)}")):
            while True:
                try:
                    prompt = f"""
                    Given the following context, generate an actionable instruction and output.
                    Context:
                    {chunk}

                    Instruction: [Generated instruction]
                    Output: [Generated output]
                    """
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_name,
                    )
                    
                    result = response.choices[0].message.content
                    if "Instruction:" in result and "Output:" in result:
                        instruction = result.split("Instruction:")[1].split("Output:")[0].strip()
                        output = result.split("Output:")[1].strip()
                        output_data.append({"instruction": instruction, "output": output})
                        break
                except Exception as e:
                    logger.error(f"Error processing chunk {chunk_index}: {e}")
                    if "429" in str(e):
                        logger.info("Rotating API key and model.")
                        client, model_name = initialize_client()
                        time.sleep(3)
                    else:
                        raise e
        
        return output_data
    except Exception as e:
        logger.error(f"Failed to process file {file_path}: {e}")
        return []
