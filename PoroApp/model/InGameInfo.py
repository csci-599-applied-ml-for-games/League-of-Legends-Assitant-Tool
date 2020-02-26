__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/15/2020 3:33 PM'

import threading

from utils.RecommendUtil import gen_recommend_champs
from view.NotificationWindow import NotificationWindow
from model.ChampInfo import ChampionBasicInfo


class UserInGameInfo(object):
    """
    玩家游戏数据
    """
    _instance_lock = threading.Lock()
    enemy_banned_champ_list = set()
    your_side_banned_champ_list = set()
    recommend_champ_list = set()

    clicked_counter = 0
    enlargement_factor = 1.0

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

    def getBannedChampListHTML(self):
        html_blob = str()
        for champ in self.your_side_banned_champ_list:
            html_str = ChampionBasicInfo.getInstance().toHtml(champ)
            html_blob += html_str
        return html_blob

    def getEnemyBannedChampionsSize(self):
        return len(self.enemy_banned_champ_list)

    def addEnemyBannedChampions(self, champ_name):
        self.enemy_banned_champ_list.add(champ_name)

    def getEnemyBannedChampListHTML(self):
        html_blob = str()
        for champ in self.enemy_banned_champ_list:
            html_str = ChampionBasicInfo.getInstance().toHtml(champ)
            html_blob += html_str
        return html_blob

    def initRecommendChampList(self):
        if self.recommend_champ_list is None or len(self.recommend_champ_list) == 0:
            self.recommend_champ_list = gen_recommend_champs(
                list(self.enemy_banned_champ_list),
                self.user_position,
                list(self.enemy_banned_champ_list.union(
                    self.your_side_banned_champ_list)))

    def getRecommendChampList(self):
        return self.recommend_champ_list

    def getRecommendChampAutoCountList(self):
        result = None
        if self.clicked_counter < len(self.recommend_champ_list):
            result = self.recommend_champ_list[self.clicked_counter][0]
            self.clicked_counter += 1
        return result

    def getRecommendChampListHTML(self):
        html_blob = str()
        for champ in self.recommend_champ_list:
            html_str = ChampionBasicInfo.getInstance().toHtml(champ[0], champ[1])
            html_blob += html_str
        return html_blob

    def setEnlargementFactor(self, value):
        self.enlargement_factor = value

    def getEnlargementFactor(self):
        return self.enlargement_factor

    def getYourFlag(self):
        return self.you_twice_flag

    def setYourFlag(self, bool_val):
        self.you_twice_flag = bool_val

    def getEnemyFlag(self):
        return self.enemy_twice_flag

    def setEnemyFlag(self, bool_val):
        self.enemy_twice_flag = bool_val

    def resetAll(self):
        self.your_side_banned_champ_list.clear()
        self.enemy_banned_champ_list.clear()
        self.recommend_champ_list.clear()
        self.clicked_counter = 0

    def resetBannedChampList(self):
        self.your_side_banned_champ_list.clear()

    def resetEnemyBannedChampList(self):
        self.enemy_banned_champ_list.clear()

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(UserInGameInfo, "_instance"):
            with UserInGameInfo._instance_lock:
                if not hasattr(UserInGameInfo, "_instance"):
                    UserInGameInfo._instance = UserInGameInfo(*args, **kwargs)
        return UserInGameInfo._instance
