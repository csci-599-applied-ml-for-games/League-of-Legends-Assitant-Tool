__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 3:33 PM'

import time

import win32gui
from PyQt5.QtCore import pyqtSignal, QObject

from conf.Settings import LOL_CLIENT_NAME


class ClientInfo():

    def __init__(self, isAlive):
        self.isAlive = isAlive

    def isAlive(self):
        return self.isAlive

    def setPosition(self, position):
        assert position is not None, "LoL Client Position cannot be None"
        self.position = position

    def getPosition(self):
        return self.position


class ClientHeartBeat(QObject):
    keeper = pyqtSignal(ClientInfo)

    def __init__(self, rate=1):
        super(ClientHeartBeat, self).__init__()
        self._rate = rate

    def __del__(self):
        self.wait()

    def run(self):
        while (True):
            hwnd = win32gui.FindWindow(None, LOL_CLIENT_NAME)
            if hwnd != 0:
                client_info = ClientInfo(True)
                rect = win32gui.GetWindowRect(hwnd)
                client_info.setPosition(rect)
                self.keeper.emit(client_info)
            else:
                self.keeper.emit(ClientInfo(False))  # lol client haven't start yet
            time.sleep(self._rate)
