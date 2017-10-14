import requests
from sys import platform
from shutil import copyfile, rmtree
from Helper import Helper
import tempfile
import os
import zipfile
import subprocess
import time
import Config
import psutil

class TorManager:
    def __init__(self):
        self._helper = Helper()
        self.tor_path_linux = tempfile.gettempdir() + "/tor_linux"
        self.tor_path_win = tempfile.gettempdir() + "/tor_win"

    def startProxy(self):
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            self.check(platform)
            self.startLinux()
        elif platform == "win32":
            self.check(platform)
            self.startWindows()
        if Config.DEBUG_MODE is False:
            time.sleep(10)

    def check(self, os):
        name = "tor"
        if os == "win32":
            name += ".exe"
        for proc in psutil.process_iter():
            if proc.name() == name:
                proc.kill()
                self._helper.info("Killed tor...")

    def startLinux(self):
        copyfile(self._helper.path("tor_bin/tor_linux.zip"), self.tor_path_linux + "zip")
        if not os.path.exists(self.tor_path_linux):
            os.makedirs(self.tor_path_linux)
        else:
            rmtree(self.tor_path_linux)
            os.makedirs(self.tor_path_linux)

        # extract the tor_linux.zip
        zip_ref = zipfile.ZipFile(self.tor_path_linux + "zip", 'r')
        zip_ref.extractall(self.tor_path_linux + "/")
        zip_ref.close()

        os.remove(self.tor_path_linux + "zip")
        self.make_executable(self.tor_path_linux + "/tor")
        self.make_executable(self.tor_path_linux + "/start.sh")
        subprocess.call(self.tor_path_linux + "/start.sh")
        self._helper.info("Started Tor")

    def startWindows(self):
        copyfile(self._helper.path("tor_bin/tor_win.zip"), self.tor_path_win + "zip")
        if not os.path.exists(self.tor_path_win):
            os.makedirs(self.tor_path_win)
        else:
            rmtree(self.tor_path_win)
            os.makedirs(self.tor_path_win)

        # extract the tor_linux.zip
        zip_ref = zipfile.ZipFile(self.tor_path_win + "zip", 'r')
        zip_ref.extractall(self.tor_path_win + "/")
        zip_ref.close()
        os.remove(self.tor_path_win + "zip")

        with open(self.tor_path_win + '/Tor/tor.vbs', 'w') as torvbs:
            torvbs.write('Dim WinScriptHost\n')
            torvbs.write('Set WinScriptHost = CreateObject("WScript.Shell")\n')
            torvbs.write(
                'WinScriptHost.Run Chr(34) & "' + self.tor_path_win + '/Tor/tor.bat" & Chr(34), 0\n')
            torvbs.write('Set WinScriptHost = Nothing\n')

        with open(self.tor_path_win + '/Tor/tor.bat', 'w') as torbat:
            torbat.write('@echo off\n')
            torbat.write('start "" /B "' + self.tor_path_win + '/Tor/tor.exe" > nul\n')
        os.system(self.tor_path_win + '/Tor/tor.vbs')
        self._helper.info("Started Tor")

    def getSession(self):
        session = requests.session()
        if Config.DEBUG_MODE is False:
            session.proxies = {'http': 'socks5://127.0.0.1:9050',
                               'https': 'socks5://127.0.0.1:9050'}
        return session

    def make_executable(self, path):
        mode = os.stat(path).st_mode
        mode |= (mode & 0o444) >> 2  # copy R bits to X
        os.chmod(path, mode)
