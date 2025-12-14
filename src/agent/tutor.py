from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from src.config.settings import config
from src.memory.memory_manager import BaseMemoryManager, InMemoryHistoryManager
from src.agent.tools.tool_factory import ToolFactory

class TutorAgent:
    def __init__(self, memory_manager: BaseMemoryManager = None):
        self.llm = ChatGoogleGenerativeAI(model=config.MODEL_NAME, temperature=0.3)
        
        # Dependency Injection (DIP)
        self.memory_manager = memory_manager or InMemoryHistoryManager()
        
        # Load Tools (OCP)
        self.tools = ToolFactory().create_tools()
        
        # ReAct Prompt
        # Standard ReAct prompt template
        template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)
        
        # Create Agent
        agent = create_react_agent(self.llm, self.tools, prompt)
        
        # Create Executor
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True
        )
        
        # Wrap with Message History
        self.conversational_agent = RunnableWithMessageHistory(
            agent_executor,
            self.memory_manager.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history", # Not used directly in ReAct prompt but stored in memory
            output_messages_key="output", # AgentExecutor returns 'output'
        )

    def ask(self, question: str, session_id: str = "default_session"):
        """Ask a question to the Agentic Tutor."""
        response = self.conversational_agent.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )
        return response["output"]

if __name__ == "__main__":
    tutor = TutorAgent()
    session_id = "test_agent_1"
    print(f"Session ID: {session_id}")
    
    while True:
        user_input = input("\nStudent: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        
        response = tutor.ask(user_input, session_id=session_id)
        print(f"\nTutor: {response}")
