import Config
import os
import sys
import logging
import psutil


class Helper:
    def __init__(self):
        if Config.DEBUG_MODE is True:
            logging.basicConfig(filename='log', level=Config.LOG_LEVEL, format='[%(asctime)s][%(levelname)s]: %(message)s')

    def debug(self, text):
        if Config.DEBUG_MODE is True:
            logging.debug(text)

    def warning(self, text):
        if Config.DEBUG_MODE is True:
            logging.warning(text)

    def error(self, text):
        if Config.DEBUG_MODE is True:
            logging.error(text)

    def info(self, text):
        if Config.DEBUG_MODE is True:
            logging.info(text)

    def path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def write_file(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)
            f.close()

    def safe_exit(self):
        os = sys.platform
        name = "tor"
        if os == "win32":
            name += ".exe"
        for proc in psutil.process_iter():
            if proc.name() == name:
                proc.kill()
                self.info("Killed tor...")
        sys.exit(0)

    def supergirl_pic(self):
        print('                                               d8b       888')
        print('                                               Y8P       888')
        print('                                                         888')
        print('.d8888b 888  88888888b.  .d88b. 888d888 .d88b. 888888d888888')
        print('88K     888  888888 "88bd8P  Y8b888P"  d88P"88b888888P"  888')
        print('"Y8888b.888  888888  88888888888888    888  888888888    888')
        print('     X88Y88b 888888 d88PY8b.    888    Y88b 888888888    888')
        print(' 88888P\' "Y8888888888P"  "Y8888 888     "Y88888888888    888')
        print('                888                         888              ')
        print('                888                    Y8b d88P              ')
        print('                888                     "Y88P"               ')

    def super_logo(self):
        print('             \t\t\t,,########################################,,\n\
                          .*##############################################*\n\
                        ,*####*:::*########***::::::::**######:::*###########,\n\
                      .*####:    *#####*.                 :*###,.#######*,####*.\n\
                     *####:    *#####*                      .###########*  ,####*\n\
                  .*####:    ,#######,                        ##########*    :####*\n\
                  *####.    :#########*,                       ,,,,,,,,.      ,####:\n\
                    ####*  ,##############****************:,,               .####*\n\
                     :####*#####################################**,        *####.\n\
                       *############################################*,   :####:\n\
                        .#############################################*,####*\n\
                          :#####:*****#####################################.\n\
                            *####:                  .,,,:*****###########,\n\
                             .*####,                            *######*\n\
                               .####* :*#######*               ,#####*\n\
                                 *###############*,,,,,,,,::**######,\n\
                                   *##############################:\n\
                                     *####*****##########**#####*\n\
                                      .####*.            :####*\n\
                                        :####*         .#####,\n\
                                          *####:      *####:\n\
                                           .*####,  *####*\n\
                                             :####*####*\n\
                                               *######,\n\
                                                 *##,')
