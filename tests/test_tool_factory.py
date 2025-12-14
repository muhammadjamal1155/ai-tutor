
import unittest
from unittest.mock import MagicMock, patch
from src.agent.tools.tool_factory import ToolFactory
from langchain_core.tools import Tool

class TestToolFactory(unittest.TestCase):
    @patch("src.agent.tools.tool_factory.RAGPipeline")
    def test_create_tools(self, MockRAG):
        # Arrange
        mock_rag_instance = MockRAG.return_value
        mock_retriever = MagicMock()
        mock_rag_instance.get_retriever.return_value = mock_retriever
        
        factory = ToolFactory()
        
        # Act
        tools = factory.create_tools()
        
        # Assert
        self.assertEqual(len(tools), 1)
        self.assertIsInstance(tools[0], Tool)
        self.assertEqual(tools[0].name, "search_course_materials")
        
        # Verify retriever was retrieved
        mock_rag_instance.get_retriever.assert_called_once()

if __name__ == "__main__":
    unittest.main()
