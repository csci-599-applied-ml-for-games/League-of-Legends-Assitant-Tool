__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/1/2020 5:01 PM'

from PIL import ImageGrab, ImageEnhance, ImageOps
from PyQt5.QtGui import QImage

from utils.StringUtil import genRandomStr


# 二值化图片
def binarize_processing(img, threshold=200):
    img = img.convert('L')
    img = img.point(lambda p: p > threshold and 255)
    # Contrast
    img = ImageEnhance.Contrast(img)
    img = img.enhance(1.5)
    # invert color black-> white
    return ImageOps.invert(img)


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


def cropImgByRect(position, binarize=True, save_file=False, threshold=200):
    img = ImageGrab.grab(bbox=(position))
    if binarize:
        img = binarize_processing(img, threshold)
    # to file
    if save_file:
        imgName = genRandomStr() + ".png"
        img.save(imgName)
        print("saved a png file whose name is: ", imgName)
    return img
