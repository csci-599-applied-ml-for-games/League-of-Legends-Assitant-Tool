__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/24/2020 9:28 PM'

import collections
import threading
import time

import win32api
import win32con
import win32gui

from conf.ProfileModelLabel import NONE_LIST
from conf.Settings import KEYBOARD_CATCHER_RATE, LOL_IN_GAME_CLIENT_NAME, TEAM_LEFT_IN_TAB, TEAM_RIGHT_IN_TAB, \
    TEAM_PROFILES, TEAM_GEARS
from model.FaceRecognitionModel import ProfileModel
from model.InGameInfo import UserInGameInfo
from model.ItemDetectionModel import ItemModel
from model.LoLClientHeartBeat import ClientStatus
from utils.CopyPasteUtil import VK_CODE
from utils.ImgUtil import grabImgByRect, split2NPieces, cropImgByRect
from utils.RecommendUtil import itemSuggestion


def expandCropArea(area):
    return (area[0], area[1], area[2] + 405, area[3])


def extractDictValue(data):
    result = list()
    for val in data.values():
        result.extend(list(set(val.get("gears", None)) - set(NONE_LIST)))

    return result


def decodeImgs(enemy_info_img):
    """
    decode img return a list of champ name and his gears
    :param enemy_info_img:
    :return: profile_and_gears
    """
    result = collections.defaultdict(dict)
    profiles_img = cropImgByRect(enemy_info_img, TEAM_PROFILES)
    gears_img = cropImgByRect(enemy_info_img, TEAM_GEARS)

    five_profiles = split2NPieces(profiles_img, interval=21, horizontal=False)
    five_gears = split2NPieces(gears_img, interval=42, horizontal=False)
    five_champ_name = ProfileModel.getInstance().predictImgs(five_profiles)
    five_gear_list = ItemModel.getInstance().predictImgs(five_gears)

    if five_champ_name is not None and five_gear_list is not None:
        for name, gears in zip(five_champ_name, five_gear_list):
            result[name] = {
                "name": name,
                "gears": gears
            }
    return result


class TabKeyListener(threading.Thread):
    _instance_lock = threading.Lock()

    def __init__(self, name, client_info, crop_position):
        threading.Thread.__init__(self)
        self.name = name
        self.client_info = client_info
        self.crop_position = crop_position
        self.__running = threading.Event()  # a event using to stop thread
        self.__running.set()  # set() could enable thread to receive event
        self._capture_rate = KEYBOARD_CATCHER_RATE
        self.left_twice_flag = False
        self.right_twice_flag = False

    def run(self):
        print(self.name + " has started.")
        while self.__running.isSet():
            if self.client_info.getStatusIndex() == ClientStatus.InGame:
                if win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME) != 0 \
                        and win32api.GetAsyncKeyState(win32con.VK_TAB):
                    print("tab was pressed")
                    if UserInGameInfo.getInstance().getEnemyInfoArea() is None:
                        self._instance_lock.acquire()
                        # crop the whole image, since we dont know where is the enemy
                        tab_panel = grabImgByRect(self.crop_position, binarize=False)
                        # 把整张图片切成五份, 但是我们不知道左边是敌人还是右边是敌人，所以需要比较一次
                        teamLeft = cropImgByRect(tab_panel, TEAM_LEFT_IN_TAB)
                        teamRight = cropImgByRect(tab_panel, TEAM_RIGHT_IN_TAB)

                        left_five_imgs = split2NPieces(teamLeft, interval=21, horizontal=False)
                        left_results = ProfileModel.getInstance().predictImgs(left_five_imgs)
                        #
                        right_five_imgs = split2NPieces(teamRight, interval=21, horizontal=False)
                        right_results = ProfileModel.getInstance().predictImgs(right_five_imgs)

                        print("left_results->", left_results)
                        print("right_results->", right_results)
                        # TODO 因为准确率的问题，（不能全部识别对， 所以认对3/5 就算， 实际排位中两方英雄都不一样）
                        if len(set(UserInGameInfo.getInstance().getEnemyTeamList()).difference(
                                set(right_results))) <= 3:
                            if self.right_twice_flag:
                                UserInGameInfo.getInstance().setEnemyInfoArea(TEAM_RIGHT_IN_TAB)
                            self.right_twice_flag = True
                        elif len(set(UserInGameInfo.getInstance().getEnemyTeamList()).intersection(
                                set(left_results))) >= 3:
                            if self.left_twice_flag:
                                UserInGameInfo.getInstance().setEnemyInfoArea(TEAM_LEFT_IN_TAB)
                            self.left_twice_flag = True

                        self._instance_lock.release()

                    else:
                        # once we got to know which is enemy, we can only crop small part of pics
                        enemy_panel_area = UserInGameInfo.getInstance().getEnemyInfoArea()
                        tab_panel = grabImgByRect(self.crop_position, binarize=False)
                        # 从整张图片提取出来敌人的部分
                        enemy_info_img = cropImgByRect(tab_panel, enemy_panel_area)
                        # 在这里还需要截自己的装备
                        self_info_img = None
                        if enemy_panel_area == expandCropArea(TEAM_LEFT_IN_TAB):
                            self_info_img = cropImgByRect(tab_panel, expandCropArea(TEAM_RIGHT_IN_TAB))
                        else:
                            self_info_img = cropImgByRect(tab_panel, expandCropArea(TEAM_LEFT_IN_TAB))

                        enemy_info = decodeImgs(enemy_info_img)
                        if len(set(enemy_info.keys()).intersection(
                                set(UserInGameInfo.getInstance().getEnemyTeamList()))) >= 3:
                            print("enemy_info ->", enemy_info)
                            UserInGameInfo.getInstance().setEnemyInfo(enemy_info)

                        if UserInGameInfo.getInstance().getYourselfChamp() is not None:
                            self_team_info = decodeImgs(self_info_img)
                            print("self_team_info ->", self_team_info)
                            self_champ = UserInGameInfo.getInstance().getYourselfChamp()
                            self_gear = self_team_info.get(self_champ, None)
                            if self_gear is not None:
                                print("self_gear[\"gears\"] ->", self_gear["gears"])
                                UserInGameInfo.getInstance().setYourselfGears(
                                    set(self_gear.get("gears", set())) - set(NONE_LIST))
                                print("output gear = ", UserInGameInfo.getInstance().getYourselfGears())
                                UserInGameInfo.getInstance().setGearDetectedFlag(True)
                            else:
                                # 1. self_champ is wrong
                                # 2. 截取到了地面
                                pass

            time.sleep(self._capture_rate)
            # self._instance_lock.release()

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread


class ShopPKeyListener(threading.Thread):
    _instance_lock = threading.Lock()

    def __init__(self, name, client_info):
        threading.Thread.__init__(self)
        self.name = name
        self.client_info = client_info
        self.__running = threading.Event()  # a event using to stop thread
        self.__running.set()  # set() could enable thread to receive event

    def run(self):
        print(self.name + " has started.")
        while self.__running.isSet():
            if self.client_info.getStatusIndex() == ClientStatus.InGame:
                if win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME) != 0 \
                        and win32api.GetAsyncKeyState(VK_CODE['p']):
                    print("key p was pressed")
                    if UserInGameInfo.getInstance().getEnemyInfoArea() is not None \
                            and UserInGameInfo.getInstance().getYourselfChamp() is not None \
                            and len(UserInGameInfo.getInstance().getEnemyInfo().keys()) > 1:
                        self._instance_lock.acquire()
                        enemy_info = UserInGameInfo.getInstance().getEnemyInfo()
                        self_champion = UserInGameInfo.getInstance().getYourselfChamp()
                        self_position = UserInGameInfo.getInstance().getUserPosition()
                        enemy_gears = extractDictValue(enemy_info)
                        print("key p enemy_gears ->", enemy_gears)
                        print("key p self_champion ->", self_champion)
                        print("key p self_position ->", self_position)
                        recommend_gears = itemSuggestion(self_position, self_champion, enemy_gears)
                        UserInGameInfo.getInstance().setRecommendGears(recommend_gears)

                        self._instance_lock.release()

            time.sleep(1)
            # self._instance_lock.release()

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread
