from cryptography.fernet import Fernet
import base64
import os

def generate_key():
    """Generates a new 32-byte base64 key for Fernet encryption."""
    return Fernet.generate_key().decode()

def get_cipher(key: str):
    """Returns a Fernet cipher instance for the given key."""
    return Fernet(key.encode())

def encrypt_data(plain_text: str, key: str):
    """Encrypts plain text using the provided Fernet key."""
    cipher = get_cipher(key)
    return cipher.encrypt(plain_text.encode()).decode()

def decrypt_data(encrypted_text: str, key: str):
    """Decrypts encrypted text using the provided Fernet key."""
    cipher = get_cipher(key)
    return cipher.decrypt(encrypted_text.encode()).decode()
