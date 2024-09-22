from cryptography.fernet import Fernet
from app import app

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data):
    f = Fernet(app.config['ENCRYPTION_KEY'])
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    f = Fernet(app.config['ENCRYPTION_KEY'])
    return f.decrypt(encrypted_data.encode()).decode()