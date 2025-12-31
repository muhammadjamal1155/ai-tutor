
import psycopg2
import sys

# Explicit credentials given by user
DB_HOST = "aws-1-ap-southeast-1.pooler.supabase.com"
DB_PORT = "6543"
DB_NAME = "postgres"
DB_USER = "postgres.blfczjgtcaugdlxtpikk"
DB_PASS = "Tester1144##@@"  # Valid password with special chars

print(f"--- Auth Debugger ---")
print(f"Target: {DB_HOST}:{DB_PORT}")
print(f"User:   {DB_USER}")
print(f"Pass:   {DB_PASS[:4]}****")

try:
    print("Connecting with explicit kwargs (no URL parsing)...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        connect_timeout=10
    )
    print("✅ SUCCESS! The password is correct and works.")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")
