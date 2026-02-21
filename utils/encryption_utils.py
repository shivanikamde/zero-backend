import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("ENCRYPTION_SECRET").encode()
cipher = Fernet(key)

def encrypt_key(private_key):
    return cipher.encrypt(private_key.encode()).decode()

def decrypt_key(encrypted_key):
    return cipher.decrypt(encrypted_key.encode()).decode()