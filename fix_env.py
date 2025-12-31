
import os

# New Password: SuperSecretPass12
# Host:     aws-1-ap-southeast-1.pooler.supabase.com
# Port:     6543
target_url = "postgresql://postgres.blfczjgtcaugdlxtpikk:SuperSecretPass12@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

try:
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    found = False
    for line in lines:
        if line.strip().startswith('DATABASE_URL='):
            new_lines.append(f"DATABASE_URL={target_url}\n")
            found = True
        else:
            new_lines.append(line)
            
    if not found:
        new_lines.append(f"\nDATABASE_URL={target_url}\n")
        
    with open('.env', 'w') as f:
        f.writelines(new_lines)
        
    print("Successfully updated .env with new password")
    
except Exception as e:
    print(f"Error updating .env: {e}")
