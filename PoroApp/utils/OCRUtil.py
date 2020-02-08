__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/6/2020 5:57 PM'

from pytesseract import image_to_string

status = ["Closed", "Loading", "InRoom", "Home", "Profile", "Collection", "TFT", "InGame"]


def img2Str(img=None):
    # 现在先用OCR代替 先把逻辑跑通  然后再用TF模型代替
    strs = image_to_string(img, lang='eng')

    if (None is not strs and strs is ""):
        # print("InRoom")
        return "InRoom"
    elif None is not strs:
        selected_name = strs.split(" ")[-1]
        if selected_name == "PLAY":
            # print("InRoom")
            return "InRoom"
        else:
            print(selected_name)
            return selected_name
