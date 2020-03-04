__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/25/2020 10:39 PM'

import time
from ctypes import *

import win32api
import win32con

VK_CODE = {
    'backspace': 0x08,
    ' ': 0x20,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
    '`': 0xC0}


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def mouse_click(x=None, y=None):
    if not x is None and not y is None:
        _mouse_move(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def _mouse_move(x, y):
    windll.user32.SetCursorPos(x, y)


def input_a_str(str=''):
    for _ in range(14):
        win32api.keybd_event(VK_CODE["backspace"], 0, 0, 0)
        win32api.keybd_event(VK_CODE["backspace"], 0, win32con.KEYEVENTF_KEYUP, 0)

    for c in str:
        win32api.keybd_event(VK_CODE[c], 0, 0, 0)
        win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)


def pasteToSearchBox(point, value):
    mouse_click(int(point[0]), int(point[1]))
    input_a_str(value.lower())
