__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/24/2020 9:28 PM'

import collections
import threading
import time

import win32api
import win32con
import win32gui

from conf.Settings import KEYBOARD_CATCHER_RATE, LOL_IN_GAME_CLIENT_NAME, TEAM_LEFT_IN_TAB, TEAM_RIGHT_IN_TAB, \
    TEAM_PROFILES, TEAM_GEARS
from model.FaceRecognitionModel import ProfileModel
from model.InGameInfo import UserInGameInfo
from model.ItemDetectionModel import ItemModel
from model.LoLClientHeartBeat import ClientStatus
from utils.ImgUtil import grabImgByRect, split2NPieces, cropImgByRect


def decodeImgs(enemy_info_img):
    """
    decode img return a list of champ name and his gears
    :param enemy_info_img:
    :return: profile_and_gears
    """
    result = collections.defaultdict(dict)
    profiles_img = cropImgByRect(enemy_info_img, TEAM_PROFILES)
    gears_img = cropImgByRect(enemy_info_img, TEAM_GEARS, save_file=True)

    five_profiles = split2NPieces(profiles_img, interval=21, horizontal=False)
    five_champ_name = ProfileModel.getInstance().predictImgs(five_profiles)

    five_gears = split2NPieces(gears_img, interval=42, horizontal=False, save_file=True)
    five_gear_list = ItemModel.getInstance().predictImgs(five_gears)

    for name, gears in zip(five_champ_name, five_gear_list):
        result[name] = {
            "name": name,
            "gears": gears
        }
    return result


class KeyBoardCatcher(threading.Thread):
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
                        # crop the whole image, since we dont know where is the enemy
                        tab_panel = grabImgByRect(self.crop_position, binarize=False, save_file=True)
                        # 把整张图片切成五份, 但是我们不知道左边是敌人还是右边是敌人，所以需要比较一次
                        teamLeft = cropImgByRect(tab_panel, TEAM_LEFT_IN_TAB, save_file=True)
                        teamRight = cropImgByRect(tab_panel, TEAM_RIGHT_IN_TAB, save_file=True)

                        left_five_imgs = split2NPieces(teamLeft, interval=21, horizontal=False, save_file=True)
                        left_results = ProfileModel.getInstance().predictImgs(left_five_imgs)
                        #
                        right_five_imgs = split2NPieces(teamRight, interval=21, horizontal=False, save_file=True)
                        right_results = ProfileModel.getInstance().predictImgs(right_five_imgs)

                        print("left_results->", left_results)
                        print("right_results->", right_results)
                        # TODO 因为准确率的问题，（不能全部识别对， 所以认对3/5 就算， 实际排位中两方英雄都不一样）
                        if len(set(UserInGameInfo.getInstance().getEnemyTeamList()).difference(
                                set(right_results))) <= 3:
                            if self.right_twice_flag:
                                UserInGameInfo.getInstance().setEnemyInfoArea(TEAM_RIGHT_IN_TAB)
                                print("set right")
                            self.right_twice_flag = True
                        elif len(set(UserInGameInfo.getInstance().getEnemyTeamList()).difference(
                                set(left_results))) <= 3:
                            if self.left_twice_flag:
                                UserInGameInfo.getInstance().setEnemyInfoArea(TEAM_LEFT_IN_TAB)
                                print("set right")
                            self.left_twice_flag = True

                    else:
                        # once we got to know which is enemy, we can only crop small part of pics
                        enemy_panel_area = UserInGameInfo.getInstance().getEnemyInfoArea()
                        tab_panel = grabImgByRect(self.crop_position, binarize=False)
                        # 把整张图片切成五份, 但是我们不知道左边是敌人还是右边是敌人，所以需要比较一次
                        enemy_info_img = cropImgByRect(tab_panel, enemy_panel_area)
                        # enemy_info = decodeImgs(enemy_info_img)
                        # TODO haven't test yet
                        pass

                time.sleep(self._capture_rate)

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread
