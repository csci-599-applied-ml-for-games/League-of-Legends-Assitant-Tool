__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/6/2020 5:57 PM'

from pytesseract import image_to_string

from conf.Settings import POSITION_SET
from utils.ImgUtil import binarize_processing


def img2Str(img=None):
    # 现在先用OCR代替 先把逻辑跑通  然后再用TF模型代替
    strs = image_to_string(img, lang='eng')

    if strs is "":
        return "InRoom"

    elif None is not strs:
        selected_name = strs.split(" ")[-1]
        if selected_name == "PLAY":
            return "InRoom"
        else:
            return selected_name


def decodePositionLabelImg(img=None):
    """
    25 是 POSITION_SET 的大小
    0 针对的是 CUSTOM ROOM 页面
    :param img:
    :return:
    """
    pos_labels = image_to_string(img, lang='eng')
    print("pos_labels ->", pos_labels)
    if (pos_labels is not None) and (25 > len(pos_labels) > 10):
        other_poss = set(x for x in pos_labels.split("\n") if x != '')
        return tuple(set(POSITION_SET) - other_poss)[0]
