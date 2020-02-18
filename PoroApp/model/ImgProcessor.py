__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 10:11 PM'

import threading
import time

from conf.ProfileModelLabel import NONE_LIST
from conf.Settings import IMG_CATCHER_RATE, BANNED_CHAMP_SIZE
from model.FaceRecognitionModel import ProfileModel
from model.InGameInfo import UserInGameInfo
from model.LoLClientHeartBeat import ClientStatus
from utils.ImgUtil import cropImgByRect, cutIntoFivePieces
from view.NotificationWindow import NotificationWindow

local_you_banned_list = set()
local_enemy_banned_list = set()


class ImgCropType:
    # index 0 to 3
    BAN_5_CHAMP, ENEMY_5_CHAMP, TAB_PANEL = range(3)
    Types = {
        BAN_5_CHAMP: None,
        ENEMY_5_CHAMP: None,
        TAB_PANEL: None
    }

    @classmethod
    def init(cls):
        cls.Types[cls.BAN_5_CHAMP] = {'index': 0}
        cls.Types[cls.ENEMY_5_CHAMP] = {'index': 1}
        cls.Types[cls.TAB_PANEL] = {'index': 2}

    @classmethod
    def type(cls, ntype):
        """
        only work when you call init() first
        :rtype: type's index
        """
        return cls.Types.get(ntype)


class ImgCatcherThread(threading.Thread):
    def __init__(self, name, client_info, crop_type, crop_position):
        threading.Thread.__init__(self)
        self.name = name
        self.client_info = client_info
        self.img_crop_type = ImgCropType.type(crop_type)["index"]
        # print(self.img_crop_type) #{'index': 0}
        self.crop_position = crop_position
        self.__running = threading.Event()  # a event using to stop thread
        self.__running.set()  # set() could enable thread to receive event
        self._heart_beat_rate = IMG_CATCHER_RATE

    def run(self):
        global local_you_banned_list
        global local_enemy_banned_list
        print(self.name + " has started.")
        while self.__running.isSet():
            if self.client_info.getStatusIndex() == ClientStatus.ChooseChampion:
                if self.img_crop_type == ImgCropType.BAN_5_CHAMP:
                    # crop the image
                    five_profiles = cropImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = cutIntoFivePieces(five_profiles)
                    # 预测五张图片
                    results = ProfileModel.getInstance().predictImgs(five_imgs)
                    print("you  ->", results)
                    new_add = list(set(set(results) - set(NONE_LIST)) - set(local_you_banned_list))
                    if len(new_add) > 0:
                        local_you_banned_list.add(new_add[0])
                        print("local_you_banned_list", local_you_banned_list)
                        UserInGameInfo.getInstance().addBannedChampions(new_add[0])

                    if len(local_you_banned_list) == BANNED_CHAMP_SIZE:
                        self.stop()

                elif self.img_crop_type == ImgCropType.ENEMY_5_CHAMP:
                    five_profiles = cropImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = cutIntoFivePieces(five_profiles)
                    # 预测五张图片
                    results = ProfileModel.getInstance().predictImgs(five_imgs)
                    print("enemy ->", results)
                    new_add = list(set(set(results) - set(NONE_LIST)) - set(local_enemy_banned_list))
                    if len(new_add) > 0:
                        local_enemy_banned_list.add(new_add[0])
                        print("local_enemy_banned_list", local_enemy_banned_list)
                        UserInGameInfo.getInstance().addEnemyBannedChampions(new_add[0])

                    if len(local_enemy_banned_list) == BANNED_CHAMP_SIZE:
                        self.stop()

            elif self.client_info.getStatusIndex() == ClientStatus.InGame:
                pass

            else:
                print("GameMode : ", self.client_info.isGameMode())
                print("You shouldn't be here. ---from ImgCatcherThread.py")

            time.sleep(self._heart_beat_rate)

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread
