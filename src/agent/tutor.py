from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from src.config.settings import config
from src.rag.vector_store import RAGPipeline

class TutorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=config.MODEL_NAME, temperature=0.3)
        self.rag = RAGPipeline()
        self.retriever = self.rag.get_retriever()
        
        # Define the system prompt template for the tutor
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
                ("human", "{input}"),
            ]
        )
        
        # Create the chain
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    def ask(self, question: str):
        """Ask a question to the AI Tutor."""
        response = self.rag_chain.invoke({"input": question})
        return response["answer"]

if __name__ == "__main__":
    tutor = TutorAgent()
    while True:
        user_input = input("\nStudent: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        
        response = tutor.ask(user_input)
        print(f"\nTutor: {response}")
