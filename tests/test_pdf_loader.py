
import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
from langchain_core.documents import Document
from src.loaders.pdf_loader import PDFLoader

class TestPDFLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data_dir"
        self.loader = PDFLoader(self.test_dir)

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("src.loaders.pdf_loader.PyMuPDFLoader")
    def test_load_documents_success(self, MockLoader, mock_listdir, mock_exists):
        # Setup mocks
        mock_exists.return_value = True
        mock_listdir.return_value = ["doc1.pdf", "doc2.pdf", "image.png"]
        
        # Mock loader instance and its load method
        mock_loader_instance = MockLoader.return_value
        mock_loader_instance.load.side_effect = [
            [Document(page_content="Content 1", metadata={"source": "doc1.pdf"})], # doc1 result
            [Document(page_content="Content 2", metadata={"source": "doc2.pdf"})]  # doc2 result
        ]

        # Act
        docs = self.loader.load_documents()

        # Assert
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0].page_content, "Content 1")
        self.assertEqual(docs[1].page_content, "Content 2")
        
        # Verify calls
        mock_listdir.assert_called_once_with(self.test_dir)
        self.assertEqual(MockLoader.call_count, 2)

    @patch("os.path.exists")
    def test_directory_not_found(self, mock_exists):
        mock_exists.return_value = False
        docs = self.loader.load_documents()
        self.assertEqual(docs, [])

    @patch("os.path.exists")
    @patch("os.listdir")
    def test_no_pdf_files(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["image.png", "notes.txt"]
        
        docs = self.loader.load_documents()
        self.assertEqual(docs, [])

    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("src.loaders.pdf_loader.PyMuPDFLoader")
    def test_loader_error_handling(self, MockLoader, mock_listdir, mock_exists):
        # Setup mocks to simulate one valid file and one broken file
        mock_exists.return_value = True
        mock_listdir.return_value = ["good.pdf", "bad.pdf"]
        
        # Configure MockLoader to succeed once then raise Exception
        mock_loader_instance = MockLoader.return_value
        
        # We need to simulate separate instances or side_effect on the class init if needed,
        # but here we are mocking the return value of the constructor.
        # To make specific instances behave differently, we can use side_effect on the method:
        mock_loader_instance.load.side_effect = [
            [Document(page_content="Good Content")], # good.pdf
            Exception("Corrupted file")              # bad.pdf
        ]

        docs = self.loader.load_documents()

        # Should retrieve the good one and skip the bad one
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].page_content, "Good Content")

if __name__ == "__main__":
    unittest.main()
