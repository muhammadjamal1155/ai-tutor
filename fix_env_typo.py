import os

env_path = ".env"

try:
    with open(env_path, "r") as f:
        content = f.read()
    
    # Fix the typo
    if "GOOGLE_APT_KEY" in content:
        new_content = content.replace("GOOGLE_APT_KEY", "GOOGLE_API_KEY")
        with open(env_path, "w") as f:
            f.write(new_content)
        print("Successfully fixed typo in .env file.")
    else:
        print("Could not find 'GOOGLE_APT_KEY' in .env file. It might already be fixed or named differently.")
        
except Exception as e:
    print(f"Error modifying .env file: {e}")
