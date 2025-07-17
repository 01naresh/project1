# crypto_utils.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

key = b'ThisIsASecretKey'  # Key must be 16, 24, or 32 bytes

def encrypt_message(raw):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(raw.encode())
    return base64.b64encode(nonce + ciphertext).decode()

def decrypt_message(enc):
    enc = base64.b64decode(enc)
    nonce = enc[:16]
    ciphertext = enc[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()
