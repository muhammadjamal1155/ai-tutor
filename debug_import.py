try:
    from src.agent.tools.tool_factory import ToolFactory
    print("Import successful")
    f = ToolFactory()
    print("Instantiation successful (if mocked)")
except Exception as e:
    print(f"Error: {e}")
