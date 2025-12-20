from dotenv import load_dotenv
import os
from pathlib import Path

# Get Project Root (3 levels up from src/config/settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"Loading .env from: {ENV_PATH}")
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Debug: Check if key is loaded
key = os.getenv("GOOGLE_API_KEY")

# Fallback: Check for common misnaming (OPENAI_API_KEY for Google Key)
if not key:
    openai_key_candidate = os.getenv("OPENAI_API_KEY")
    if openai_key_candidate and openai_key_candidate.startswith("AIza"):
        print("WARNING: Found 'OPENAI_API_KEY' that looks like a Google API Key. Using it as GOOGLE_API_KEY.")
        key = openai_key_candidate

if not key:
    print("CRITICAL WARNING: GOOGLE_API_KEY is still None after loading .env!")
    # Fallback: Manual read
    if ENV_PATH.exists():
        print("Attempting manual read of .env file...")
        with open(ENV_PATH, "r") as f:
            for line in f:
                # Check for Google Key
                if line.strip().startswith("GOOGLE_API_KEY="):
                    key = line.strip().split("=", 1)[1].strip('"').strip("'")
                    print("Key found via manual read (GOOGLE_API_KEY).")
                    break
                # Check for Misnamed Key
                elif line.strip().startswith("OPENAI_API_KEY=") and "AIza" in line:
                    key = line.strip().split("=", 1)[1].strip('"').strip("'")
                    print("Key found via manual read (Found OPENAI_API_KEY with Google format).")
                    break

if key:
    # Strip quotes just in case
    key = key.strip('"').strip("'")
    print(f"GOOGLE_API_KEY loaded successfully (starts with {key[:4]}...)")
else:
    print("ERROR: Could not find any suitable API Key.")

class Config:
    GOOGLE_API_KEY = key
    DATA_DIR = BASE_DIR / "data"
    RAW_PDFS_DIR = DATA_DIR / "raw_pdfs"
    PROCESSED_TEXT_DIR = DATA_DIR / "processed_text"
    EMBEDDINGS_DIR = DATA_DIR / "embeddings"
    
    # Model Config
    MODEL_NAME = "gemini-2.5-flash"  # Latest stable Gemini model
    EMBEDDING_MODEL = "models/text-embedding-004"

config = Config()

