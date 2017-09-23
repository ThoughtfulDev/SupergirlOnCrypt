from PyQt5.QtCore import QThread
import sys
from Helper import Helper
from pathlib import Path
from FileCrypter import FileCrypter


class DecryptThread (QThread):
    def __init__(self, priv_key):
        QThread.__init__(self)
        self.privkey = priv_key

    def run(self):
        h = Helper()
        h.info('DecryptThread started')
        self.decrypt()

    def decrypt(self):
        h = Helper()
        not_encrypted = []
        pathlist = Path('./test_files').glob('**/*.supergirl')
        for path in pathlist:
            path_in_str = str(path)
            fc = FileCrypter()
            try:
                fc.decrypt_file(path_in_str, self.privkey)
                h.info("Decrypted " + path_in_str)
            except IOError:
                not_encrypted.append(path_in_str)
                h.error("Could not decrypt " + path_in_str)
        sys.exit()
