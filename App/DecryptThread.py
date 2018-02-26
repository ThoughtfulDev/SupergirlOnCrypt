import sys
import threading
from pathlib import Path
from Helper import Helper
from FileCrypter import FileCrypter
import Config


class DecryptThread (threading.Thread):
    def __init__(self, priv_key, eel_obj):
        threading.Thread.__init__(self)
        self.privkey = priv_key
        self.eel = eel_obj

    def run(self):
        h = Helper()
        h.info('DecryptThread started')
        self.decrypt()

    def decrypt(self):
        h = Helper()
        not_encrypted = []
        p = './test_files'
        if Config.DEBUG_MODE is False:
            p = str(Path.home())
        pathlist = Path(p).glob('**/*.supergirl')
        for path in pathlist:
            path_in_str = str(path)
            fc = FileCrypter()
            try:
                fc.decrypt_file(path_in_str, self.privkey)
                h.info("Decrypted " + path_in_str)
            except IOError:
                not_encrypted.append(path_in_str)
                h.error("Could not decrypt " + path_in_str)
        #h.safe_exit()
        self.eel.decrypt_success()
