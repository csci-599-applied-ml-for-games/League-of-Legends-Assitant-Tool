__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '1/31/2020 1:27 PM'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QMenu, QSystemTrayIcon, QMessageBox, qApp, QWidgetAction, QSlider, QLabel, \
    QVBoxLayout

from conf.Settings import DEFAULT_OPACITY, DEFAULT_DRAGGABLE, LOL_CLIENT_HEART_BEAT_RATE, BAN_AREA_YOU, BAN_AREA_ENEMY, \
    POSITION_AREA
from model.ImgProcessor import ImgCatcherThread, ImgCropType
from model.LoLClientHeartBeat import ClientHeartBeat, ClientInfo, ClientStatus
from model.Pet import Poro
from utils.PositionUtil import genRelativePos
from view.NotificationWindow import NotificationWindow


class TrayMenuWindow(QWidget):
    client_info_sender = pyqtSignal(ClientInfo)
    # save previous client position in window
    old_client_position = None
    old_client_status = 0

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initPet()

        # setting menu group
        settings = QMenu("Settings", self)
        settings.setIcon(QIcon("resources/ico/poro.ico"))

        # setting -> draggable
        self.drag_action = QAction("Draggable", self)
        self.drag_action.setCheckable(True)
        self.drag_action.setChecked(DEFAULT_DRAGGABLE)
        self.drag_action.triggered.connect(self.freezeOrNot)

        # setting -> opacity slider
        self.opacity_action = self.initOpacitySlider(QWidgetAction(self))
        settings.addAction(self.drag_action)
        settings.addAction(self.opacity_action)

        # about and exit action
        about_action = QAction(QIcon("resources/ico/poro.ico"), "About", self)
        exit_action = QAction(QIcon("resources/ico/poro.ico"), '&Exit', self)
        about_action.triggered.connect(self.aboutInfo)
        exit_action.triggered.connect(qApp.quit)

        # init the tray_menu
        tray_menu = QMenu(self)
        tray_menu.addMenu(settings)
        tray_menu.addAction(about_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        tray_icon = QSystemTrayIcon(self)
        tray_icon.setIcon(QIcon("resources/ico/poro.ico"))
        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()

        ClientStatus.init()
        self.count_false = 0
        self.has_client_connected = False
        # init thread using to monitor lol client
        self.lol_client_heart_beat_thread = ClientHeartBeat(LOL_CLIENT_HEART_BEAT_RATE)
        # client 的监听信号 会发给 self.getClientInfo 这个函数
        self.lol_client_heart_beat_thread.keeper.connect(self.getClientInfo)
        self.thread = QThread()
        # QObject 转 Qthread
        self.lol_client_heart_beat_thread.moveToThread(self.thread)
        self.thread.started.connect(self.lol_client_heart_beat_thread.run)
        self.thread.start()

        # when the signal got new position, send to ImgCatcher
        self.client_info_sender.connect(statusChange)

    def initOpacitySlider(self, widget):
        opacity_slider_widget = QWidget(self)
        layout = QVBoxLayout(opacity_slider_widget)
        self.opacity_label = QLabel("Opacity: {} %".format(DEFAULT_OPACITY), self)
        self.opacity_label.setAlignment(Qt.AlignCenter)
        slider = QSlider(Qt.Horizontal, self.opacity_label)
        slider.setSingleStep(10)
        slider.setValue(DEFAULT_OPACITY)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.valueChanged.connect(self.updateOpacity)
        layout.addWidget(self.opacity_label)
        layout.addWidget(slider)
        widget.setDefaultWidget(opacity_slider_widget)
        return widget

    def initPet(self, draggable=DEFAULT_DRAGGABLE, opacity=float(DEFAULT_OPACITY / 100)):
        self.pet = Poro(draggable, opacity)

    def updateOpacity(self, value):
        # render new opacity to label widget
        self.opacity_label.setText("Opacity: {} %".format(str(value)))
        # update avatar's opacity
        self.pet.updateAvatarOpacity(float(int(value) / 100))

    def freezeOrNot(self, bool_value):
        if bool_value:
            # make avatar draggable
            self.drag_action.setChecked(True)
            self.pet.setFreezeOrNot(True)
        else:
            # make avatar position fixed
            self.drag_action.setChecked(False)
            self.pet.setFreezeOrNot(False)

    def aboutInfo(self):
        QMessageBox.about(self.pet, 'About',
                          """<style type="text/css">
                            table.imagetable {
                                font-family: verdana,arial,sans-serif;
                                font-size:11px;
                                color:#333333;
                                border-width: 1px;
                                border-color: #999999;
                                border-collapse: collapse;
                            }
                            
                          """)

    def getClientInfo(self, lol_client):
        global old_client_position
        global old_client_status
        if lol_client.isAlive and (not self.has_client_connected):
            # first connected, and send a notification
            self.has_client_connected = True
            old_client_position = lol_client.getPosition()
            old_client_status = lol_client.getStatusIndex()
            NotificationWindow.success('Success',
                                       '''Connected to LOL Client''',
                                       callback=None)
            self.client_info_sender.emit(lol_client)
            # 设置poro 表情 TODO  表情有问题 具体看测试用例
            # self.pet.setEmoji('coolguy')

        elif lol_client.isAlive and self.has_client_connected:
            # when you got here that means you have connected stably
            if (lol_client.getPosition() != old_client_position) or \
                    (lol_client.getStatusIndex() != old_client_status):
                # 如果跟之前状态不一样 我们法院一条信息， 如果一样就不发
                old_client_position = lol_client.getPosition()
                old_client_status = lol_client.getStatusIndex()
                self.client_info_sender.emit(lol_client)

        elif not lol_client.isAlive:
            self.has_client_connected = False
            self.count_false += 1
            old_client_position = None
            old_client_status = 0
            if (self.count_false == 1) or (self.count_false % 5 == 0):
                # 如果等了10次都没连上， 发个提示
                NotificationWindow.error('Error',
                                         '''Haven't connect LOL Client''',
                                         callback=None)
                self.client_info_sender.emit(lol_client)
                # 设置poro 表情
                # self.pet.setEmoji('shock')


def statusChange(client):
    if client.hasAlive():
        if not client.isGameMode():
            NotificationWindow.info('Info',
                                    "LOL Client Status: Your are in <u><b>{}</b></u> Panel".format(
                                        client.getStatus()["name"]),
                                    callback=None)
        else:
            # picking champions
            if client.getStatusIndex() == ClientStatus.ChooseChampion:
                NotificationWindow.suggest('Picking Champion ...',
                                           "Poro recommends these following champions for you".format(
                                               client.getStatus()["name"]),
                                           callback=None)
                # 这里开启一个线程 去捕捉 图片 预测 不需要跟pyqt挂钩
                goCaptureAndAnalysis(client)
            else:
                # InGame
                # TODO
                NotificationWindow.suggest('Game Mode',
                                           "continue to give you suggestions".format(
                                               client.getStatus()["name"]),
                                           callback=None)
                # goCaptureAndAnalysis(client)


    else:
        NotificationWindow.warning('Warning',
                                   "Assistant has lost connection to LOL client",
                                   callback=None)


# initialize an image catcher
# and use position data to crop imgs in every n sec.
def goCaptureAndAnalysis(client_info):
    ImgCropType.init()
    if client_info.getStatusIndex() == ClientStatus.ChooseChampion:
        ban_you_catcher = ImgCatcherThread("BAN_YOU_IMG_CATCHER", client_info, ImgCropType.BAN_5_CHAMP,
                                           genRelativePos(client_info.getPosition(), BAN_AREA_YOU,
                                                          client_info.getEnlargementFactor()))

        ban_enemy_catcher = ImgCatcherThread("BAN_ENEMY_IMG_CATCHER", client_info, ImgCropType.BAN_5_CHAMP,
                                             genRelativePos(client_info.getPosition(), BAN_AREA_ENEMY,
                                                            client_info.getEnlargementFactor()))

        position_catcher = ImgCatcherThread("POS_IMG_CATCHER", client_info, ImgCropType.POSITION_LABEL,
                                            genRelativePos(client_info.getPosition(), POSITION_AREA,
                                                           client_info.getEnlargementFactor()))

        ban_you_catcher.start()
        ban_enemy_catcher.start()
        position_catcher.start()
    else:
        # when you got here, it means you are in the game mode
        print("go_capture -> ", client_info.getStatus())
    # capturer.receivePosition(client_info.getPosition())
