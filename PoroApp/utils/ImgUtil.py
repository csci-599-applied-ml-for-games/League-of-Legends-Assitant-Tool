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


def grabImgByRect(position, binarize=True, save_file=False, threshold=200):
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


def cropImgByRect(img, position, save_file=False):
    cropped = img.crop(position)
    if save_file:
        imgName = genRandomStr() + ".png"
        cropped.save(imgName)
        print("saved a png file whose name is: ", imgName)
    return cropped


def split2NPieces(img, pieces=5, interval=10, horizontal=True, save_file=False):
    rect_list = []
    five_imgs = []
    if horizontal:
        length = int((img.size[0] - (pieces - 1) * interval) / pieces)
        width = img.size[1]
        for index in range(pieces):
            left = (length + interval) * index
            right = length + left
            rect_list.append((left, 0, right, width))

    else:
        width = img.size[0]
        height = int((img.size[1] - (pieces - 1) * interval) / pieces)
        for index in range(pieces):
            upper = (height + interval) * index
            lower = height + upper
            rect_list.append((0, upper, width, lower))

    for rect in rect_list:
        cropped = img.crop(rect)
        five_imgs.append(cropped)
        if save_file:
            imgName = genRandomStr() + ".png"
            cropped.save(imgName)
            print("saved a png file whose name is: ", imgName)

    return five_imgs


def cut3X2Boxes(img, interval=5, save_file=False):
    rect_list = []
    six_imgs = []
    length = int((img.size[0] - 2 * interval) / 3)
    width = int((img.size[1] - interval) / 2)
    for index in range(3):
        left_upper = (length + interval - 1) * index
        right_upper = length + left_upper
        upper_img = (left_upper, 0, right_upper, width)
        lower_img = (left_upper, width + interval, right_upper, 2 * width + interval)
        rect_list.append(upper_img)
        rect_list.append(lower_img)

    for rect in rect_list:
        cropped = img.crop(rect)
        six_imgs.append(cropped)
        if save_file:
            imgName = genRandomStr() + ".png"
            cropped.save(imgName)
            print("saved a png file whose name is: ", imgName)

    return six_imgs
