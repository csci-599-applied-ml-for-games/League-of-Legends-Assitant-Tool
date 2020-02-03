__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '1/31/2020 1:23 PM'

import sys
import PyQt5.sip
from PyQt5.QtWidgets import QApplication

from view.Panel import TrayMenuPanel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    trayMenu = TrayMenuPanel()
    # trayMenu.pet.setEmoji("angry")
    sys.exit(app.exec_())
