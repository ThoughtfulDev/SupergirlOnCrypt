from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from AES.RandomKeyGen import RandomKeyGen
import base64, os
import glob
from chardet.universaldetector import UniversalDetector

class FileCrypter:

    def __init__(self):
        self.key, self.iv = RandomKeyGen().getKey()
        self.backend = default_backend()
        self.cipher = Cipher(algorithms.AES(self.key), modes.CTR(self.iv), backend=self.backend)
        self.encryptor = self.cipher.encryptor()
        self.decryptor = self.cipher.decryptor()
        self.encoding = 'utf-8'

    def detectDecoding(self, filename):
        detector = UniversalDetector()
        for filename in glob.glob(filename):
            detector.reset()
            for line in open(filename, 'rb'):
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            self.encoding = detector.result['encoding']

    def aes_encrypt(self, msg):
        return self.encryptor.update(msg)

    def aes_decrypt(self, cipher):
        return self.decryptor.update(cipher)

    def isNone(self):
        return self.encoding is None

    def encryptFile(self, filename, client_pub_key):
        if self.isNone(): return

        with open(filename, 'rb') as f:
            content_list = f.readlines()
            f.close()

        i = 0
        for x in content_list:
            x = self.aes_encrypt(x)
            x = base64.b64encode(x).decode(self.encoding)
            content_list[i] = x
            i = i + 1

        public_key = serialization.load_ssh_public_key(
            bytes(client_pub_key, 'utf-8'),
            backend=default_backend()
        )

        keyb64 = base64.b64encode(self.key)
        ivb64 = base64.b64encode(self.iv)
        t = bytes(keyb64.decode(self.encoding) + ";" + ivb64.decode(self.encoding), self.encoding)

        cipher = public_key.encrypt(
            t,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        cipher = base64.b64encode(cipher).decode(self.encoding)
        with open(filename + '.supergirl', 'w') as enc_f:
            enc_f.write(self.encoding + '\n')
            enc_f.write(cipher + '\n')
            for x in content_list:
                enc_f.write(str(x) + '\n')
            enc_f.close()

        os.remove(filename)

    def decyptFile(self, filename, privateKeyStr):
        if self.isNone(): return

        private_key = serialization.load_pem_private_key(
            bytes(privateKeyStr, 'utf-8'),
            password=None,
            backend=default_backend()
        )

        with open(filename, 'r') as f_enc:
            encoding = f_enc.readline().strip()
            file_content_cipher = f_enc.readlines()
            f_enc.close()

        aes_line = file_content_cipher[0] # second line
        file_content_cipher.pop(0)
        aes_line = bytes(aes_line, encoding)
        aes_line = base64.b64decode(aes_line)

        j = 0
        for x in file_content_cipher:
            x = x.strip()
            file_content_cipher[j] = base64.b64decode(x)
            j = j + 1

        aes_iv_clear = private_key.decrypt(
            aes_line,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        aes_iv = aes_iv_clear.decode(encoding).split(';')
        aes_key = base64.b64decode(aes_iv[0])
        aes_iv = base64.b64decode(aes_iv[1])
        decryptor = Cipher(algorithms.AES(aes_key), modes.CTR(aes_iv), backend=self.backend).decryptor()

        fileContentClearList = []
        for x in file_content_cipher:
            fileContentClear = decryptor.update(x)
            fileContentClear = fileContentClear.decode(encoding)
            fileContentClearList.append(fileContentClear)

        with open(filename[0: len(filename) - 10], 'w') as clearFile:
            for text in fileContentClearList:
                clearFile.write(text)
            clearFile.close()

        os.remove(filename)
