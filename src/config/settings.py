from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DATA_DIR = os.path.join(os.getcwd(), "data")
    RAW_PDFS_DIR = os.path.join(DATA_DIR, "raw_pdfs")
    PROCESSED_TEXT_DIR = os.path.join(DATA_DIR, "processed_text")
    EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")
    
    # Model Config
    MODEL_NAME = "gemini-pro"
    EMBEDDING_MODEL = "models/text-embedding-004"

config = Config()

