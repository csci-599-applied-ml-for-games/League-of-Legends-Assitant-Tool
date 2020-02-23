__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/15/2020 3:33 PM'

import threading

from view.NotificationWindow import NotificationWindow
from model.ChampInfo import ChampionBasicInfo


class UserInGameInfo(object):
    """
    玩家游戏数据
    """
    _instance_lock = threading.Lock()
    enemy_banned_champ_list = set()
    your_side_banned_champ_list = set()

    def __init__(self):
        self.you_twice_flag = False
        self.enemy_twice_flag = False

    def setPosition(self, position, msg=None):
        self.user_position = position
        if msg is not None:
            NotificationWindow.detect('BP Champion Session',
                                      "You has been assigned in <u><b>TOP</b></u> position. <br/> Tips: {}".format(
                                          msg),
                                      callback=None)
        else:
            NotificationWindow.detect('BP Champion Session',
                                      "You has been assigned in <u><b>TOP</b></u> position",
                                      callback=None)

    def getPosition(self):
        return self.user_position

    def hasPositionInfo(self):
        return hasattr(self, "user_position")

    def addBannedChampions(self, champ_name):
        self.your_side_banned_champ_list.add(champ_name)

    def getBannedChampionsSize(self):
        return len(self.your_side_banned_champ_list)

    def getBannedChampList(self):
        html_blob = str()
        for champ in self.your_side_banned_champ_list:
            html_str = ChampionBasicInfo.getInstance().toHtml(champ)
            html_blob += html_str
        print("html_blob -> ", html_blob)
        return html_blob

    def getEnemyBannedChampionsSize(self):
        return len(self.enemy_banned_champ_list)

    def addEnemyBannedChampions(self, champ_name):
        self.enemy_banned_champ_list.add(champ_name)

    def getEnemyBannedChampList(self):
        return self.enemy_banned_champ_list

    def getYourFlag(self):
        return self.you_twice_flag

    def setYourFlag(self, bool_val):
        self.you_twice_flag = bool_val

    def getEnemyFlag(self):
        return self.enemy_twice_flag

    def setEnemyFlag(self, bool_val):
        self.enemy_twice_flag = bool_val

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(UserInGameInfo, "_instance"):
            with UserInGameInfo._instance_lock:
                if not hasattr(UserInGameInfo, "_instance"):
                    UserInGameInfo._instance = UserInGameInfo(*args, **kwargs)
        return UserInGameInfo._instance
