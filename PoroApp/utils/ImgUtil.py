__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/1/2020 5:01 PM'

from PIL import ImageGrab
from PyQt5.QtGui import QImage

from utils.StringUtil import genRandomStr


def loadSingleImgFromPath(path):
    img = QImage()
    img.load(path)
    return img


def loadAllImgFromDirPath(base_path, img_paths):
    img_list = list()
    for path in img_paths:
        img = loadSingleImgFromPath(base_path + path)
        img_list.append(img)
    return img_list


def cropImgByRect(position, save_file=False):
    im = ImageGrab.grab(bbox=(position))
    # to file
    if save_file:
        imgName = genRandomStr() + ".png"
        im.save(imgName)
