import zlib
from cryptography.fernet import Fernet

SKIP_COMPRESSION_EXTENSIONS = {
    '.zip', '.gz', '.bz2', '.xz', '.rar', '.7z',
    '.jpg', '.jpeg', '.png', '.gif', '.webp',
    '.mp3', '.mp4', '.avi', '.mkv', '.mov',
    '.pdf'
}

def generate_aes_key():
    return Fernet.generate_key()

def encrypt_file_with_aes(file_data: bytes, aes_key: bytes, file_extension: str) -> bytes:
   
    fernet = Fernet(aes_key)

    if file_extension.lower() not in SKIP_COMPRESSION_EXTENSIONS:
        try:
            file_data = zlib.compress(file_data)

        except Exception as e:
            print(f"[!] Compression failed: {e}")
    
    return fernet.encrypt(file_data)

def decrypt_file_with_aes(ciphertext: bytes, aes_key: bytes, file_extension: str) -> bytes:
   
    fernet = Fernet(aes_key)

    try:
        decrypted_data = fernet.decrypt(ciphertext)

    except Exception as e:
        raise Exception(f"[!] AES decryption failed: {e}")

    if file_extension.lower() not in SKIP_COMPRESSION_EXTENSIONS:
        try:
            decrypted_data = zlib.decompress(decrypted_data)
            
        except zlib.error:
            print("[!] Warning: Failed to decompress — file may not be compressed")

    return decrypted_data
