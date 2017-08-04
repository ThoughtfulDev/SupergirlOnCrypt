from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from AES.RandomKeyGen import RandomKeyGen

class FileCrypter:
    def __init__(self):
        self.key, self.iv = RandomKeyGen().getKey()
        self.backend = default_backend()
        self.cipher = Cipher(algorithms.AES(self.key), modes.CTR(self.iv), backend=self.backend)
        self.encryptor = self.cipher.encryptor()
        self.decryptor = self.cipher.decryptor()

    def aes_encrypt(self, msg):
        return self.encryptor.update(msg) + self.encryptor.finalize()

    def aes_decrypt(self, cipher):
        return self.decryptor.update(cipher) + self.decryptor.finalize()

