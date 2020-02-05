__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '1/31/2020 1:27 PM'

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget, QMenu, QSystemTrayIcon, QMessageBox, qApp, QWidgetAction, QSlider, QLabel, \
    QVBoxLayout

from conf.Settings import DEFAULT_OPACITY
from model.Pet import Poro


class TrayMenuWindow(QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initPet()

        # setting menu group
        settings = QMenu("Settings", self)
        settings.setIcon(QIcon("resources/ico/poro.ico"))

        # setting -> draggable
        self.drag_action = QAction("Draggable", self)
        self.drag_action.setCheckable(True)
        self.drag_action.setChecked(True)
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

    def initPet(self, draggable=True, opacity=float(DEFAULT_OPACITY / 100)):
        self.pet = Poro(draggable, opacity)

    def updateOpacity(self, value):
        # render new opacity to label widget
        self.opacity_label.setText("Opacity: {} %".format(str(value)))
        # update avatar's opacity
        self.pet.updateAvatarOpacity(float(int(value) / 100))

    def freezeOrNot(self, bool_value):
        # TODO make update to the avatar
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
