import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class WindowError(QWidget):

    def __init__(self, application, error):
        # Обязательно нужно вызвать метод супер класса
        super().__init__()
        self.application = application
        self.title = 'Window Error'
        self.error = error
        self.initUI()

    def initUI(self):
        buttonReply = QMessageBox.question(self, self.title, self.error, QMessageBox.Yes)
        buttonReply.show()
        if buttonReply == QMessageBox.Yes:
            self.mainWindowClose()

    def mainWindowClose(self):
        sys.exit(self.application.exec_())