__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/4/2020 10:30 PM'

import pyscreenshot as ImageGrab
import win32gui

from conf.Settings import LOL_CLIENT_NAME
from view.NotificationWindow import NotificationWindow


def checkLoLIsOpen():
    hwnd = win32gui.FindWindow(None, LOL_CLIENT_NAME)
    return False if 0 == int(hwnd) else True


def getLoLClientPos():
    if checkLoLIsOpen():
        hwnd = win32gui.FindWindow(None, LOL_CLIENT_NAME)
        rect = win32gui.GetWindowRect(hwnd)
        print(rect)
        pos = (rect[0], rect[1])
        size = (rect[2] - rect[0], rect[3] - rect[1])
        return pos, size, rect

    else:
        print("ssssss")
        NotificationWindow.warning('warning',
                                   '<html><head/><body><p><span style=" font-style:italic; color:teal;"><img src="resources/assets/angry/poro-angry-0.png">这是提示文案这是提示文案这是提示文案这是提示文案这是提示<br>文案这是提示文案这是提示文案这是提示文案</span></p></body></html>',
                                   callback=None)
        return None, None, None


def getLoLClientScrrenShot():
    _, _, rect = getLoLClientPos()
    if None is not rect:
        im = ImageGrab.grab(bbox=(rect))
        im.show()
        # to file
        im.save('ssss.png')
