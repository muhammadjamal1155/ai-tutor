import os
import sys
import traceback

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import config
from src.agent.tutor import TutorAgent

def debug_chat():
    print("Initializing Tutor Agent...")
    try:
        tutor_agent = TutorAgent()
        print("Initialization Successful.")
    except Exception as e:
        print("Initialization Failed.")
        traceback.print_exc()
        return

    print("\nAttempting to ask a question...")
    try:
        # Simulate the call made in server.py
        response = tutor_agent.ask("Hello, who are you?", session_id="debug_session")
        print(f"\nResponse received: {response}")
    except Exception as e:
        print(f"\nCaught Exception during ask(): {type(e).__name__}")
        print(f"Error message: '{str(e)}'")
        traceback.print_exc()

if __name__ == "__main__":
    debug_chat()
