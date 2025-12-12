from src.loaders.pdf_loader import PDFLoader
from src.rag.vector_store import RAGPipeline
from src.config.settings import config
import sys

def ingest_data():
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

if __name__ == "__main__":
    ingest_data()
