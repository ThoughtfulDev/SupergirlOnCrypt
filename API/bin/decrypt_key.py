from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64
import sys

if not len(sys.argv) is 2:
    sys.exit()


def decryptCPriv(server_priv, client_private_enc_key_filename):
    "Decrypts the clients private key with the servers private key"
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


filename = sys.argv[1]

with open("bin/private.key", "rb") as server_p:
    server_priv_key = serialization.load_pem_private_key(
        server_p.read(),
        password=None,
        backend=default_backend()
    )

clear_key = decryptCPriv(server_priv_key, filename)
clear_key = base64.b64encode(clear_key).decode('utf-8')
print(clear_key)
