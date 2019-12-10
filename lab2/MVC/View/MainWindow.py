import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from MVC.View.Interface import Interface
from MVC.Controller.Controller import Controller


class MainWindow(QMainWindow):
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.initUI()

    def initUI(self):
        self.interface = Interface(self.application)

        self.setCentralWidget(self.interface)
        self.s = Controller()
        self.s.initController(self.interface, self)

        self.saveAction = QAction('&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save table')
        self.saveAction.triggered.connect(self.interface.click_save)
        self.interface.setSaveAction(self.saveAction)

        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)

        self.clearTableAction = QAction('&Сlear Table', self)
        self.clearTableAction.setShortcut('Ctrl+T')
        self.clearTableAction.setStatusTip('Clearing table data')
        self.clearTableAction.triggered.connect(self.interface.clearTable)
        self.interface.setSaveAction(self.clearTableAction)

        self.statusBar()
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.clearTableAction)
        self.fileMenu.addAction(self.exitAction)
        self.resize(800, 600)
        self.setWindowTitle('Проверка решений v0.142')
        self.setWindowIcon(QIcon('search.png'))
        self.show()

    def saveMessage(self):
        self.statusBar().showMessage('File saved OK')

    def addedTable(self):
        self.statusBar().showMessage('Data added to table')

    def clearTable(self):
        self.statusBar().showMessage('Table data cleared')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow(app)
    sys.exit(app.exec_())
