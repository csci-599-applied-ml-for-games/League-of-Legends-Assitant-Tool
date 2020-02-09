__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 10:11 PM'

import threading
import time

from conf.Settings import IMG_CATCHER_RATE
from model.LoLClientHeartBeat import ClientStatus
from utils.ImgUtil import cropImgByRect
from utils.OCRUtil import img2Str


class ImgCropType:
    # index 0 to 3
    BAN_5_CHAMP, POSITION_LABEL, TAB_PANEL = range(3)
    Types = {
        BAN_5_CHAMP: None,
        POSITION_LABEL: None,
        TAB_PANEL: None
    }

    @classmethod
    def init(cls):
        cls.Types[cls.BAN_5_CHAMP] = {'index': 0}
        cls.Types[cls.POSITION_LABEL] = {'index': 1}
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
        print("name: " + self.name + " has started.")
        while self.__running.isSet():
            if self.client_info.getStatusIndex() == ClientStatus.ChooseChampion:
                if self.img_crop_type == ImgCropType.BAN_5_CHAMP:
                    # crop the image
                    client_banner_img = cropImgByRect(self.crop_position, binarize=False)
                    print("ready to use model to predict")
                    self.stop()

                elif self.img_crop_type == ImgCropType.POSITION_LABEL:
                    print(self.crop_position)
                    client_banner_img = cropImgByRect(self.crop_position, binarize=True, save_file=True)

                    user_position_in_game = img2Str(client_banner_img)
                    print("ssssssss", user_position_in_game)
                    if user_position_in_game == "AYAY666":
                        self.stop()


            elif self.client_info.getStatusIndex() == ClientStatus.InGame:
                pass

            time.sleep(self._heart_beat_rate)

    def stop(self):
        print("name: " + self.name + " has stopped.")
        self.__running.clear()  # stop this thread
