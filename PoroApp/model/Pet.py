__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '1/31/2020 1:47 PM'

import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget

from Utils.ImgUtil import loadSingleImgFromPath, loadAllImgFromDirPath
from model.PetsStatus import PoroStatus

ASSETS_DIR = "resources/assets/"
ABS_ASSETS_DIR = "../resources/assets"


class Poro(QWidget):
    def __init__(self, draggable, opacity, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.graphics_opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.initUI(draggable, opacity)

    def initUI(self, draggable, opacity):
        # make the window translucent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # init avatar
        self.initAvatar(draggable, opacity)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animationSetUp)
        self.timer.start(800)

        self.fixedPos()
        self.show()

    def initAvatar(self, draggable, opacity):
        self.avatar = QLabel(self)
        self.graphics_opacity_effect.setOpacity(opacity)
        self.avatar.setGraphicsEffect(self.graphics_opacity_effect)
        self.avatar.setAutoFillBackground(True)
        self.avatar.setAttribute(Qt.WA_TranslucentBackground, True)

        # load first frame
        self.avatar.setPixmap(QPixmap.fromImage(loadSingleImgFromPath(ASSETS_DIR + 'stare/poro-stare-0.png')))

        pet_s_status = PoroStatus()
        pet_s_status.loadData(ASSETS_DIR)
        seq_imgs_paths = pet_s_status.getAllImgPaths()

        self.initData(seq_imgs_paths)
        self.avatar.resize(128, 128)

    def initData(self, seq_img_paths):
        self.index = 0
        self.running = False
        self.activated_move_data = []
        for seq in seq_img_paths:
            imgs = loadAllImgFromDirPath(ASSETS_DIR, seq)
            self.activated_move_data.append(imgs)

    def animationSetUp(self):
        if not self.running:
            # control which img could be play
            self.move_index = self.setMovement()
            self.index = 0
            self.running = True
        self.play(self.activated_move_data[self.move_index])

    def setMovement(self, animation_name=None):
        print(animation_name)
        return random.randint(0, len(self.activated_move_data) - 1)

    def play(self, imgs):
        if self.index >= len(imgs):
            self.index = 0
            self.running = False

        self.avatar.setPixmap(QPixmap.fromImage(imgs[self.index]))
        self.index += 1

    def fixedPos(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width() - 150),
                  (screen.height() - size.height() - 200))

    def updateAvatarOpacity(self, opacity):
        pass

    def setFreezeOrNot(self, bool_value):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
