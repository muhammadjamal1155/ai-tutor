from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config.settings import config
from src.rag.vector_store import RAGPipeline
from src.memory.memory_manager import BaseMemoryManager, InMemoryHistoryManager

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class TutorAgent:
    def __init__(self, memory_manager: BaseMemoryManager = None):
        self.llm = ChatGoogleGenerativeAI(
            model=config.MODEL_NAME, 
            temperature=0.3, 
            google_api_key=config.GOOGLE_API_KEY
        )
        self.rag = RAGPipeline()
        self.retriever = self.rag.get_retriever()
        
        # Dependency Injection (DIP)
        self.memory_manager = memory_manager or InMemoryHistoryManager()
        
        # System Prompt
        system_prompt = (
            "You are an expert AI Tutor designed to help students understand complex topics. "
            "Use the following pieces of retrieved context to answer the question. "
            "If the answer is not in the context, say that you don't have that information in your notes. "
            "Keep your answer simple, clear, and focused on the student's question."
            "\n\n"
            "Context:\n{context}"
        )
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        
        # Construct Chain using pure LCEL (No 'create_retrieval_chain' dependency)
        # 1. Retrieve context
        # 2. Format context
        # 3. Pass through input and history
        # 4. Generate answer
        
        # We need a chain that accepts 'input' and 'chat_history'
        # The retriever needs 'input'.
        
        rag_chain = (
            RunnablePassthrough.assign(
                context=lambda x: format_docs(self.retriever.invoke(x["input"]))
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Wrap with Message History
        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.memory_manager.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer", # StrOutputParser returns the string directly as output
        )

    def ask(self, question: str, session_id: str = "default_session"):
        """Ask a question to the AI Tutor with memory."""
        # For RunnableWithMessageHistory wrapping a chain that returns a string, 
        # the output is just the result.
        response_text = self.conversational_rag_chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )
        return response_text

    def refresh_retriever(self):
        """Reload the retriever with updated index (after new document upload)."""
        print("Refreshing retriever with updated knowledge base...")
        self.rag = RAGPipeline()
        self.retriever = self.rag.get_retriever()
        
        # Rebuild the chain with new retriever
        rag_chain = (
            RunnablePassthrough.assign(
                context=lambda x: format_docs(self.retriever.invoke(x["input"]))
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.memory_manager.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        print("Retriever refreshed successfully.")

    def search_documents(self, query: str, k: int = 5) -> str:
        """
        Search documents without using the LLM (fallback when quota exceeded).
        Returns formatted document excerpts relevant to the query.
        """
        try:
            docs = self.retriever.invoke(query)
            if not docs:
                return "No relevant information found in the uploaded documents. Please upload a document first or try a different question."
            
            # Remove duplicates based on content
            seen_content = set()
            unique_docs = []
            for doc in docs:
                content_hash = doc.page_content.strip()[:200]  # Use first 200 chars as fingerprint
                if content_hash not in seen_content:
                    seen_content.add(content_hash)
                    unique_docs.append(doc)
            
            if not unique_docs:
                return "No relevant information found in the uploaded documents."
            
            # Format the results nicely
            results = []
            results.append("📚 **Found relevant information from your documents:**\n")
            
            for i, doc in enumerate(unique_docs[:k], 1):
                source = doc.metadata.get('source', 'Unknown document')
                # Get just the filename
                if '/' in source or '\\' in source:
                    source = source.replace('\\', '/').split('/')[-1]
                
                content = doc.page_content.strip()
                # Truncate if too long
                if len(content) > 500:
                    content = content[:500] + "..."
                
                results.append(f"**📄 Source {i}: {source}**")
                results.append(f"> {content}\n")
            
            results.append("\n---\n*⚠️ This response is from document search only (AI is currently unavailable due to quota limits). The AI will provide better explanations when available.*")
            
            return "\n".join(results)
        except Exception as e:
            return f"Error searching documents: {str(e)}"

if __name__ == "__main__":
    tutor = TutorAgent()
    session_id = "test_user_lcel"
    print(f"Session ID: {session_id}")
    
    while True:
        user_input = input("\nStudent: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        
        response = tutor.ask(user_input, session_id=session_id)
        print(f"\nTutor: {response}")
