import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print("--- Debugging Environment Loading ---")

# 1. Check CWD
print(f"CWD: {os.getcwd()}")

# 2. Resolve Path
FILE_PATH = Path(__file__).resolve()
PROJECT_ROOT = FILE_PATH.parent
ENV_PATH = PROJECT_ROOT / ".env"

print(f"Script Location: {FILE_PATH}")
print(f"Calculated Root: {PROJECT_ROOT}")
print(f"Target .env Path: {ENV_PATH}")
print(f"Exists? {ENV_PATH.exists()}")

# 3. Try Loading
load_dotenv(dotenv_path=ENV_PATH, override=True)
key = os.getenv("GOOGLE_API_KEY")

if key:
    print(f"SUCCESS: Loaded key via dotenv: {key[:5]}...")
else:
    print("FAILURE: dotenv did not load key.")
    
    # 4. Manual Read Attempt
    if ENV_PATH.exists():
        print("Reading file manually...")
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"File content length: {len(content)}")
                if "GOOGLE_API_KEY" in content:
                    print("Key VARIABLE found in text.")
                else:
                    print("Key VARIABLE NOT FOUND in text.")
        except Exception as e:
            print(f"Error reading file: {e}")

# 5. Check Import from Settings
print("\n--- Importing src.config.settings ---")
try:
    from src.config.settings import config
    print(f"Settings Config Key: {str(config.GOOGLE_API_KEY)[:5]}...")
except Exception as e:
    print(f"Import failed: {e}")
