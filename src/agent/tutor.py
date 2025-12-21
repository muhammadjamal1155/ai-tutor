from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config.settings import config
from src.rag.vector_store import RAGPipeline
from src.memory.memory_manager import BaseMemoryManager, InMemoryHistoryManager

def format_docs(docs):
    """Enhanced document formatting to preserve all content and improve comprehension."""
    formatted_parts = []
    for i, doc in enumerate(docs):
        # Add document separator to help AI distinguish between different sources
        source = doc.metadata.get('source', f'Document {i+1}')
        formatted_parts.append(f"--- Source: {source} ---\n{doc.page_content}")
    
    return "\n\n".join(formatted_parts)

class TutorAgent:
    def __init__(self, memory_manager: BaseMemoryManager = None):
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME, 
            temperature=0.3, 
            openai_api_key=config.OPENAI_API_KEY
        )
        self.rag = RAGPipeline()
        self.retriever = self.rag.get_retriever(k=12)  # Get more documents for comprehensive answers
        
        # Dependency Injection (DIP)
        self.memory_manager = memory_manager or InMemoryHistoryManager()
        
        # System Prompt (comprehensive with focus on listing all types/categories)
        system_prompt = (
            "You are an expert AI Tutor. Provide comprehensive answers based on the provided context. "
            "IMPORTANT: When asked about types, categories, methods, or techniques, you MUST list ALL different types mentioned in the context. "
            "Do not summarize - list each type separately with its description. "
            "Use numbered lists or bullet points to clearly show all different types/categories. "
            "If multiple types are mentioned across different parts of the context, include ALL of them. "
            "If the answer isn't fully covered in the context, say what information you have available. "
            "Be thorough and well-organized in your explanations.\n\n"
            "SUMMARIZATION REQUESTS:\n"
            "If the user asks for a summary of a document, format your response as follows:\n"
            "1. **Key Concepts**: A bulleted list of the main ideas.\n"
            "2. **Detailed Summary**: A comprehensive paragraph explaining the document's content.\n"
            "3. **Key Takeaways**: A numbered list of the most important points."
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
        self.retriever = self.rag.get_retriever(k=12)  # Get more documents for comprehensive answers
        
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

    def search_documents(self, query: str, k: int = 8) -> str:
        """
        Search documents without using the LLM (fallback when quota exceeded).
        Enhanced to find comprehensive answers for types/categories questions.
        """
        try:
            # For questions about types/categories, expand search terms
            search_queries = [query]
            
            # If asking about types, add variations to capture more content
            if any(word in query.lower() for word in ['types', 'kinds', 'categories', 'methods', 'techniques', 'approaches']):
                base_term = query.lower()
                # Extract the main concept
                for word in ['types of', 'kinds of', 'categories of', 'methods of', 'techniques of']:
                    if word in base_term:
                        concept = base_term.split(word)[1].strip()
                        search_queries.extend([
                            concept,
                            f"{concept} methods",
                            f"{concept} techniques", 
                            f"{concept} approaches",
                            f"different {concept}",
                            f"{concept} examples"
                        ])
                        break
            
            # Perform multiple searches and combine results
            all_docs = []
            seen_content = set()
            
            for search_query in search_queries:
                docs = self.retriever.invoke(search_query)
                for doc in docs:
                    content_hash = doc.page_content.strip()[:200]  # Use first 200 chars as fingerprint
                    if content_hash not in seen_content:
                        seen_content.add(content_hash)
                        all_docs.append(doc)
            
            if not all_docs:
                return "No relevant information found in the uploaded documents. Please upload a document first or try a different question."
            
            # Sort by relevance score (if available) and take top k*2 for comprehensive coverage
            unique_docs = all_docs[:k*2]  # Get more docs for comprehensive answers
            
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
