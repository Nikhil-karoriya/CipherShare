# CipherShare - Secure P2P File Sharing System

A lightweight, secure, and efficient **peer-to-peer (P2P)** file sharing system built in Python. This tool allows two peers to send and receive files directly over a network using **TCP sockets**, with **AES encryption**, **RSA key exchange**, and **zlib compression** to ensure privacy, integrity, and performance.

---

## Key Features

- Peer-to-peer architecture (no central server)
- AES (symmetric) encryption for fast and secure file protection
- RSA (asymmetric) encryption for secure AES key exchange
- Zlib compression to reduce file size before encryption
- Memory-optimized chunked transfer for large files
- File name and directory structure preserved on receipt
- Real-time transfer progress with `tqdm`
- Robust IP and port validation using the `ipaddress` module

---

## Security Architecture

- **AES-128** via Fernet for fast symmetric encryption
- **RSA-2048** for secure asymmetric key exchange
- **Zlib Compression** for pre-encryption size reduction
- **SHA-256** hashing for integrity verification after decryption

---

## Performance & Optimization

CipherShare is engineered to handle large file transfers over local or remote networks with minimal memory usage.

### Efficient Memory Management

Files are streamed in **32KB chunks**, allowing CipherShare to transfer **multi-GB files** using less than **2 MB of memory** per peer. This chunk-based approach eliminates the need to load full files into RAM.

### Speed Benchmark (1.5 GB file)

- **Transfer Time:** ~33 seconds  
- **Sender RAM Usage:** ~15.5 MB  
- **Receiver RAM Usage:** ~15.0 MB  
- **Encryption:** AES-128 per chunk  
- **Compression:** Zlib per chunk

> Demonstrates CipherShare's capability to securely transfer large files in under a minute with minimal system overhead.

---

## RAM Usage Comparison

| File Size | Full-Load RAM Usage | CipherShare (Chunked 32KB) | Actual RAM Used |
|-----------|----------------------|------------------------------|------------------|
| 42 MB     | ~105 MB              | ~15–18 MB                    | 15.5 MB          |
| 100 MB    | ~160 MB              | ~16 MB                       | 16 MB            |
| 500 MB    | ~560 MB              | ~18 MB                       | 18 MB (est.)     |
| 1.5 GB    | ~1600 MB             | ~20 MB                       | 15 MB            |
| 2 GB      | ~2100 MB             | ~23 MB                       | 17–18 MB (est.)  |

> Real usage stays within predicted bounds across various file sizes.

---

## Multi-GB File Transfer Capabilities

- Supports files over 2 GB via chunked streaming
- AES encryption and compression applied per chunk
- Consistent memory usage regardless of file size

---

## Project Screenshots

### Send File Interface
![Sending](assets/screenshots/client-1.png)

### Receive File Interface
![Receiving](assets/screenshots/client2-rcv.png)

---

## Project Structure

```

secure-p2p-file-transfer/
├── peer.py
├── crypto/
│ ├── aes_crypto.py
│ └── rsa_crypto.py
├── utils/
│ └── file_utils.py
├── keys/
│ ├── private_key.pem # Ignored (auto-generated)
│ └── public_keys.pem # Ignored (shared public key)
├── received_files/
├── .gitignore
└── README.md

```

---
## Requirements

- Python 3.10 or higher
- [`cryptography`](https://pypi.org/project/cryptography/)
- [`tqdm`](https://pypi.org/project/tqdm/)

### Installation

```bash
python -m venv .venv
source .venv/Scripts/activate        # For Windows
# or
source .venv/bin/activate            # For Linux/macOS

pip install cryptography tqdm
```

---

## Usage Instructions
### Start a peer to receive files

```bash
Copy
Edit
python peer.py --listen-port 5001
```
### Send a file to another peer

You will be prompted for:

```yaml
Send file (y/n)? y
Enter file path to send: sample.txt
Enter receiver's IP address: 192.168.1.10
Enter receiver's port: 5001
```

The file will be compressed, encrypted, securely transferred, and saved at the recipient’s end with a real-time progress bar and confirmation.
