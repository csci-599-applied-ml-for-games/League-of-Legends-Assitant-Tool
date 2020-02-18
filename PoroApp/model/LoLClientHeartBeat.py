__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 3:33 PM'

import time

import win32gui
from PyQt5.QtCore import pyqtSignal, QObject

from conf.Settings import LOL_CLIENT_NAME, LOL_IN_GAME_CLIENT_NAME, STATUS_AREA, LOL_CLIENT_SIZE, POSITION_AREA, \
    POSITION_SET, BP_AREA
from model.InGameInfo import UserInGameInfo
from utils.ImgUtil import cropImgByRect
from utils.OCRUtil import img2Str
from utils.PositionUtil import genRelativePos


class ClientStatus:
    # index 0 to 9
    Closed, Loading, InRoom, Home, Profile, Collection, TFT, CLASH, AssignPosition, ChooseChampion, InGame = range(11)

    Types = {
        Closed: None,
        Loading: None,
        InRoom: None,
        Home: None,
        Profile: None,
        Collection: None,
        TFT: None,
        CLASH: None,
        AssignPosition: None,
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
        cls.Types[cls.CLASH] = {'index': 7, 'client_name': LOL_CLIENT_NAME, 'name': "CLASH"}
        cls.Types[cls.AssignPosition] = {'index': 8, 'client_name': LOL_CLIENT_NAME, 'name': "AssignPosition"}
        cls.Types[cls.ChooseChampion] = {'index': 9, 'client_name': LOL_CLIENT_NAME, 'name': "ChooseChampion"}
        cls.Types[cls.InGame] = {'index': 10, 'client_name': LOL_IN_GAME_CLIENT_NAME, 'name': "InGame"}

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
            "TFT.": 6,
            "TET": 6,
            "CLASH": 7,
            "CHAMPION!": 9,
            "InGame": 10,
            "PLAY": 2,
            "LOADOUT!": 10,
            "BATTLE!": 10,
            "TOP": 8,
            "SUPPORT": 8,
            "BOTTOM": 8,
            "JUNGLE": 8,
            "MID": 8,
            "banning": 9,
            "picking": 9,
            "players": 9,
            "choosing": 9
        }
        return inverted_index.get(status_str, 3)


class ClientInfo:

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
        actual_client_size = (position[2] - position[0], position[3] - position[1])
        self.enlargement_factor = \
            (list(float(actual / default) for default, actual in zip(LOL_CLIENT_SIZE, actual_client_size)))[0]
        self.position = position

    def getEnlargementFactor(self):
        return self.enlargement_factor

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
        if self.status in (ClientStatus.AssignPosition,
                           ClientStatus.ChooseChampion,
                           ClientStatus.InGame):
            return True
        else:
            return False


class ClientHeartBeat(QObject):
    keeper = pyqtSignal(ClientInfo)

    def __init__(self, rate=1):
        super(ClientHeartBeat, self).__init__()
        self._heart_beat_rate = rate
        self.twice_flag = False

    def __del__(self):
        self.wait()

    def run(self):
        while (True):
            # 大厅和游戏进程 名字不同
            lobby_client = win32gui.FindWindow(None, LOL_CLIENT_NAME)
            game_client = win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME)
            if lobby_client != 0 and game_client == 0:
                # 正常逻辑,现在去截张图 然后看页面是什么状态
                rect = win32gui.GetWindowRect(lobby_client)
                # keep the func work properly when user open different size of client,
                # we create a variable called enlargement factor
                enlargement_factor = self._getEnlargementFactor(rect)
                current_status = self._getCurrentStatus(rect, enlargement_factor)
                print("current_status ->", current_status)
                client_info = ClientInfo(True, current_status)
                client_info.setPosition(rect)
                self.keeper.emit(client_info)
            elif game_client != 0:
                # 进入游戏阶段
                print("game mode detected")
                client_info = ClientInfo(True, ClientStatus.InGame)
                rect = win32gui.GetWindowRect(game_client)
                client_info.setPosition(rect)
                self.keeper.emit(client_info)
            else:
                self.keeper.emit(ClientInfo(False))  # lol client haven't start yet
            time.sleep(self._heart_beat_rate)

    def _getEnlargementFactor(self, position):
        actual_client_size = (position[2] - position[0], position[3] - position[1])
        enlargement_factor = \
            (list(float(actual / default) for default, actual in zip(LOL_CLIENT_SIZE, actual_client_size)))[0]
        return enlargement_factor

    def _getCurrentStatus(self, position, factor=1.0):
        client_banner_img = cropImgByRect(
            genRelativePos(position, STATUS_AREA, factor), threshold=200)
        highlight_name = img2Str(client_banner_img)
        print("highlight_name ->", highlight_name)
        # 如果返回的是InRoom 状态， 这时需要额外关注 POSITION_AREA 区域字体的变化
        if highlight_name == "InRoom":
            # 降低阈值 再次判断
            client_banner_img = cropImgByRect(
                genRelativePos(position, BP_AREA, factor), threshold=150)
            twice_title = img2Str(client_banner_img)
            print("twice_title ->", twice_title)
            position_label_img = cropImgByRect(
                genRelativePos(position, POSITION_AREA, factor), threshold=140)
            position = img2Str(position_label_img)

            if (position is not None) and (position != "") and \
                    (position in POSITION_SET):
                # 有位置信息
                print("Assigned user position in ", position)
                UserInGameInfo.getInstance().setPosition(position)
                return ClientStatus.str2Status(position)
            else:
                # 如果没有位置信息
                if twice_title == "InRoom" and not self.twice_flag:
                    self.twice_flag = True
                    return ClientStatus.str2Status("InRoom")
                else:
                    return ClientStatus.str2Status(twice_title)
        else:
            self.twice_flag = False

        return ClientStatus.str2Status(highlight_name)
