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
    # need to binarize or not
    if binarize:
        img = binarize_processing(img, threshold)
    # save to file
    if save_file:
        imgName = genRandomStr() + ".png"
        img.save(imgName)
        print("saved a png file whose name is: ", imgName)
    return img


def cutIntoFivePieces(img, interval=10, horizontal=False):
    rect_list = []
    five_imgs = []
    if not horizontal:
        length = int((img.size[0] - 4 * interval) / 5)
        width = img.size[1]
        for index in range(5):
            left = (length + interval) * index
            right = length + left
            rect_list.append((left, 0, right, width))

    else:
        width = img.size[0]
        height = int((img.size[1] - 4 * interval) / 5)
        for index in range(5):
            upper = (height + interval) * index
            lower = width + upper
            rect_list.append((0, upper, width, lower))

    for rect in rect_list:
        cropped = img.crop(rect)
        five_imgs.append(cropped)

    return five_imgs
