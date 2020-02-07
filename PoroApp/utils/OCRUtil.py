__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/6/2020 5:57 PM'

import random

status = ["Home", "Profile", "Collection", "TFT"]


def img2Str(img=None):
    # 现在先用OCR代替 先把逻辑跑通  然后再用TF模型代替
    # print(image_to_string(Image.open('3131.png'), lang='eng'))
    ranInt = random.randint(0, 1)
    return status[ranInt]
