import os
import hashlib
import ipaddress

def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def write_file(path: str, data: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True) 
    with open(path, "wb") as f:
        f.write(data)

def sha256_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def ensure_dir(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_valid_ip(ip_str):
    try:
        if ip_str.strip().lower() == "localhost":
            return True
        
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False
    
def is_valid_port(port_str):
    try:
        port = int(port_str)
        return 1 <= port <= 65535
    except ValueError:
        return False
