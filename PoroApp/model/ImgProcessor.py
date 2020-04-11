__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 10:11 PM'

import threading
import time

import win32gui

from conf.ProfileModelLabel import NONE_LIST
from conf.Settings import IMG_CATCHER_RATE, BANNED_CHAMP_SIZE, LOL_IN_GAME_CLIENT_NAME
from model.FaceRecognitionModel import ProfileModel, BanedChampRecognitionModel, MiniMapChampionModel
from model.InGameInfo import UserInGameInfo
from model.LoLClientHeartBeat import ClientStatus
from utils.ImgUtil import grabImgByRect, split2NPieces, find_circles, cropImgsByRects
from utils.PositionUtil import getEnlargementFactor, genRelativePos

local_you_banned_list = set()
local_enemy_banned_list = set()

local_yourself_champ_list = set()
local_yourself_gears_list = set()


class ImgCropType:
    # index 0 to 7
    BAN_5_CHAMP, ENEMY_BAN_5_CHAMP, YOUR_TEAM_5_CHAMP, \
    ENEMY_TEAM_5_CHAMP, USER_S_CHAMP_AREA, USER_S_GEAR_AREA, MINI_MAP = range(7)

    Types = {
        BAN_5_CHAMP: None,
        ENEMY_BAN_5_CHAMP: None,
        YOUR_TEAM_5_CHAMP: None,
        ENEMY_TEAM_5_CHAMP: None,
        USER_S_CHAMP_AREA: None,
        USER_S_GEAR_AREA: None,
        MINI_MAP: None
    }

    @classmethod
    def init(cls):
        cls.Types[cls.BAN_5_CHAMP] = {'index': 0}
        cls.Types[cls.ENEMY_BAN_5_CHAMP] = {'index': 1}
        cls.Types[cls.YOUR_TEAM_5_CHAMP] = {'index': 2}
        cls.Types[cls.ENEMY_TEAM_5_CHAMP] = {'index': 3}
        cls.Types[cls.USER_S_CHAMP_AREA] = {'index': 4}
        cls.Types[cls.USER_S_GEAR_AREA] = {'index': 5}
        cls.Types[cls.MINI_MAP] = {'index': 6}

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
        self.self_ban_check_flag = 0
        self.enemy_ban_check_flag = 0
        self.enemy_team_check_flag = 0
        self.self_champ_check_flag = 0

    @classmethod
    def resetLocalList(cls):
        global local_yourself_champ_list
        global local_yourself_gears_list
        local_yourself_champ_list.clear()
        local_yourself_gears_list.clear()

    def run(self):
        global local_yourself_champ_list
        global local_yourself_gears_list
        print(self.name + " has started.")
        while self.__running.isSet():
            if self.client_info.getStatusIndex() == ClientStatus.ChooseChampion:
                if self.img_crop_type == ImgCropType.BAN_5_CHAMP:
                    # crop the image
                    five_profiles = grabImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = split2NPieces(five_profiles)
                    # 预测五张图片
                    results = BanedChampRecognitionModel.getInstance().predictImgs(five_imgs)
                    print("you  banned->", results)
                    UserInGameInfo.getInstance().addBannedChampions(set(set(results) - set(NONE_LIST)))

                    if UserInGameInfo.getInstance().getBannedChampionsSize() >= BANNED_CHAMP_SIZE:
                        if self.self_ban_check_flag == 2:
                            self.stop()
                        self.self_ban_check_flag += 1

                elif self.img_crop_type == ImgCropType.ENEMY_BAN_5_CHAMP:
                    five_profiles = grabImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = split2NPieces(five_profiles)
                    # 预测五张图片
                    results = BanedChampRecognitionModel.getInstance().predictImgs(five_imgs)
                    print("enemy banned ->", results)
                    UserInGameInfo.getInstance().addEnemyBannedChampions(set(set(results) - set(NONE_LIST)))

                    if UserInGameInfo.getInstance().getEnemyBannedChampionsSize() >= BANNED_CHAMP_SIZE:
                        if self.enemy_ban_check_flag == 2:
                            self.stop()
                        self.enemy_ban_check_flag += 1

            elif self.client_info.getStatusIndex() == ClientStatus.InGame:
                if self.img_crop_type == ImgCropType.YOUR_TEAM_5_CHAMP:
                    five_profiles = grabImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = split2NPieces(five_profiles, interval=20, horizontal=False)
                    # 预测五张图片
                    results = ProfileModel.getInstance().predictImgs(five_imgs)
                    print("your team choose ->", results)

                elif self.img_crop_type == ImgCropType.ENEMY_TEAM_5_CHAMP:
                    five_profiles = grabImgByRect(self.crop_position, binarize=False)
                    # 把整张图片切成五份
                    five_imgs = split2NPieces(five_profiles, interval=20, horizontal=False)
                    # 预测五张图片
                    results = ProfileModel.getInstance().predictImgs(five_imgs)
                    print("enemy team predict result -> ", results)

                    if len(list(set(set(results) - set(NONE_LIST)))) == 5:
                        UserInGameInfo.getInstance().setEnemyTeamList(results)
                        print("enemy team choose ->", results)
                        if self.enemy_team_check_flag == 12:
                            self.stop()
                        self.enemy_team_check_flag += 1

                elif self.img_crop_type == ImgCropType.USER_S_CHAMP_AREA:
                    if win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME) != 0 \
                            and UserInGameInfo.getInstance().hasEnemyInfoArea():
                        rect = win32gui.GetWindowRect(win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME))
                        factor = getEnlargementFactor(rect, "in_game")
                        new_area = genRelativePos(rect, self.crop_position, factor)
                        user_profiles = grabImgByRect(new_area, binarize=False)
                        champ_name = ProfileModel.getInstance().predictSingleImg(user_profiles)
                        local_yourself_champ_list.add(champ_name)
                        if len(local_yourself_champ_list) == 1 and self.self_champ_check_flag == 2:
                            UserInGameInfo.getInstance().setYourselfChamp(champ_name)
                            print("your champ is -> ", champ_name)
                            self.stop()
                        self.self_champ_check_flag += 1

                elif self.img_crop_type == ImgCropType.MINI_MAP:
                    if win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME) != 0 \
                            and UserInGameInfo.getInstance().getYourselfChamp() is not None \
                            and UserInGameInfo.getInstance().getEnemyTeamList() is not None:
                        rect = win32gui.GetWindowRect(win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME))
                        factor = getEnlargementFactor(rect, "in_game")
                        map_area = genRelativePos(rect, self.crop_position, factor)
                        captured_map = None
                        try:
                            captured_map = grabImgByRect(map_area, binarize=False)
                        except:
                            print("something error happened when capturing mini map.")

                        enemy_profile_rect, enemy_positions = find_circles(captured_map)
                        if len(enemy_profile_rect) > 0:
                            enemy_profiles = cropImgsByRects(captured_map,
                                                             enemy_profile_rect)

                            enemy_names = MiniMapChampionModel.getInstance().predictImgs(enemy_profiles)
                            enemy_info = dict(zip(enemy_names, enemy_positions))
                            if len(enemy_info.keys()) > 0:
                                UserInGameInfo.getInstance().updateEnemyDeque(enemy_info)
                                # mock the data,
                                UserInGameInfo.getInstance().mockWarningInfo(enemy_info)

            else:
                # only expect choose champion mode and in game mode
                print("GameMode : ", self.client_info.isGameMode())
                print("You shouldn't be here. ---from ImgCatcherThread.py")

            time.sleep(self._capture_rate)

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread
