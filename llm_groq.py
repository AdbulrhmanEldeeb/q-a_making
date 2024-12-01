import os
import json
from tqdm import tqdm
from groq import Groq
from dotenv import load_dotenv
import logging
import time

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    filename="process_log.txt", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define multiple API keys and models for rotation
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

# Initialize global state for API key and model index
api_key_index = 0
model_index = 0

# Function to get the next API key and model
def get_next_key_and_model():
    global api_key_index, model_index
    api_key_index = (api_key_index + 1) % len(GROQ_API_KEYS)
    model_index = (model_index + 1) % len(GROQ_MODELS)
    return GROQ_API_KEYS[api_key_index], GROQ_MODELS[model_index]

# Initialize Groq client with the first API key
api_key, model_name = GROQ_API_KEYS[api_key_index], GROQ_MODELS[model_index]
client = Groq(api_key=api_key)

# Directory containing markdown files
markdown_dir = "./parsed_data"
markdown_files = [os.path.join(markdown_dir, f) for f in os.listdir(markdown_dir) if f.endswith(".md")]

# Log start of processing
logging.info("Processing started for markdown files.")

# Process each markdown file
for md_file in tqdm(markdown_files, desc="Processing Markdown Files"):
    output_data = []  # Reset for each file
    try:
        # Log the file being processed
        logging.info(f"Processing file: {md_file}")

        # Read the markdown file
        with open(md_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split content into chunks for processing
        chunks = [content[i:i + 1000] for i in range(0, len(content), 1000)]  # Chunk size: 1000 characters
        logging.info(f"File {md_file} split into {len(chunks)} chunks.")

        # Initialize a counter for tracking processed instruction-output pairs
        counter = 0

        # Process each chunk with the Groq API
        for chunk_index, chunk in enumerate(tqdm(chunks, desc=f"Processing chunks in {os.path.basename(md_file)}")):
            while True:  # Retry mechanism
                try:
                    # Prepare the instruction generation request
                    prompt = f"""
                    Given the following context, generate an actionable instruction relevant to the content and a clear, concise output.
                    The instruction should guide a task based on the context, and the output should demonstrate the result of that task.

                    Context:
                    {chunk}

                   
                    Now generate:
                    Instruction: [Your generated instruction]
                    Output: [Your generated output]
                    """


                    # Send request to Groq API
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_name,
                    )

                    # Extract the response content
                    response = chat_completion.choices[0].message.content

                    # Parse the response to extract instruction and output
                    if "Instruction:" in response and "Output:" in response:
                        instruction = response.split("Instruction:")[1].split("Output:")[0].strip()
                        output = response.split("Output:")[1].strip()

                        # Append the result to the dataset
                        output_data.append({"instruction": instruction, "output": output})
                        counter += 1

                        # Save the output data after every 50 instruction-output pairs
                        if counter % 50 == 0:
                            base_name = os.path.splitext(os.path.basename(md_file))[0]
                            output_json_file = f"processed/{base_name}_instruction_output_{counter}.json"
                            os.makedirs(os.path.dirname(output_json_file), exist_ok=True)  # Ensure output directory exists
                            with open(output_json_file, 'w', encoding='utf-8') as json_file:
                                json.dump(output_data, json_file, indent=4, ensure_ascii=False)
                            logging.info(f"Saved partial output to {output_json_file}.")
                            output_data = []  # Reset output data after saving

                        logging.info(f"Chunk {chunk_index + 1}/{len(chunks)} in {md_file} processed successfully.")
                        break  # Break out of retry loop
                    else:
                        logging.warning(f"Chunk {chunk_index + 1}/{len(chunks)} in {md_file} returned incomplete response.")
                        break

                except Exception as e:
                    logging.error(f"Failed to process chunk {chunk_index + 1} in {md_file}: {e}")

                    # Handle rate limiting or other errors by switching API key and model
                    if "429" in str(e) or "Too Many Requests" in str(e):
                        logging.warning("Rate limit reached. Rotating API key and model.")
                        api_key, model_name = get_next_key_and_model()
                        client = Groq(api_key=api_key)
                        time.sleep(3)  # Wait before retrying
                    else:
                        break

        # Save any remaining output data after processing all chunks
        if output_data:
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            output_json_file = f"processed/{base_name}_instruction_output_final.json"
            os.makedirs(os.path.dirname(output_json_file), exist_ok=True)  # Ensure output directory exists
            with open(output_json_file, 'w', encoding='utf-8') as json_file:
                json.dump(output_data, json_file, indent=4, ensure_ascii=False)
            logging.info(f"File {md_file} processed and saved to {output_json_file}.")

    except Exception as e:
        logging.error(f"Failed to process file {md_file}: {e}")

# Log completion
logging.info("Processing complete for all markdown files.")
print("Processing complete.")

