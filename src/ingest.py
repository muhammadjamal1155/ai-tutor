from src.loaders.pdf_loader import PDFLoader
from src.rag.vector_store import RAGPipeline
from src.config.settings import config
import sys
import os

def ingest_data():
    """Full ingestion of all PDFs (used for initial setup)."""
    print("Starting data ingestion...")
    
    # 1. Load Documents
    loader = PDFLoader(config.RAW_PDFS_DIR)
    documents = loader.load_documents()
    
    if not documents:
        print("No documents found in raw_pdfs directory.")
        return

    print(f"Loaded {len(documents)} pages from PDFs.")

    # 2. Create/Update Index
    rag = RAGPipeline()
    rag.create_index(documents)
    
    print("Ingestion complete!")

def ingest_single_file(filepath: str):
    """Fast incremental ingestion of a single PDF file."""
    print(f"Starting incremental ingestion for: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    
    # 1. Load single document
    loader = PDFLoader(os.path.dirname(filepath))
    documents = loader.load_single_file(filepath)
    
    if not documents:
        print("Failed to load document.")
        return False

    print(f"Loaded {len(documents)} pages from {os.path.basename(filepath)}")

    # 2. Add to existing index
    rag = RAGPipeline()
    success = rag.add_documents(documents)
    
    print("Incremental ingestion complete!")
    return success

if __name__ == "__main__":
    ingest_data()
