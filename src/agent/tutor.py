# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from src.config.settings import config
# from src.rag.vector_store import RAGPipeline
# from src.memory.memory_manager import BaseMemoryManager, InMemoryHistoryManager

# MOCK AGENT TO UNBLOCK UI DEVELOPMENT
class TutorAgent:
    def __init__(self, memory_manager=None):
        print("initializing Mock Tutor Agent...")

    def ask(self, question: str, session_id: str = "default_session"):
        """Ask a question to the AI Tutor (Mock)."""
        return f"MOCK RESPONSE: You said '{question}'. I am currently in maintenance mode while we build the UI, but I can still hear you!"

if __name__ == "__main__":
    tutor = TutorAgent()
    print(tutor.ask("Hello"))
