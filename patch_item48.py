import os

enc_path = "documents/encryption.py"
os.makedirs("documents", exist_ok=True)

encryption_code = """
import os
from cryptography.fernet import Fernet

def get_or_create_key():
    key_path = "config/encryption.key"
    os.makedirs("config", exist_ok=True)
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_uploaded_file(file_path):
    \"\"\"
    Encrypts sensitive compliance document files at rest on the server disk[cite: 1].
    \"\"\"
    if not os.path.exists(file_path):
        return False
        
    key = get_or_create_key()
    f = Fernet(key)
    
    with open(file_path, "rb") as file_to_encrypt:
        data = file_to_encrypt.read()
        
    encrypted_data = f.encrypt(data)
    
    with open(file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
        
    print(f"ENCRYPTION SUCCESS: File securely encrypted at rest -> {file_path}")
    return True
"""

with open(enc_path, "w", encoding="utf-8") as f:
    f.write(encryption_code)

print("SUCCESS: File-level encryption service created successfully!")
