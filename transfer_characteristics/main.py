# -*- coding: utf-8 -*
"""GUI Setting"""
from PySide2 import QtWidgets

from gui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
