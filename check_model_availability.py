import google.generativeai as genai
from src.config.settings import config
import os

genai.configure(api_key=config.GOOGLE_API_KEY)

desired_models = ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.0-pro", "gemini-1.5-flash"]

print("Checking specific models...")
try:
    available = [m.name for m in genai.list_models()]
    for d in desired_models:
        if d in available:
            print(f"FOUND: {d}")
        else:
            print(f"MISSING: {d}")
            
    # Print first 5 available just in case
    print("\nFirst 5 available models:")
    for m in available[:5]:
        print(m)

except Exception as e:
    print(f"Error: {e}")
