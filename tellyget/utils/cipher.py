from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

class Cipher:
    def __init__(self, key):
        self.cipher = DES3.new(key.encode(), DES3.MODE_ECB)

    def encrypt(self, plain_text):
        cipher_text = self.cipher.encrypt(pad(plain_text.encode(), DES3.block_size))
        return cipher_text.hex().upper()

    def decrypt(self, cipher_text):
        plain_text = unpad(self.cipher.decrypt(bytes.fromhex(cipher_text)), DES3.block_size)
        return plain_text.decode()
