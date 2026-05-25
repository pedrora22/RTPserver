from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Chave pré-compartilhada de 16 bytes (AES-128)
KEY = b'RTPchave1234567!'

def encrypt(data: bytes) -> bytes:
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted

def decrypt(data: bytes) -> bytes:
    iv = data[:16]
    encrypted = data[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted), AES.block_size)
