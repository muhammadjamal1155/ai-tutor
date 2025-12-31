
import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load env variables
load_dotenv()

url = os.getenv("DATABASE_URL")

print(f"--- Database Connection Debugger ---")
if not url:
    print("ERROR: DATABASE_URL is not set in .env")
    sys.exit(1)

print(f"URL found (starts with): {url[:15]}...")

try:
    print("Attempting to connect...")
    conn = psycopg2.connect(url)
    print("Connection SUCCESS!")
    
    print("Attempting to create a cursor...")
    cur = conn.cursor()
    
    print("Attempting to run a simple query (SELECT 1)...")
    cur.execute("SELECT 1")
    result = cur.fetchone()
    print(f"Query Result: {result}")
    
    print("Attempting to check for 'message_store' table...")
    cur.execute("SELECT to_regclass('public.message_store');")
    table_exists = cur.fetchone()[0]
    print(f"Table 'message_store' exists: {table_exists}")

    cur.close()
    conn.close()
    print("--- Test Complete: SUCCESS ---")
    
except Exception as e:
    print(f"\n!!! CONNECTION FAILED !!!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
