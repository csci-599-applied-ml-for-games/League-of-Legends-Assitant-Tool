__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '1/31/2020 1:47 PM'

import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget

from conf.Settings import ASSETS_DIR, TIME_INTERVAL
from model.PetsStatus import PoroAssets
from utils.ImgUtil import loadSingleImgFromPath, loadAllImgFromDirPath
from view.NotificationWindow import NotificationWindow


class Poro(QWidget):
    def __init__(self, draggable, opacity, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.graphics_opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.pet_status = PoroAssets()
        self.pet_status.loadData(ASSETS_DIR)
        self.initUI(draggable, opacity)

    def initUI(self, draggable, opacity):
        # make the window translucent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # init avatar
        self.initAvatar(draggable, opacity)

        # every 0.8s update a img, making avatar alive
        self.timer = QTimer()
        self.timer.timeout.connect(self.animationSetUp)
        self.timer.start(TIME_INTERVAL)

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

        # init animation sequence
        self.initAnimationDataSet()
        self.avatar.resize(128, 128)

        # could draggable or not
        self.could_draggable = draggable

    def initAnimationDataSet(self):
        # get img data
        all_imgs_path = self.pet_status.getAllImgPaths()
        # whether animation is running
        self.running = False
        # the times of animation type None runs
        self.none_times = 0
        # all the emoji data saved in here
        self.activated_move_data = []
        for img_paths in all_imgs_path:
            imgs = loadAllImgFromDirPath(ASSETS_DIR, img_paths)
            self.activated_move_data.append(imgs)

    def animationSetUp(self):
        if not self.running:
            # control which emoji could be play
            self.emojis = self.setEmoji()
            # basically, every emoji play from 1 frame to the end
            self.frame_index = 0
            self.running = True
        self.play(self.activated_move_data[self.emojis])

    def setEmoji(self, emoji_name=None):
        if None is emoji_name:
            self.none_times += 1
            if self.none_times >= 3:
                self.initAnimationDataSet()
            return random.randint(0, len(self.activated_move_data) - 1)
        else:
            specific_movement = self.pet_status.getSomeImgPaths(emoji_name)
            self.updateAnimationDateSet(specific_movement)
            return 0

    def updateAnimationDateSet(self, img_paths):
        self.activated_move_data = []
        imgs = loadAllImgFromDirPath(ASSETS_DIR, img_paths)
        self.activated_move_data.append(imgs)
        self.activated_move_data.append(imgs)
        self.activated_move_data.append(imgs)

    def play(self, imgs):
        if self.frame_index >= len(imgs):
            self.frame_index = 0
            self.running = False

        self.avatar.setPixmap(QPixmap.fromImage(imgs[self.frame_index]))
        self.frame_index += 1

    def fixedPos(self):
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - 300),
                  (screen.height() - 315))

    def updateAvatarOpacity(self, opacity):
        self.graphics_opacity_effect.setOpacity(opacity)
        self.avatar.setGraphicsEffect(self.graphics_opacity_effect)

    def setFreezeOrNot(self, bool_value):
        self.could_draggable = bool_value

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.could_draggable:
            self.dragged_new_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        # print("self. pos - >", self.pos()) #where the pet shows
        if Qt.LeftButton and self.could_draggable:
            self.move(event.globalPos() - self.dragged_new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        NotificationWindow.last()
        self.setCursor(QCursor(Qt.ArrowCursor))
