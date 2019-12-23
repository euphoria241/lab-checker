import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp

from MVC.Controller.Controller import Controller
from MVC.View.Interface import Interface
from MVC.View.FramelessWindow import FramelessWindow

from ctypes import *


class YUZU(QMainWindow):
    def __init__(self, frame, application):
        super().__init__()
        self.frame = frame
        self.application = application
        self.initUI()

    def initUI(self):
        self.interface = Interface(self.application)

        self.setCentralWidget(self.interface)

        self.saveAction = QAction('&Сохранить', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Сохранение данных таблицы')
        self.saveAction.triggered.connect(self.interface.click_save)
        self.interface.setSaveAction(self.saveAction)

        self.exitAction = QAction('&Выход', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Выход из программы')
        self.exitAction.triggered.connect(qApp.quit)

        self.clearTableAction = QAction('&Очисить Таблицу', self)
        self.clearTableAction.setShortcut('Ctrl+T')
        self.clearTableAction.setStatusTip('Очищение данных таблицы')
        self.clearTableAction.triggered.connect(self.interface.clearTable)
        self.interface.setSaveAction(self.clearTableAction)

        self.referenceAction = QAction('&О Программе', self)
        self.referenceAction.setShortcut('Ctrl+G')
        self.referenceAction.setStatusTip('Информация по программе')
        self.referenceAction.triggered.connect(self.interface.openLink)

        self.autographAction = QAction('&Разработчики', self)
        self.autographAction.setStatusTip('Черкасов Д.Е., Шафиев А.А.')

        self.statusBar()
        self.menubar = self.menuBar()
        self.menubar.setMinimumHeight(27)
        self.fileMenu = self.menubar.addMenu('&Файл')
        self.referenceMenu = self.menubar.addMenu('&Справка')

        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.clearTableAction)
        self.fileMenu.addAction(self.exitAction)

        self.referenceMenu.addAction(self.referenceAction)
        self.referenceMenu.addAction(self.autographAction)

        self.setStyleSheet('QMainWindow {background-color: rgb(230,230,230)}')


        self.referenceAction = QAction('&О Программе', self)
        self.referenceAction.setShortcut('Ctrl+G')
        self.referenceAction.setStatusTip('Информация по программе')
        self.referenceAction.triggered.connect(self.interface.openLink)


        self.an = QAction('&Anime', self)
        self.an.setShortcut('Ctrl+L')
        self.an.setStatusTip('Информация по программе')
        self.an.triggered.connect(self.start_super_mode)
        self.addAction(self.an)


        oImage = QImage("jojo.jpeg")
        sImage = oImage.scaled(QSize(800, 700))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        # self.show()

    def saveMessage(self):
        self.statusBar().showMessage('Данные таблицы сохранены')

    def addedTable(self):
        self.statusBar().showMessage('Данные добавлены в таблицу')

    def clearTable(self):
        self.statusBar().showMessage('Данные таблицы очищены')

    def hideWindow(self):
        self.interface.setDisabled(True)

    def showWindow(self):
        self.interface.setDisabled(False)

    def start_super_mode(self):
        print('Запускаем супер мод')

    def create_controller(self):
        self.s = Controller()
        self.s.initController(self.interface, self)

    def hide_frame(self):
        self.frame.hide()

StyleSheet = """
/* Панель заголовка */
TitleBar {
    background-color: #EFEE55; /* #f0c70f */
}
QMenuBar {
    background-color: #EFEE55;
    color: black;
}
QMenuBar::item {
    background-color: #EFEE55;
    color: black;
}
QMenuBar::item:selected {    
    background-color: #d2d214;
    color: white;
}
QMenuBar::item:pressed {
    background: rgb(93,159,59);
}
QMenu {
    background-color: rgb(93,159,59);
    color: white;
}
QMenu::item {
    background-color: transparent;
}
QMenu::item:selected { 
    background-color: rgb(54,79,47);
    color: rgb(242,207,59);
}
QMenu::item:disabled { 
    color: #B8B8B8;
}
/* Минимизировать кнопку `Максимальное выключение` Общий фон по умолчанию */
#buttonMinimum,#buttonMaximum,#buttonClose, #buttonMy {
    border: none;
    background-color: #EFEE55;
    color: black;
}
/* Зависание */
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: #d2d214;
    color: white;
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}
#buttonMy:hover {
    color: white;
    background-color: rgb(0,154,76); 
}
/* Мышь удерживать */
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(0,154,76);
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
QProgressBar {
     border-radius: 5px;
     text-align: center;
     border: 0.5px solid lightgrey;
}
QProgressBar::chunk {
         background-color: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 rgb(177,243,111), stop:1 rgb(117,171,73));
}
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    app.setStyle('Fusion')
    w = FramelessWindow()
    w.setWindowTitle('    YUZU v0.572')
    app.setWindowIcon(QIcon('yuzu2.png'))
    mainWindow = YUZU(w, app)
    w.setWidget(mainWindow)  # Добавить свое окно
    w.show()
    mainWindow.create_controller()
    sys.exit(app.exec_())
