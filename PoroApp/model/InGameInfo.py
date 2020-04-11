__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/15/2020 3:33 PM'

import collections
import copy
import threading
from queue import PriorityQueue

from conf.ProfileModelLabel import NONE_LIST
from model.GearsInfo import GearsBasicInfo
from utils.RecommendUtil import gen_recommend_champs
from model.ChampInfo import ChampionBasicInfo


# LEFT_BRACKETS = "<img src=\"resources/data/support/22222.png\">"
# # RIGHT_BRACKETS = "<img src=\"resources/data/support/bracket_right.png\">"


def mixedWrapper(champ_name, gears_set):
    champ_img_html = ChampionBasicInfo.getInstance().toImgHtml(champ_name)
    actual_gears = list()
    if gears_set is not None:
        actual_gears = list(set(gears_set) - set(NONE_LIST))
    if len(actual_gears) == 0: actual_gears.append("Nothing")
    gear_img_html = GearsBasicInfo.getInstance().toImgHtml(actual_gears)
    return "<div class=\"mixed\">" + champ_img_html + gear_img_html + "</div><hr/>"


class UserInGameInfo(object):
    """
    玩家游戏数据
    """
    _instance_lock = threading.Lock()
    # banned champs
    enemy_banned_champ_list = set()
    your_side_banned_champ_list = set()

    # recommend champs
    recommend_champ_list = set()

    # in game champs
    enemy_team_champ_list = list()
    # enemy team is left or right in tab panel
    enemy_info_in_table_area = None

    enemy_info = collections.defaultdict(dict)
    # has user enter the game
    in_game_flag = False

    champ_clicked_counter = 0
    gear_clicked_counter = 0
    enlargement_factor = 1.0

    yourself_champ = None
    yourself_gears = None
    gear_detected_flag = False
    gear_recommend_flag = False

    enemy_position_deque = None
    warning_priority_queue = PriorityQueue()

    def __init__(self):
        self.you_twice_flag = False
        self.enemy_twice_flag = False

    def getEnemyPositionDetail(self):
        """
        get or init a deque which saved enemy position info in last 5 sec
        :return: self.enemy_position_deque
        """
        if self.enemy_position_deque is None:
            self.enemy_position_deque = dict()
            for enemy in self.enemy_team_champ_list:
                self.enemy_position_deque[enemy] = collections.deque(maxlen=5)

        return self.enemy_position_deque

    def updateEnemyDeque(self, data_dict: dict):
        """
        update self.enemy_position_deque every sec
        self.user_position "TOP" ,
        :param data_dict: {'Wukong': (38.5, 35.5), 'Cassiopeia': (122.5, 125.5), 'Leona': (229.5, 184.5)}
        :return: {
            'Vayne': deque([], maxlen=5),
            'Leona': deque([(224.5, 179.5), (225.5, 167.5), (227.5, 173.5), (225.5, 177.5), (229.5, 184.5)], maxlen=5),
            'Wukong': deque([(75.5, 27.5), (27.5, 45.5), (30.5, 41.5), (38.5, 35.5)], maxlen=5),
            'Cassiopeia': deque([(131.5, 116.5), (128.5, 120.5), (128.5, 119.5), (127.5, 119.5), (122.5, 125.5)], maxlen=5),
            'Udyr': deque([(23.5, 51.5), (21.5, 56.5), (22.5, 53.5), (28.5, 44.5), (43.5, 31.5)], maxlen=5)
        }
        """
        self.enemy_position_deque = self.getEnemyPositionDetail()

        temp_dict = copy.deepcopy(self.enemy_position_deque)
        for data_key in data_dict.keys():
            if data_key in temp_dict.keys():
                self.enemy_position_deque.get(data_key).append(data_dict.get(data_key))

    def analysisEnemyPosition(self):
        # self.warning_priority_queue
        # from queue import PriorityQueue
        #
        # q = PriorityQueue()
        #
        # q.put((1, 'A','head to you'))
        # q.put((1, 'B','missing'))
        # q.put((3, 'C','idle'))
        #
        # while not q.empty():
        #     next_item = q.get()
        #     print(next_item)

        # 结果：
        #   (1, 'eat')
        #   (2, 'code')
        #   (3, 'sleep')
        pass

    def getWarningInfo(self):
        return self.warning_priority_queue

    def resetGearCounter(self):
        self.gear_clicked_counter = 0

    def setGearDetectedFlag(self, flag=True):
        self.gear_detected_flag = flag

    def getGearDetectedFlag(self):
        return self.gear_detected_flag

    def setGearRecommendFlag(self, flag=True):
        self.gear_recommend_flag = flag

    def getGearRecommendFlag(self):
        return self.gear_recommend_flag

    def setYourselfChamp(self, champ):
        self.yourself_champ = champ

    def getYourselfChamp(self):
        return self.yourself_champ

    def getYourselfChampHTML(self):
        return ChampionBasicInfo.getInstance().toHtml(self.yourself_champ)

    def setYourselfGears(self, gears_info=None):
        self.yourself_gears = gears_info

    def getYourselfGears(self):
        return self.yourself_gears

    def setRecommendGears(self, gears):
        self.gear_recommend_flag = True
        self.recommend_gear_list = gears

    def getRecommendGears(self):
        html_blob = str()
        for gear in self.recommend_gear_list:
            html_str = GearsBasicInfo.getInstance().toHtml(gear)
            html_blob += html_str

        return html_blob

    def getRecommendGearAutoCountList(self):
        result = None
        if self.gear_clicked_counter < len(self.recommend_gear_list):
            result = self.recommend_gear_list[self.gear_clicked_counter]
            self.gear_clicked_counter += 1
        return result

    def getEnemyTeamDetailHTML(self):
        html_blob = str()
        for champ, val in self.enemy_info.items():
            html_str = mixedWrapper(champ, val["gears"])
            html_blob += html_str
        return html_blob

    def getSelfChampAndGearHTML(self):
        return mixedWrapper(self.yourself_champ, self.yourself_gears)

    def setInGameFlag(self):
        self.in_game_flag = True

    def getInGameFlag(self):
        return self.in_game_flag

    def setEnemyInfoArea(self, area):
        expanded_area = (area[0], area[1], area[2] + 405, area[3])
        self.enemy_info_in_table_area = expanded_area

    def getEnemyInfoArea(self):
        return self.enemy_info_in_table_area

    def hasEnemyInfoArea(self):
        return self.enemy_info_in_table_area is not None

    def setEnemyInfo(self, result):
        self.enemy_info = result

    def getEnemyInfo(self):
        return self.enemy_info

    def getEnemyInfoHTML(self):
        html_blob = str()
        for champ in self.enemy_info:
            html_str = ChampionBasicInfo.getInstance().toHtml(champ)
            html_blob += html_str
        return html_blob

    def setUserPosition(self, position):
        self.user_position = position

    def getUserPosition(self):
        return self.user_position

    def hasPositionInfo(self):
        return hasattr(self, "user_position")

    def addBannedChampions(self, champ_names):
        self.your_side_banned_champ_list = champ_names

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

    def getEnemyBannedChampionsSet(self):
        return self.enemy_banned_champ_list

    def addEnemyBannedChampions(self, champ_names):
        self.enemy_banned_champ_list = champ_names

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

            return self.recommend_champ_list

    def getRecommendChampList(self):
        return self.recommend_champ_list

    def getRecommendChampAutoCountList(self):
        result = None
        if self.champ_clicked_counter < len(self.recommend_champ_list):
            result = self.recommend_champ_list[self.champ_clicked_counter][0]
            self.champ_clicked_counter += 1
        return result

    def getRecommendChampListHTML(self):
        html_blob = str()
        if self.recommend_champ_list is not None:
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
        self.yourself_gears = None
        self.your_side_banned_champ_list.clear()
        self.yourself_champ = None
        self.recommend_champ_list.clear()

        self.enemy_banned_champ_list.clear()
        self.enemy_info_in_table_area = None
        self.enemy_team_champ_list.clear()
        self.enemy_info.clear()
        self.enemy_position_deque = None

        self.enlargement_factor = 1.0
        self.champ_clicked_counter = 0
        self.gear_clicked_counter = 0
        self.in_game_flag = False
        self.gear_detected_flag = False
        self.gear_recommend_flag = False

    def resetBannedChampList(self):
        self.your_side_banned_champ_list.clear()

    def resetEnemyBannedChampList(self):
        self.enemy_banned_champ_list.clear()

    def setEnemyTeamList(self, champ_list):
        self.enemy_team_champ_list = champ_list

    def getEnemyTeamList(self):
        return self.enemy_team_champ_list

    def getEnemyTeamListHTML(self):
        html_blob = str()
        for champ in self.enemy_team_champ_list:
            html_str = ChampionBasicInfo.getInstance().toHtml(champ)
            html_blob += html_str
        return html_blob

    def getEnemyTeamListSimpleHTML(self):
        html_blob = str()
        for champ in self.enemy_team_champ_list:
            html_str = ChampionBasicInfo.getInstance().toSimpleHtml(champ)
            html_blob += html_str
        return html_blob

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(UserInGameInfo, "_instance"):
            with UserInGameInfo._instance_lock:
                if not hasattr(UserInGameInfo, "_instance"):
                    UserInGameInfo._instance = UserInGameInfo(*args, **kwargs)
        return UserInGameInfo._instance
