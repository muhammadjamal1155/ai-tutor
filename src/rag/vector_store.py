from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from src.config.settings import config
import os

class RAGPipeline:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        self.vector_store_path = str(config.EMBEDDINGS_DIR / "faiss_index")
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

    def add_documents(self, documents: List[Document]):
        """Add new documents to existing index (incremental update)."""
        if not documents:
            print("No documents to add.")
            return False

        print("Splitting new documents...")
        splits = self.text_splitter.split_documents(documents)
        
        # Load existing index
        if not self.vector_store:
            loaded = self.load_index()
            if not loaded:
                # No existing index, create new one
                print("No existing index, creating new...")
                self.vector_store = FAISS.from_documents(documents=splits, embedding=self.embeddings)
            else:
                print(f"Adding {len(splits)} new chunks to existing index...")
                self.vector_store.add_documents(splits)
        else:
            print(f"Adding {len(splits)} new chunks to existing index...")
            self.vector_store.add_documents(splits)
        
        print("Saving updated index...")
        self.vector_store.save_local(self.vector_store_path)
        print("Index updated successfully.")
        return True

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

    def get_retriever(self, k=8):
        if not self.vector_store:
            loaded = self.load_index()
            if not loaded:
                raise ValueError("Index not found. Please run ingestion first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})
