from groq import Groq  # Import the Groq library for API interaction
from config import GROQ_API_KEYS, GROQ_MODELS  # Import API keys and model names from the configuration

# Initialize indices to keep track of the current API key and model
api_key_index = 0
model_index = 0

def get_next_key_and_model():
    """
    Rotate through the list of API keys and models in a round-robin fashion.
    
    This function updates the indices for the API keys and models to ensure
    that subsequent calls use the next key and model in the list.
    
    Returns:
        tuple: The next API key and model name to use.
    """
    global api_key_index, model_index  # Declare global variables for modification
    api_key_index = (api_key_index + 1) % len(GROQ_API_KEYS)  # Cycle through API keys
    model_index = (model_index + 1) % len(GROQ_MODELS)  # Cycle through model names
    return GROQ_API_KEYS[api_key_index], GROQ_MODELS[model_index]  # Return the current key and model

def initialize_client():
    """
    Initialize the Groq client with the current API key and model.
    
    This function creates a Groq client instance using the current API key and model,
    allowing interactions with the API using the specified credentials and settings.
    
    Returns:
        tuple: The initialized Groq client and the model name.
    """
    # Get the current API key and model name
    api_key, model_name = GROQ_API_KEYS[api_key_index], GROQ_MODELS[model_index]
    return Groq(api_key=api_key), model_name  # Return the initialized client and model name
