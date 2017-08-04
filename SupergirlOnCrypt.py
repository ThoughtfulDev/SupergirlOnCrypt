from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from RSA.RSAKeyGen import RSAKeyGen


def init():
    genKeyPair()


def genKeyPair():
    keys = RSAKeyGen(size=1024)
    encryptClientPrivKey(keys.getPrivateKeyAsStr())
    keys.forgetPrivate()

def encryptClientPrivKey(priv_key):
    with open("serverkeys/public.key", "rb") as key_file:
        public_key = serialization.load_ssh_public_key(
            key_file.read(),
            backend=default_backend()
        )

    cipher_cpriv = public_key.encrypt(
        bytes(priv_key, 'utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )








if __name__ == "__main__":
    init()