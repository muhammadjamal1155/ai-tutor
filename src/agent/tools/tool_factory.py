from src.rag.vector_store import RAGPipeline
from typing import List
from langchain_core.tools import Tool

class ToolFactory:
    """
    Factory class to create tools for the agent (Open/Closed Principle).
    """
    def __init__(self):
        self.rag = RAGPipeline()

    def create_tools(self) -> List[Tool]:
        """Creates and returns the list of tools available to the agent."""
        retriever = self.rag.get_retriever()
        
        def search_func(query: str):
            docs = retriever.invoke(query)
            return "\n\n".join([doc.page_content for doc in docs])

        search_tool = Tool(
            name="search_course_materials",
            func=search_func,
            description="Searches and returns excerpts from the student's course materials/notes. Use this tool when you need to answer questions based on the provided documents."
        )
        
        return [search_tool]
