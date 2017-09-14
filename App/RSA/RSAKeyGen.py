from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class RSAKeyGen:
    def __init__(self, size=1024, pub_exp=65537):
        self.key = rsa.generate_private_key(backend=default_backend(), public_exponent=pub_exp, key_size=size)
        self.public_key = self.key.public_key().public_bytes(serialization.Encoding.OpenSSH,
                                                             serialization.PublicFormat.OpenSSH)
        self.private_key = self.key.private_bytes(encoding=serialization.Encoding.PEM,
                                                  format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                  encryption_algorithm=serialization.NoEncryption())
        self.public_key_str = self.public_key.decode('utf-8')
        self.private_key_str = self.private_key.decode('utf-8')

    def getPrivateKeyAsStr(self):
        return self.private_key_str

    def getPublicKeyAsStr(self):
        return self.public_key_str

    def getKeyPair(self):
        return self.key

    def forgetPrivate(self):
        self.private_key = None
        self.private_key_str = None
        del self.private_key
        del self.private_key_str
