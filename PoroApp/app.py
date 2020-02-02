__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '1/31/2020 1:23 PM'

import sys

from PyQt5.QtWidgets import QApplication

from view.Panel import TrayMenuPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    trayMenu = TrayMenuPanel()
    trayMenu.pet.setMovement("angry")
    sys.exit(app.exec_())
