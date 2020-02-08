__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 3:33 PM'

import time

import win32gui
from PyQt5.QtCore import pyqtSignal, QObject

from conf.Settings import LOL_CLIENT_NAME, LOL_IN_GAME_CLIENT_NAME
from utils.ImgUtil import cropImgByRect
from utils.OCRUtil import img2Str


class ClientStatus():
    # index 0 to 6
    Closed, Loading, InRoom, Home, Profile, Collection, TFT, ChooseChampion, InGame = range(9)
    Types = {
        Closed: None,
        Loading: None,
        InRoom: None,
        Home: None,
        Profile: None,
        Collection: None,
        TFT: None,
        ChooseChampion: None,
        InGame: None
    }

    @classmethod
    def init(cls):
        # icon img -> base64
        cls.Types[cls.Closed] = {'index': 0, 'client_name': LOL_CLIENT_NAME, 'name': "Closed"}
        cls.Types[cls.Loading] = {'index': 1, 'client_name': LOL_CLIENT_NAME, 'name': "Loading"}
        cls.Types[cls.InRoom] = {'index': 2, 'client_name': LOL_CLIENT_NAME, 'name': "InRoom"}
        cls.Types[cls.Home] = {'index': 3, 'client_name': LOL_CLIENT_NAME, 'name': "Home"}
        cls.Types[cls.Profile] = {'index': 4, 'client_name': LOL_CLIENT_NAME, 'name': "Profile"}
        cls.Types[cls.Collection] = {'index': 5, 'client_name': LOL_CLIENT_NAME, 'name': "Collection"}
        cls.Types[cls.TFT] = {'index': 6, 'client_name': LOL_CLIENT_NAME, 'name': "TFT"}
        cls.Types[cls.ChooseChampion] = {'index': 7, 'client_name': LOL_CLIENT_NAME, 'name': "ChooseChampion"}
        cls.Types[cls.InGame] = {'index': 8, 'client_name': LOL_IN_GAME_CLIENT_NAME, 'name': "InGame"}

    @classmethod
    def status(cls, ntype):
        # only work when you call init() first
        return cls.Types.get(ntype)

    @classmethod
    def str2Status(cls, status_str: str) -> object:
        inverted_index = {
            "closed": 0,
            "Loading": 1,
            "InRoom": 2,
            "HOME": 3,
            "PROFILE": 4,
            "COLLECTION": 5,
            "TFT": 6,
            "CHAMPION!": 7,
            "InGame": 8,
            "PLAY": 2
        }
        return inverted_index.get(status_str, 3)


class ClientInfo():

    def __init__(self, isAlive, status=None):
        self.isAlive = isAlive
        if None is status:
            self.status = ClientStatus.Loading if isAlive else ClientStatus.Closed
        else:
            self.status = status

    def hasAlive(self):
        return self.isAlive

    def setPosition(self, position):
        assert position is not None, "LoL Client Position cannot be None"
        self.position = position

    def getPosition(self):
        return self.position

    def getStatusIndex(self):
        return self.status

    def getStatus(self):
        return ClientStatus.status(self.status)

    def __str__(self):
        return "ClientInfo { 'isAlive' : '" + str(self.isAlive) + "', " + \
               "'Status' : '" + str(ClientStatus.status(self.status)) + "', " + \
               "'Position' : '" + str(self.position) + "'"

    def isGameMode(self):
        if self.status in (ClientStatus.ChooseChampion, ClientStatus.InGame):
            return True
        else:
            return False


class ClientHeartBeat(QObject):
    keeper = pyqtSignal(ClientInfo)

    def __init__(self, rate=1):
        super(ClientHeartBeat, self).__init__()
        self._rate = rate

    def __del__(self):
        self.wait()

    def run(self):
        while (True):
            # 大厅和游戏进程 名字不同
            lobby_client = win32gui.FindWindow(None, LOL_CLIENT_NAME)
            game_client = win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME)
            if lobby_client != 0:
                # 正常逻辑,现在去截张图 然后看页面是什么状态
                rect = win32gui.GetWindowRect(lobby_client)
                current_status = self._getCurrentStatus(rect)
                client_info = ClientInfo(True, current_status)
                client_info.setPosition(rect)
                self.keeper.emit(client_info)
            elif game_client != 0:
                client_info = ClientInfo(True, ClientStatus.InGame)
                rect = win32gui.GetWindowRect(game_client)
                client_info.setPosition(rect)
                self.keeper.emit(client_info)
            else:
                self.keeper.emit(ClientInfo(False))  # lol client haven't start yet
            time.sleep(self._rate)

    def _getCurrentStatus(self, position):
        # only crop image in 600 * 80 area
        client_banner_img = cropImgByRect((position[0] + 50, position[1] + 20, position[0] + 840, position[1] + 52))
        highlight_name = img2Str(client_banner_img)
        return ClientStatus.str2Status(highlight_name)
