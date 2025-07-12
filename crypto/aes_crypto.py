import zlib
from cryptography.fernet import Fernet

def generate_aes_key():
    return Fernet.generate_key()

def encrypt_file_with_aes(file_data: bytes, aes_key: bytes) -> bytes:
    fernet = Fernet(aes_key)
    compressed = zlib.compress(file_data)
    return fernet.encrypt(compressed)

def decrypt_file_with_aes(ciphertext: bytes, aes_key: bytes) -> bytes:
    fernet = Fernet(aes_key)
    decompressed = zlib.decompress(fernet.decrypt(ciphertext))
    return decompressed