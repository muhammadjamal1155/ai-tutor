from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.config.settings import config
from src.rag.vector_store import RAGPipeline
from src.memory.memory_manager import BaseMemoryManager, InMemoryHistoryManager

class TutorAgent:
    def __init__(self, memory_manager: BaseMemoryManager = None):
        self.llm = ChatGoogleGenerativeAI(model=config.MODEL_NAME, temperature=0.3)
        self.rag = RAGPipeline()
        self.retriever = self.rag.get_retriever()
        
        # Dependency Injection (DIP)
        self.memory_manager = memory_manager or InMemoryHistoryManager()
        
        # System Prompt with History
        system_prompt = (
            "You are an expert AI Tutor designed to help students understand complex topics. "
            "Use the following pieces of retrieved context to answer the question. "
            "If the answer is not in the context, say that you don't have that information in your notes. "
            "Keep your answer simple, clear, and focused on the student's question."
            "\n\n"
            "{context}"
        )
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"), # Memory slot
                ("human", "{input}"),
            ]
        )
        
        # Create Chains
        question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)
        
        # Wrap with Message History
        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.memory_manager.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def ask(self, question: str, session_id: str = "default_session"):
        """Ask a question to the AI Tutor with memory."""
        response = self.conversational_rag_chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )
        return response["answer"]

if __name__ == "__main__":
    tutor = TutorAgent()
    session_id = "test_user_1"
    print(f"Session ID: {session_id}")
    
    while True:
        user_input = input("\nStudent: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        
        response = tutor.ask(user_input, session_id=session_id)
        print(f"\nTutor: {response}")
