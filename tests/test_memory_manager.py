
import unittest
from langchain_community.chat_message_histories import ChatMessageHistory
from src.memory.memory_manager import InMemoryHistoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = InMemoryHistoryManager()

    def test_get_session_history_creates_new(self):
        # Act
        history = self.manager.get_session_history("user_1")
        
        # Assert
        self.assertIsInstance(history, ChatMessageHistory)
        self.assertEqual(len(history.messages), 0)

    def test_get_session_history_retrieves_existing(self):
        # Arrange
        history1 = self.manager.get_session_history("user_1")
        history1.add_user_message("Hello")
        
        # Act
        history2 = self.manager.get_session_history("user_1")
        
        # Assert
        self.assertEqual(len(history2.messages), 1)
        self.assertEqual(history2.messages[0].content, "Hello")
        self.assertIs(history1, history2) # Should be same object reference

    def test_separate_sessions(self):
        # Arrange
        self.manager.get_session_history("user_1").add_user_message("Hi User 1")
        self.manager.get_session_history("user_2").add_user_message("Hi User 2")
        
        # Act
        hist1 = self.manager.get_session_history("user_1")
        hist2 = self.manager.get_session_history("user_2")
        
        # Assert
        self.assertEqual(hist1.messages[0].content, "Hi User 1")
        self.assertEqual(hist2.messages[0].content, "Hi User 2")

if __name__ == "__main__":
    unittest.main()
