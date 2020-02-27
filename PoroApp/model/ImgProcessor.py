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

local_you_banned_list = set()
local_enemy_banned_list = set()


class ImgCropType:
    # index 0 to 3
    BAN_5_CHAMP, ENEMY_BAN_5_CHAMP, YOUR_TEAM_5_CHAMP, ENEMY_TEAM_5_CHAMP = range(4)
    Types = {
        BAN_5_CHAMP: None,
        ENEMY_BAN_5_CHAMP: None,
    }

    @classmethod
    def init(cls):
        cls.Types[cls.BAN_5_CHAMP] = {'index': 0}
        cls.Types[cls.ENEMY_BAN_5_CHAMP] = {'index': 1}
        cls.Types[cls.YOUR_TEAM_5_CHAMP] = {'index': 2}
        cls.Types[cls.ENEMY_TEAM_5_CHAMP] = {'index': 3}

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
        self.crop_position = crop_position
        self.__running = threading.Event()  # a event using to stop thread
        self.__running.set()  # set() could enable thread to receive event
        self._capture_rate = IMG_CATCHER_RATE

    @classmethod
    def resetLocalList(cls):
        global local_you_banned_list
        global local_enemy_banned_list
        local_you_banned_list.clear()
        local_enemy_banned_list.clear()

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
                    print("you  banned->", results)
                    new_add = list(set(set(results) - set(NONE_LIST)) - set(local_you_banned_list))
                    if len(new_add) > 0:
                        local_you_banned_list.add(new_add[0])
                        UserInGameInfo.getInstance().addBannedChampions(new_add[0])

                    if len(local_you_banned_list) == BANNED_CHAMP_SIZE:
                        self.stop()

                elif self.img_crop_type == ImgCropType.ENEMY_BAN_5_CHAMP:
                    five_profiles = cropImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = cutIntoFivePieces(five_profiles)
                    # 预测五张图片
                    results = ProfileModel.getInstance().predictImgs(five_imgs)
                    print("enemy banned ->", results)
                    new_add = list(set(set(results) - set(NONE_LIST)) - set(local_enemy_banned_list))
                    if len(new_add) > 0:
                        local_enemy_banned_list.add(new_add[0])
                        UserInGameInfo.getInstance().addEnemyBannedChampions(new_add[0])

                    if len(local_enemy_banned_list) == BANNED_CHAMP_SIZE:
                        self.stop()

            elif self.client_info.getStatusIndex() == ClientStatus.InGame:
                if self.img_crop_type == ImgCropType.YOUR_TEAM_5_CHAMP:
                    five_profiles = cropImgByRect(self.crop_position, save_file=True, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = cutIntoFivePieces(five_profiles, interval=20, horizontal=True)
                    # 预测五张图片
                    results = ProfileModel.getInstance().predictImgs(five_imgs)
                    print("your team choose ->", results)

                elif self.img_crop_type == ImgCropType.ENEMY_TEAM_5_CHAMP:
                    five_profiles = cropImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = cutIntoFivePieces(five_profiles, interval=20, horizontal=True)
                    # 预测五张图片
                    results = ProfileModel.getInstance().predictImgs(five_imgs)
                    # TODO 之所以加Urgot 是因为Unselected总是识别失败
                    if len(list(set(results) - set(NONE_LIST) - set("Urgot"))) == 5:
                        UserInGameInfo.getInstance().setEnemyTeamList(results)
                        print("enemy team choose ->", results)
                        self.stop()

            else:
                # only expect choose champion mode and in game mode
                print("GameMode : ", self.client_info.isGameMode())
                print("You shouldn't be here. ---from ImgCatcherThread.py")

            time.sleep(self._capture_rate)

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread
