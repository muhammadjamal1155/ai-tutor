
import unittest
from unittest.mock import MagicMock, patch
import os
from langchain_core.documents import Document
from src.rag.vector_store import RAGPipeline

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.rag = RAGPipeline()

    @patch("src.rag.vector_store.FAISS")
    def test_create_index(self, MockFAISS):
        # Mock documents
        docs = [Document(page_content="Test content")]
        
        # Mock split_documents to return same docs
        self.rag.text_splitter.split_documents = MagicMock(return_value=docs)
        
        # Act
        self.rag.create_index(docs)
        
        # Assert - check if FAISS.from_documents was called
        MockFAISS.from_documents.assert_called_once()
        
        # Check if save_local was called on the instance returned by from_documents
        mock_vector_store = MockFAISS.from_documents.return_value
        mock_vector_store.save_local.assert_called_once()

    def test_create_index_empty(self):
        # Act
        self.rag.create_index([])
        
        # Assert - vector_store should still be None or unchanged from init
        self.assertIsNone(self.rag.vector_store)

    @patch("src.rag.vector_store.FAISS")
    @patch("os.path.exists")
    def test_load_index_success(self, mock_exists, MockFAISS):
        mock_exists.return_value = True
        
        # Act
        result = self.rag.load_index()
        
        # Assert
        self.assertTrue(result)
        MockFAISS.load_local.assert_called_once()

    @patch("os.path.exists")
    def test_load_index_failure(self, mock_exists):
        mock_exists.return_value = False
        
        # Act
        result = self.rag.load_index()
        
        # Assert
        self.assertFalse(result)

    @patch("src.rag.vector_store.FAISS")
    @patch("os.path.exists")
    def test_get_retriever_success(self, mock_exists, MockFAISS):
        # Setup - simulate index exists
        mock_exists.return_value = True
        
        # Act
        retriever = self.rag.get_retriever(k=5)
        
        # Assert
        MockFAISS.load_local.return_value.as_retriever.assert_called_with(search_kwargs={"k": 5})

    def test_get_retriever_no_index(self):
        # Ensure load_index fails
        self.rag.load_index = MagicMock(return_value=False)
        
        # Act & Assert
        with self.assertRaisesRegex(ValueError, "Index not found"):
            self.rag.get_retriever()

if __name__ == "__main__":
    unittest.main()
