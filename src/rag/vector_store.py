from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from src.config.settings import config
import os

class RAGPipeline:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        self.vector_store_path = os.path.join(config.EMBEDDINGS_DIR, "faiss_index")
        self.vector_store = None

    def create_index(self, documents: List[Document]):
        """Creates and saves the vector store index."""
        if not documents:
            print("No documents to index.")
            return

        print("Splitting documents...")
        splits = self.text_splitter.split_documents(documents)
        
        print(f"Creating vector store with {len(splits)} chunks...")
        self.vector_store = FAISS.from_documents(documents=splits, embedding=self.embeddings)
        
        print("Saving vector store...")
        self.vector_store.save_local(self.vector_store_path)
        print("Index saved successfully.")

    def load_index(self):
        """Loads the existing vector store index."""
        if os.path.exists(self.vector_store_path):
            self.vector_store = FAISS.load_local(
                self.vector_store_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True # Local file safe
            )
            return True
        return False

    def get_retriever(self, k=4):
        if not self.vector_store:
            loaded = self.load_index()
            if not loaded:
                raise ValueError("Index not found. Please run ingestion first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})
