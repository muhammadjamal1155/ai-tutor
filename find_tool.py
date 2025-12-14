import langchain
import pkgutil
import importlib

def find_function(package, func_name):
    # This is a naive search, might work if it's exported
    try:
        from langchain.tools.retriever import create_retriever_tool
        print("Found in: langchain.tools.retriever")
        return
    except ImportError:
        pass

    try:
        from langchain.agents.agent_toolkits import create_retriever_tool
        print("Found in: langchain.agents.agent_toolkits")
        return
    except ImportError:
        pass
    
    print("Could not find it via standard paths.")

find_function(langchain, "create_retriever_tool")
