__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/1/2020 5:01 PM'

from PIL import ImageGrab, ImageEnhance, ImageOps
from PyQt5.QtGui import QImage

from utils.StringUtil import genRandomStr


def binarize_image(img, threshold=200):
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


def cropImgByRect(position, save_file=False):
    img = ImageGrab.grab(bbox=(position))
    img = binarize_image(img)
    # to file
    if save_file:
        imgName = genRandomStr() + ".png"
        img.save(imgName)
    return img
