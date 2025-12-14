from abc import ABC, abstractmethod
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from typing import Dict

class BaseMemoryManager(ABC):
    """
    Abstract Base Class for Memory Management (Dependency Inversion Principle).
    The Agent will depend on this abstraction, not the concrete implementation.
    """
    @abstractmethod
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        pass

class InMemoryHistoryManager(BaseMemoryManager):
    """
    Concrete implementation of Memory Manager using in-memory storage.
    (Single Responsibility Principle: Handles ONLY storage retrieval).
    """
    def __init__(self):
        self.store: Dict[str, ChatMessageHistory] = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
