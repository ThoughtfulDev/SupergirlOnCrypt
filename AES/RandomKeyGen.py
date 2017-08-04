import os

class RandomKeyGen:
    def __init__(self):
        self.key = os.urandom(32)
        self.iv = os.urandom(16)

    def getKey(self):
        return self.key, self.iv
