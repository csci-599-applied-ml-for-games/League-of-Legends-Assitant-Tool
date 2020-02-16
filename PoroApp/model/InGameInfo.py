__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/15/2020 3:33 PM'

import threading


class UserInGameInfo(object):
    """
    玩家游戏数据
    """
    _instance_lock = threading.Lock()
    enemy_banned_champ_list = []
    your_side_banned_champ_list = []

    def __init__(self):
        pass

    def setPosition(self, position):
        self.user_position = position

    def getPosition(self):
        return self.user_position

    def hasPositionInfo(self):
        return hasattr(self, "user_position")

    def addChampions(self, position):
        # TODO
        self.user_position = position

    def getBannedChampList(self):
        return self.user_position

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(UserInGameInfo, "_instance"):
            with UserInGameInfo._instance_lock:  # 为了保证线程安全在内部加锁
                if not hasattr(UserInGameInfo, "_instance"):
                    UserInGameInfo._instance = UserInGameInfo(*args, **kwargs)
        return UserInGameInfo._instance
