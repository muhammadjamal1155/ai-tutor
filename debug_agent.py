try:
    from langchain.agents import AgentExecutor
    print("AgentExecutor found in langchain.agents")
except ImportError as e:
    print(f"AgentExecutor NOT found: {e}")

try:
    from langchain.agents import create_react_agent
    print("create_react_agent found in langchain.agents")
except ImportError as e:
    print(f"create_react_agent NOT found: {e}")

import langchain
print(f"LangChain version: {langchain.__version__}")
