
from src.memory.postgres_manager import PostgresHistoryManager
from langchain_core.messages import HumanMessage, AIMessage
from src.config.settings import config
import sys

print("--- Testing Postgres History Persistance ---")

if not config.DATABASE_URL:
    print("ERROR: DATABASE_URL is missing.")
    sys.exit(1)

try:
    # 1. Initialize Manager
    print("Initializing Manager...")
    manager = PostgresHistoryManager()
    
    # 2. Get History for a dummy session
    session_id = "test_debug_session_123"
    print(f"Getting history for session: {session_id}")
    history = manager.get_session_history(session_id)
    
    # 3. Add Messages
    print("Adding Human Message...")
    history.add_user_message("Hello, this is a debug test.")
    
    print("Adding AI Message...")
    history.add_ai_message("I am confirming that I can search the database.")
    
    # 4. Read Verification
    print("Reading back messages...")
    stored_messages = history.messages
    print(f"Count: {len(stored_messages)}")
    for msg in stored_messages:
        print(f" - [{msg.type}]: {msg.content}")
        
    if len(stored_messages) >= 2:
        print("\n✅ SUCCESS: Messages were saved and retrieved!")
        print("Please check your Supabase dashboard for session_id 'test_debug_session_123'.")
    else:
        print("\n❌ FAILED: Messages were NOT saved.")

except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")
