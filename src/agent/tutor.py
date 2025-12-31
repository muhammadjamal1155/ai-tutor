from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config.settings import config
from src.rag.vector_store import RAGPipeline
from src.memory.memory_manager import BaseMemoryManager, InMemoryHistoryManager
from src.memory.postgres_manager import PostgresHistoryManager
import os

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
        if memory_manager:
            self.memory_manager = memory_manager
        elif config.DATABASE_URL:
            # Use Supabase/Postgres if URL is available
            print("Using Persistent Postgres Memory (Supabase).")
            self.memory_manager = PostgresHistoryManager(config.DATABASE_URL)
        else:
            # Fallback to In-Memory
            print("Using In-Memory History (Volatile).")
            self.memory_manager = InMemoryHistoryManager()
        
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
        
        # Construct Chain using pure LCEL
        # We accept 'input' and 'context' from the caller (ask method)
        rag_chain = (
            RunnablePassthrough()
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
        )

    def generate_queries(self, original_query: str):
        """Generate variations of the query to potentially increase recall."""
        # Simple prompting for query expansion
        prompt = (
            f"You are an AI assistant. Generate 3 different search queries based on the user question "
            f"to retrieve comprehensive information from a document knowledge base.\n"
            f"Original question: {original_query}\n"
            f"Output ONLY the 3 queries separated by newlines."
        )
        try:
            response = self.llm.invoke(prompt)
            # Handle response being either AIMessage or string
            content = response.content if hasattr(response, 'content') else str(response)
            queries = [q.strip() for q in content.split('\\n') if q.strip()]
            final_queries = []
            for q in queries:
                 final_queries.append(q)
            return final_queries[:3]
        except Exception as e:
            print(f"Query expansion failed: {e}")
            return [original_query]

    def ask(self, question: str, session_id: str = "default_session"):
        """Ask a question to the AI Tutor with memory."""
        
        # 1. Retrieval (Enhanced with optional expansion)
        # We manually retrieve here so we can return the sources
        
        # Step A: Expansion
        search_queries = [question]
        if len(question.split()) > 2:
            print(f"Expanding query: {question}")
            expanded = self.generate_queries(question)
            if expanded:
                print(f"Expanded queries: {expanded}")
                search_queries.extend(expanded)
        
        # Step B: Multi-query Retrieval
        all_docs = []
        seen = set()
        for q in search_queries:
            docs = self.retriever.invoke(q)
            for doc in docs:
                # Content hash to deduplicate
                key = doc.page_content[:50]
                if key not in seen:
                    seen.add(key)
                    all_docs.append(doc)
        
        # Limit total docs (top 15)
        unique_docs = all_docs[:15]
        
        # Format Context
        formatted_context = format_docs(unique_docs)
        
        # Invoke Chain
        response_text = self.conversational_rag_chain.invoke(
            {"input": question, "context": formatted_context},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Prepare Sources
        sources = []
        for i, doc in enumerate(unique_docs):
            src = doc.metadata.get('source', 'Unknown')
            # Extract just filename if path
            filename = os.path.basename(src) if src else 'Unknown'
            # Check if source already added
            if not any(s['source'] == filename for s in sources):
                 sources.append({
                    "source": filename,
                    "content": doc.page_content[:200] + "..." # Snippet
                })
            
        return {
            "answer": response_text,
            "sources": sources[:5] # Top 5 distinct sources
        }

    def refresh_retriever(self):
        """Reload the retriever with updated index (after new document upload)."""
        print("Refreshing retriever with updated knowledge base...")
        self.rag = RAGPipeline()
        self.retriever = self.rag.get_retriever(k=12)  # Get more documents for comprehensive answers
        
        # Rebuild the chain with new retriever (logic same as init)
        rag_chain = (
            RunnablePassthrough()
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.memory_manager.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
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
            
            # Show ONLY the top result as requested
            for i, doc in enumerate(unique_docs[:1], 1):
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
