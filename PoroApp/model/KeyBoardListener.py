__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/24/2020 9:28 PM'

import threading
import time

import win32api
import win32con
import win32gui

from conf.Settings import KEYBOARD_CATCHER_RATE, LOL_IN_GAME_CLIENT_NAME
from model.LoLClientHeartBeat import ClientStatus
from utils.ImgUtil import cropImgByRect


class KeyBoardCatcher(threading.Thread):
    def __init__(self, name, client_info, crop_position):
        threading.Thread.__init__(self)
        self.name = name
        self.client_info = client_info
        self.crop_position = crop_position
        self.__running = threading.Event()  # a event using to stop thread
        self.__running.set()  # set() could enable thread to receive event
        self._capture_rate = KEYBOARD_CATCHER_RATE

    def run(self):
        print(self.name + " has started.")
        while self.__running.isSet():
            if self.client_info.getStatusIndex() == ClientStatus.InGame:
                if win32gui.FindWindow(None, LOL_IN_GAME_CLIENT_NAME) != 0 \
                        and win32api.GetAsyncKeyState(win32con.VK_TAB):
                    print("tab was pressed")
                    # crop the image
                    tab_panel = cropImgByRect(self.crop_position, save_file=True, binarize=False)
                    # # 把整张图片切成五份
                    # five_imgs = cutIntoFivePieces(five_profiles)
                    # # 预测五张图片
                    # results = ProfileModel.getInstance().predictImgs(five_imgs)
                    # print("you  ->", results)
                    # new_add = list(set(set(results) - set(NONE_LIST)) - set(local_you_banned_list))
                    # if len(new_add) > 0:
                    #     local_you_banned_list.add(new_add[0])
                    #     print("local_you_banned_list", local_you_banned_list)
                    #     UserInGameInfo.getInstance().addBannedChampions(new_add[0])
                    #
                    # if len(local_you_banned_list) == BANNED_CHAMP_SIZE:
                    #     self.stop()
                time.sleep(self._capture_rate)

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread
