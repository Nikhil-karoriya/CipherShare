# 🔐 CipherShare - Secure P2P File Sharing System 

A lightweight, secure, and efficient **peer-to-peer (P2P)** file sharing system built in Python. This tool allows two peers to send and receive files directly over a network using **TCP sockets**, with **AES encryption**, **RSA key exchange**, and **zlib compression** to ensure privacy, integrity, and efficiency.

---

## 🚀 Features

- 📡 Peer-to-peer architecture (no central server)
- 🔒 AES (symmetric) encryption for fast and secure file protection
- 🔑 RSA (asymmetric) encryption for safe AES key exchange
- 🗜️ Zlib compression to reduce file size before encryption
- 🧠 Optimized memory usage for large files using chunked transfer
- 📁 File name and structure preserved on receipt
- 📊 Real-time progress bar using `tqdm`
- ✅ IP and port validation using `ipaddress` module

---

## 🔐 Security

- **AES**: Fast file encryption (Fernet/AES-128)
- **RSA**: 2048-bit key pair used to securely encrypt the AES key
- **Zlib Compression**: Applied before encryption for supported formats
- **SHA-256**: File integrity check printed after decryption

---

## ⚙️ Performance & Optimization

CipherShare is built to **efficiently handle large file transfers** without consuming excessive RAM.

### ✅ Memory Optimization

Files are processed in **streaming chunks (32KB by default)**, meaning only one chunk is loaded into memory at a time — not the entire file. This enables **multi-GB file transfers** while using less than **2 MB of memory** per peer.

### 🚀 Real-World Speed Benchmark

**File Size:** 1.5 GB  
**Transfer Time:** ⏱️ ~33 seconds  
**Sender RAM:** ~15.5 MB  
**Receiver RAM:** ~15.0 MB  
**Chunk Size:** 32 KB (streamed & encrypted per chunk)

> ✅ Demonstrates CipherShare's ability to securely transfer multi-GB files in under a minute with minimal memory usage.

### 📊 RAM Usage Comparison

| File Size | Unoptimized RAM (Full File in RAM) | Optimized (Chunked 32KB) | Actual RAM Used |
|-----------|------------------------------------|----------------------------|------------------|
| 42 MB     | ~105 MB                            | ~15–18 MB                  | ✅ 15.5 MB        |
| 100 MB    | ~160 MB                            | ~16 MB                     | ✅ 16 MB          |
| 500 MB    | ~560 MB                            | ~18 MB                     | ✅ 18 MB (est.)   |
| 1.5 GB    | ~1600 MB                           | ~20 MB                     | ✅ 15 MB          |
| 2 GB      | ~2100 MB                           | ~23 MB                     | ✅ 17–18 MB (est.)|

---

### 📉 RAM Usage vs File Size

![RAM Graph](assets/ram_usage_vs_file_size.png)

> 🔍 The actual memory usage aligns closely with theoretical predictions.

---

## ⚡ Multi-GB File Transfer

- ✅ Chunk-based streaming supports massive files (tested: **up to 2 GB**)
- 🧠 Memory usage stays flat (~15MB)
- 🔐 AES encryption and zlib compression used per chunk

---

## 📸 Screenshots

### 📤 Send File Prompt

![Sending](assets/screenshots/client-1.png)

### 🔽 Receiving File with Progress Bar

![Receving](assets/screenshots/client2-rcv.png)

---

## 🛠️ Project Structure


```
secure-p2p-file-transfer/
├── peer.py
| 
├── crypto/
│ ├── aes_crypto.py
│ └── rsa_crypto.py
| 
├── utils/
│ └── file_utils.py
|
├── keys/
│ ├── private_key.pem     # (Ignored) Generated RSA private key
│ └── public_keys.pem     # (Ignored) Shared RSA public key
|
├── received_files/
| 
├── .gitignore
└── README.md
```

---

## 📦 Requirements

- Python 3.10+
- [`cryptography`](https://pypi.org/project/cryptography/)
- [`tqdm`](https://pypi.org/project/tqdm/)

### 📥 Install dependencies

```bash
python -m venv .venv
source .venv/Scripts/activate        # Windows
# or
source .venv/bin/activate            # Linux/macOS

pip install cryptography tqdm
```

---

## 📡 Usage

### 📥 Start a peer to receive files

```bash
python peer.py --listen-port 5001
```

### 📤 Send a file to another peer
You will be prompted:

```
Send file (y/n)? y
Enter file path to send: sample.txt
Enter receiver's IP address: 192.168.1.10
Enter receiver's port: 5001
```

- The file will be compressed, encrypted, transferred securely, and the sender and recipient will see a progress bar and confirmation.

---
