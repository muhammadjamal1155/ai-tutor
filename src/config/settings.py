from dotenv import load_dotenv
import os
from pathlib import Path

# Get Project Root (3 levels up from src/config/settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"Loading .env from: {ENV_PATH}")
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Debug: Check if key is loaded
key = os.getenv("OPENAI_API_KEY")

if not key:
    print("CRITICAL WARNING: OPENAI_API_KEY is still None after loading .env!")
    # Fallback: Manual read
    if ENV_PATH.exists():
        print("Attempting manual read of .env file...")
        with open(ENV_PATH, "r") as f:
            for line in f:
                if line.strip().startswith("OPENAI_API_KEY="):
                    key = line.strip().split("=", 1)[1].strip('"').strip("'")
                    print("Key found via manual read (OPENAI_API_KEY).")
                    break

if key:
    # Strip quotes just in case
    key = key.strip('"').strip("'")
    print(f"OPENAI_API_KEY loaded successfully (starts with {key[:4]}...)")
else:
    print("ERROR: Could not find OPENAI_API_KEY.")

class Config:
    OPENAI_API_KEY = key
    DATA_DIR = BASE_DIR / "data"
    RAW_PDFS_DIR = DATA_DIR / "raw_pdfs"
    PROCESSED_TEXT_DIR = DATA_DIR / "processed_text"
    EMBEDDINGS_DIR = DATA_DIR / "embeddings"
    
    # Model Config
    MODEL_NAME = "gpt-4o-mini"
    EMBEDDING_MODEL = "text-embedding-3-small"

config = Config()

