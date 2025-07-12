import os
import socket
import threading
import traceback
from tqdm import tqdm
import argparse
from time import sleep
from crypto.rsa_crypto import (
    decrypt_with_rsa_private_key,
    encrypt_with_rsa_public_key,
    generate_rsa_key_pair,
    is_valid_pem_key
)
from crypto.aes_crypto import generate_aes_key, encrypt_file_with_aes, decrypt_file_with_aes
from utils.file_utils import read_file, write_file, ensure_dir, sha256_digest, is_valid_ip, is_valid_port

PRIVATE_KEY_PATH = 'keys/private_key.pem'
PUBLIC_KEY_PATH = 'keys/public_keys.pem'
RECEIVE_DIR = 'received_files'
DEFAULT_PORT = 5001

ensure_dir(RECEIVE_DIR)
os.makedirs("keys", exist_ok=True)

if not is_valid_pem_key(PRIVATE_KEY_PATH, is_private=True) or not is_valid_pem_key(PUBLIC_KEY_PATH, is_private=False):
    print("\n[*] RSA key missing or invalid. Regenerating...")
    generate_rsa_key_pair(PRIVATE_KEY_PATH, PUBLIC_KEY_PATH)
    print("\n[+] RSA key pair regenerated.")

parser = argparse.ArgumentParser()
parser.add_argument("--listen-port", type=int, required=True)
args = parser.parse_args()

LISTEN_PORT = args.listen_port

def peer_listener():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', LISTEN_PORT))
        server_socket.listen(5)
        print(f"\n[+] Listening on port {LISTEN_PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"\n[+] Incoming connection from {addr}")

            try:
                key_size = int.from_bytes(client_socket.recv(4), 'big')
                encrypted_key = client_socket.recv(key_size)

                name_len = int.from_bytes(client_socket.recv(4), 'big')
                file_name = client_socket.recv(name_len).decode()

                extension = int.from_bytes(client_socket.recv(4), 'big')
                file_extension = client_socket.recv(extension).decode()

                total_size = int.from_bytes(client_socket.recv(8), 'big')
                ciphertext = b""

                with tqdm(total=total_size, desc=f"Receiving {file_name}", unit="B", unit_scale=True) as pbar:
                    while len(ciphertext) < total_size:
                        chunk = client_socket.recv(min(4096, total_size - len(ciphertext)))
                        if not chunk:
                            break
                        ciphertext += chunk
                        pbar.update(len(chunk))

                aes_key = decrypt_with_rsa_private_key(encrypted_key, PRIVATE_KEY_PATH)
                plaintext = decrypt_file_with_aes(ciphertext, aes_key, file_extension)

                file_path = os.path.join(RECEIVE_DIR, file_name)
                write_file(file_path, plaintext)
                print(f"\n[+] File saved to {file_path}")

                file_hash = sha256_digest(plaintext)
                print(f"\n[+] SHA256 Hash: {file_hash}")

            except Exception as e:
                print(f"\n[!] ERROR receiving file: {str(e)}\n{traceback.format_exc()}")
            finally:
                client_socket.close()

    except Exception as e:
        print(f"\n[!] Server failed: {str(e)}\n{traceback.format_exc()}")

def send_file(file_path, peer_ip, peer_port):
    try:
    
        if not os.path.isfile(file_path):
            print(f"\n[!] File '{file_path}' does not exist.")
            return

        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1].lower()
        file_data = read_file(file_path)
        
        aes_key = generate_aes_key()
        ciphertext = encrypt_file_with_aes(file_data, aes_key, file_extension)
        encrypted_key = encrypt_with_rsa_public_key(aes_key, PUBLIC_KEY_PATH)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_ip, peer_port))

        client_socket.sendall(len(encrypted_key).to_bytes(4, 'big'))
        client_socket.sendall(encrypted_key)
        
        client_socket.sendall(len(file_name.encode()).to_bytes(4, 'big'))
        client_socket.sendall(file_name.encode())
        
        client_socket.sendall(len(file_extension.encode()).to_bytes(4, 'big'))
        client_socket.sendall(file_extension.encode())
        
        client_socket.sendall(len(ciphertext).to_bytes(8, 'big'))

        with tqdm(total=len(ciphertext), desc=f"Sending {file_name}", unit="B", unit_scale=True) as pbar:
            for i in range(0, len(ciphertext), 4096):
                chunk = ciphertext[i:i+4096]
                client_socket.sendall(chunk)
                pbar.update(len(chunk))

        print(f"\n[+] File '{file_name}' sent successfully to {peer_ip}:{peer_port}.")
        client_socket.close()

    except Exception as e:
        print(f"\n[!] Failed to send file: {str(e)}\n{traceback.format_exc()}")

if __name__ == '__main__':

    threading.Thread(target=peer_listener, daemon=True).start()
    sleep(1)

    while True:
        user_input = input("\nSend file (y/n)? ").strip().lower()

        if user_input == 'y':
            file_path = input("\nEnter file path to send: ").strip()
            peer_ip = input("\nEnter receiver's IP address: ").strip()
            peer_port_input = input("\nEnter receiver's port: ").strip()

            if not is_valid_port(peer_port_input) or not is_valid_ip(peer_ip):
                print("\n[!] Receiver IP or port not correct/specified.")
                continue

            peer_port = int(peer_port_input)
            send_file(file_path, peer_ip, peer_port)

        else:
            print("\n[INFO] Waiting for incoming transfers.")
            
            user_input = input("\nPress 'e' to exit / 'c' to continue: ").strip().lower()
            if user_input == 'e':
                print("\n[INFO] Exiting...")
                break
