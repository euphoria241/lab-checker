import sys
from PyQt5.QtWidgets import *
from MVC.View.FileOpener import FileOpener
from MVC.View.MainWindow import MainWindow
from MVC.View.WindowError import WindowError
from MVC.Controller.Controller import Controller

class Interface(QWidget):
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.initUI()

    def initUI(self):
        self.ifOpenBD = False
        self.ifOpenFilesOfStudents = False
        self.fileOpener = FileOpener()
        # Создание окна с фиксированной длинной 600
        self.resize(800, 600)
        # self.w.setMaximumWidth(800)
        self.setWindowTitle('Проверка решений v0.142')

        self.str1 = QLabel('Выберите базу данных студентов', self)

        self.line1 = QLineEdit()
        self.line1.setMinimumWidth(600)
        self.line1.setReadOnly(True)

        self.btn1 = QPushButton('Open', self)
        self.btn1.clicked.connect(self.click_btn1)

        self.str2 = QLabel('Выберите файл/файлы для проверки', self)

        self.line2 = QLineEdit()
        self.line2.setMinimumWidth(600)
        self.line2.setReadOnly(True)

        self.btn2 = QPushButton('Open')
        self.btn2.clicked.connect(self.click_btn2)

        self.start = QPushButton('Start')
        self.start.setMaximumWidth(200)
        self.start.clicked.connect(self.gettingStarted)
        self.start.setDisabled(True)

        # Таблица
        self.mw = MainWindow()
        self.mw.setMinimumWidth(600)

        self.txtArea = QPlainTextEdit()
        self.txtArea.setMinimumWidth(600)
        self.txtArea.setReadOnly(True)

        self.pbar = QProgressBar(self)
        self.pbar.setMinimumWidth(600)

        self.strPbar1 = QLabel('Обработано задач: 0 из 0', self)

        self.box = QGridLayout(self)
        self.box.addWidget(self.str1, 0, 0)
        self.box.addWidget(self.line1, 1, 0)
        self.box.addWidget(self.str2, 2, 0)
        self.box.addWidget(self.line2, 3, 0)
        self.box.addWidget(self.btn1, 1, 1)
        self.box.addWidget(self.btn2, 3, 1)
        self.box.addWidget(self.mw, 5, 0)
        self.mw.hide()
        self.box.addWidget(self.txtArea, 5, 0)
        self.box.addWidget(self.start, 6, 1)
        self.box.addWidget(self.pbar, 4, 0)
        self.box.addWidget(self.strPbar1, 4, 1)
        self.show()

    def click_btn1(self):
        if not self.txtArea.isVisible():
            self.txtArea.show()
            self.mw.hide()
        fileName = self.fileOpener.openFileNameDialog()
        if fileName != '':
            self.line1.setText(fileName)
            self.txtArea.appendPlainText("Загружен файл базы данных студентов:\n" + fileName)
            self.ifOpenBD = True
            if self.ifOpenBD == self.ifOpenFilesOfStudents:
                self.start.setEnabled(True)

    def click_btn2(self):
        if not self.txtArea.isVisible():
            self.txtArea.show()
            self.mw.hide()
        fileNames = self.fileOpener.openFileNamesDialog()
        if len(fileNames) != 0:
            self.txtArea.appendPlainText("Загружены файлы для проверки:")
            str = ""
            for fileName in fileNames:
                self.txtArea.appendPlainText(fileName)
                str += fileName + "; "
            self.line2.setText(str)
            self.ifOpenFilesOfStudents = True
            if self.ifOpenBD == self.ifOpenFilesOfStudents:
                self.start.setEnabled(True)

    def gettingStarted(self):
        self.pbar.show()
        self.strPbar1.setStyleSheet("QLabel {background-color:yellow}")
        decisions, name_students = s.checkDecisions(self.pbar, self.strPbar1)
        self.strPbar1.setText('Формирование таблицы')
        self.mw.setRowsTable(decisions, name_students, self.pbar)
        self.strPbar1.setText('Обработка завершена')
        self.strPbar1.setStyleSheet("QLabel {background-color:rgb(240,240,240)}")
        self.txtArea.hide()
        self.mw.show()
        # self.pbar.hide()

    def isTable(self):
        if not self.txtArea.isVisible():
            self.mw.hide()
            self.txtArea.show()
            self.mw = MainWindow()
            self.mw.hide()
            self.mw.setMinimumWidth(600)
            self.box.addWidget(self.mw, 5, 0)

    def openWindowError(self, error):
        WindowError(self.application, error)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Interface(app)
    s = Controller()
    s.initController(ex)
    sys.exit(app.exec_())
