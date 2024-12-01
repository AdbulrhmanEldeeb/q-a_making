from groq import Groq
from config import GROQ_API_KEYS, GROQ_MODELS
import time

api_key_index = 0
model_index = 0

def get_next_key_and_model():
    global api_key_index, model_index
    api_key_index = (api_key_index + 1) % len(GROQ_API_KEYS)
    model_index = (model_index + 1) % len(GROQ_MODELS)
    return GROQ_API_KEYS[api_key_index], GROQ_MODELS[model_index]

def initialize_client():
    api_key, model_name = GROQ_API_KEYS[api_key_index], GROQ_MODELS[model_index]
    return Groq(api_key=api_key), model_name
