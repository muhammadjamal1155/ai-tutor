import os
import psycopg2
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from src.memory.memory_manager import BaseMemoryManager
from src.config.settings import config

class PostgresHistoryManager(BaseMemoryManager):
    """
    Concrete implementation of Memory Manager using PostgreSQL (Supabase).
    PERSISTENT storage that survives server restarts.
    Uses langchain_community for robust psycopg2 support.
    """
    def __init__(self, connection_string: str = None):
        # Use config if not provided
        self.connection_string = connection_string or config.DATABASE_URL
        
        if not self.connection_string:
            raise ValueError("Database connection string is required for PostgresHistoryManager")
            
        print(f"Initializing Postgres History connection...", flush=True)
        # Verify connection immediately to fail fast if creds are wrong
        try:
            conn = psycopg2.connect(self.connection_string)
            conn.close()
            print("Postgres connection verification successful.", flush=True)
        except Exception as e:
            print(f"CRITICAL ERROR: Could not connect to Postgres/Supabase: {e}", flush=True)
            # We don't raise here to avoid crashing app startup if DB is flaky, 
            # but getting history will fail later.

    def get_session_history(self, session_id: str):
        """
        Returns a Postgres-backed chat message history.
        Table 'message_store' will be created automatically if it doesn't exist.
        """
        # langchain_community's PostgresChatMessageHistory auto-creates table
        return PostgresChatMessageHistory(
            session_id=session_id,
            connection_string=self.connection_string,
            table_name="message_store"
        )
