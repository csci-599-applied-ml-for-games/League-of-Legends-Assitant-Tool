__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '1/31/2020 1:23 PM'

import cgitb
import sys

from PyQt5.QtWidgets import QApplication

from view.TrayMenuWindow import TrayMenuWindow

if __name__ == "__main__":
    sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    app = QApplication(sys.argv)
    trayMenu = TrayMenuWindow()
    sys.exit(app.exec_())
