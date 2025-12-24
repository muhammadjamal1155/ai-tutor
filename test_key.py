import os
from dotenv import load_dotenv
import openai

load_dotenv(override=True)
key = os.getenv("OPENAI_API_KEY")

if not key:
    print("No key found!")
    exit(1)

print(f"Testing key: {key[:10]}...{key[-5:]}")

client = openai.OpenAI(api_key=key)

try:
    print("Attempting to list models...")
    client.models.list()
    print("SUCCESS: Key is valid and working!")
except Exception as e:
    print(f"FAILED: {e}")
