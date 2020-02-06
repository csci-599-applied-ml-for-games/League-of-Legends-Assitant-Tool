__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0
__update__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/3/2020 10:22 PM'

from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QPainterPath, \
    QColor
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, \
    QGridLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, \
    QListWidgetItem

from model.NotificationIcon import NotificationIcon


class NotificationItem(QWidget):
    closed = pyqtSignal(QListWidgetItem)
    BackgroundColor = QColor(195, 195, 195)
    BorderColor = QColor(150, 150, 150)

    def __init__(self, title, message, item, *args, ntype=0, callback=None, **kwargs):
        super(NotificationItem, self).__init__(*args, **kwargs)
        self.item = item
        self.callback = callback
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # notification item background widget
        self.bgWidget = QWidget(self)
        layout.addWidget(self.bgWidget)

        layout = QGridLayout(self.bgWidget)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        layout.addWidget(
            QLabel(self, pixmap=NotificationIcon.icon(ntype)), 0, 0)

        # title
        self.labelTitle = QLabel(title, self)
        font = self.labelTitle.font()
        font.setBold(True)
        font.setPixelSize(15)
        self.labelTitle.setFont(font)

        # close button
        self.labelClose = QLabel(
            self, cursor=Qt.PointingHandCursor, pixmap=NotificationIcon.icon(NotificationIcon.Close))

        # notification message content
        self.labelMessage = QLabel(
            message, self, cursor=Qt.PointingHandCursor, wordWrap=True, alignment=Qt.AlignLeft | Qt.AlignTop)
        font = self.labelMessage.font()
        font.setPixelSize(15)
        self.labelMessage.setFont(font)
        self.labelMessage.adjustSize()

        # add to the grid layout
        layout.addWidget(self.labelTitle, 0, 1)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2)
        layout.addWidget(self.labelClose, 0, 3)
        layout.addWidget(self.labelMessage, 1, 1, 1, 2)

        # 边框阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setColor(QColor(0, 0, 0, 25))
        effect.setOffset(0, 2)
        self.setGraphicsEffect(effect)

        self.adjustSize()

        # after 5 sec, close window
        self._timer = QTimer(self, timeout=self.doClose)
        self._timer.setSingleShot(True)
        self._timer.start(3000)

    def doClose(self):
        try:
            self.closed.emit(self.item)
        except:
            # when the item had been deleted by user, this action could trigger a exception
            pass

    def mousePressEvent(self, event):
        super(NotificationItem, self).mousePressEvent(event)
        w = self.childAt(event.pos())
        if not w:
            return
        if w == self.labelClose:  # 点击关闭图标
            # 先尝试停止计时器
            self._timer.stop()
            self.closed.emit(self.item)
        elif w == self.labelMessage and self.callback and callable(self.callback):
            # 点击消息内容
            self._timer.stop()
            self.closed.emit(self.item)
            self.callback()  # 回调

    def paintEvent(self, event):
        # create round rect
        super(NotificationItem, self).paintEvent(event)
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 6, 6)

        # background color setting
        painter.fillPath(path, self.BackgroundColor)
