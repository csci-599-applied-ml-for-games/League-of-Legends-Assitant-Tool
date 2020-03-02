__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0
__update__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/4/2020 9:42 PM'

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from colormap import rgb2hex

from model.NotificationIcon import NotificationIcon
from model.NotificationItem import NotificationItem


class NotificationWindow(QListWidget):
    _instance = None

    def __init__(self, *args, **kwargs):
        super(NotificationWindow, self).__init__(*args, **kwargs)
        self.setSpacing(4)
        self.setMinimumWidth(412)
        self.setMaximumWidth(412)
        QApplication.instance().setQuitOnLastWindowClosed(True)
        # 隐藏任务栏,无边框,置顶等
        self.setWindowFlags(self.windowFlags() | Qt.Tool |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 去掉窗口边框
        self.setFrameShape(self.NoFrame)
        # 背景透明
        self.viewport().setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 不显示滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 获取屏幕高宽
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.setMinimumHeight(rect.height())
        self.setMaximumHeight(rect.height())
        self.move(rect.width() - self.minimumWidth() - 20, 20)

    def removeItem(self, item):
        w = self.itemWidget(item)
        self.removeItemWidget(item)
        item = self.takeItem(self.indexFromItem(item).row())
        w.close()
        w.deleteLater()
        del item

    @classmethod
    def saveLastMessage(cls, message):
        cls.last_message = message

    @classmethod
    def getLastMessage(cls):
        return cls.last_message

    @classmethod
    def _createInstance(cls):
        if not cls._instance:
            cls._instance = NotificationWindow()
            cls._instance.show()
            NotificationIcon.init()
        return cls._instance

    @classmethod
    def info(cls, title, message, callback=None, disabled=False):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Info, callback=callback,
                             bg_color=QColor(237, 242, 252),
                             msg_color=rgb2hex(144, 147, 153))
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)
        cls.saveLastMessage(message)

    @classmethod
    def last(cls, callback=None, disabled=False):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem("The Last Message", cls.getLastMessage(), item, cls._instance,
                             ntype=NotificationIcon.Info, callback=callback,
                             bg_color=QColor(237, 242, 252),
                             msg_color=rgb2hex(144, 147, 153))
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)
        cls.saveLastMessage(cls.getLastMessage())

    @classmethod
    def success(cls, title, message, callback=None, disabled=False):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Success, callback=callback,
                             bg_color=QColor(240, 249, 235),
                             msg_color=rgb2hex(103, 194, 58))
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)
        cls.saveLastMessage(message)

    @classmethod
    def warning(cls, title, message, callback=None, disabled=False):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item, cls._instance,
                             ntype=NotificationIcon.Warning, callback=callback,
                             bg_color=QColor(253, 246, 236),
                             msg_color=rgb2hex(230, 162, 60))
        w.closed.connect(cls._instance.removeItem)
        item.setSizeHint(QSize(cls._instance.width() -
                               cls._instance.spacing(), w.height()))
        cls._instance.setItemWidget(item, w)
        cls.saveLastMessage(message)

    @classmethod
    def error(cls, title, message, callback=None, disabled=False):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item,
                             ntype=NotificationIcon.Error, callback=callback,
                             bg_color=QColor(254, 240, 240),
                             msg_color=rgb2hex(245, 108, 108))
        w.closed.connect(cls._instance.removeItem)
        width = cls._instance.width() - cls._instance.spacing()
        item.setSizeHint(QSize(width, w.height()))
        cls._instance.setItemWidget(item, w)
        cls.saveLastMessage(message)

    @classmethod
    def detect(cls, title, message, callback=None, disabled=False):

        if not disabled:
            cls._createInstance()
            item = QListWidgetItem(cls._instance)
            w = NotificationItem(title, message, item,
                                 ntype=NotificationIcon.Detect, callback=callback,
                                 bg_color=QColor(7, 73, 83),
                                 msg_color=rgb2hex(244, 244, 244))
            w.closed.connect(cls._instance.removeItem)
            width = cls._instance.width() - cls._instance.spacing()
            item.setSizeHint(QSize(width, w.height()))
            cls._instance.setItemWidget(item, w)
            cls.saveLastMessage(message)

    @classmethod
    def threat(cls, title, message, callback=None, disabled=False):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item,
                             ntype=NotificationIcon.Detect, callback=callback,
                             bg_color=QColor(150, 30, 42),
                             msg_color=rgb2hex(244, 244, 244))
        w.closed.connect(cls._instance.removeItem)
        width = cls._instance.width() - cls._instance.spacing()
        item.setSizeHint(QSize(width, w.height()))
        cls._instance.setItemWidget(item, w)
        cls.saveLastMessage(message)

    @classmethod
    def suggest(cls, title, message, callback=None, disabled=False):
        cls._createInstance()
        item = QListWidgetItem(cls._instance)
        w = NotificationItem(title, message, item,
                             ntype=NotificationIcon.Suggest, callback=callback,
                             bg_color=QColor(1, 10, 19),
                             msg_color=rgb2hex(244, 244, 244))
        w.closed.connect(cls._instance.removeItem)
        width = cls._instance.width() - cls._instance.spacing()
        item.setSizeHint(QSize(width, w.height()))
        cls._instance.setItemWidget(item, w)
        cls.saveLastMessage(message)
