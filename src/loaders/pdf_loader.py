import os
from langchain_community.document_loaders import PyMuPDFLoader
from typing import List
from langchain_core.documents import Document

class PDFLoader:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    def load_documents(self) -> List[Document]:
        """Loads all PDFs from the specified directory."""
        documents = []
        if not os.path.exists(self.directory_path):
            print(f"Directory not found: {self.directory_path}")
            return []

        for filename in os.listdir(self.directory_path):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.directory_path, filename)
                print(f"Loading: {filename}")
                try:
                    loader = PyMuPDFLoader(file_path)
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        return documents

if __name__ == "__main__":
    # Test
    from src.config.settings import config
    loader = PDFLoader(config.RAW_PDFS_DIR)
    docs = loader.load_documents()
    print(f"Loaded {len(docs)} pages.")
