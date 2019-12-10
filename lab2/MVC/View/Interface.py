import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from MVC.View.FileOpener import FileOpener
from MVC.View.VerificationWindow import VerificationWindow
from MVC.View.WindowError import WindowError
from MVC.View.Tabs import Tabs
from MVC.View.Insets import Insets
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
        self.mw = Tabs()
        self.mw.setMinimumWidth(600)

        self.txtArea = QPlainTextEdit()
        self.txtArea.setMinimumWidth(600)
        self.txtArea.setReadOnly(True)

        self.pbar = QProgressBar(self)
        self.pbar.setMinimumWidth(600)

        self.pbar2 = QProgressBar(self)
        self.pbar2.setMinimumWidth(600)

        # self.strPbar1 = QLabel('Обработано задач: 0 из 0', self)
        self.tabs_area = Insets(self.mw, self.txtArea)


        self.enabledElement = [self.start, self.btn1, self.btn2, self.tabs_area]

        self.box = QGridLayout(self)
        self.box.addWidget(self.str1, 0, 0)
        self.box.addWidget(self.line1, 1, 0)
        self.box.addWidget(self.str2, 2, 0)
        self.box.addWidget(self.line2, 3, 0)
        self.box.addWidget(self.btn1, 1, 1)
        self.box.addWidget(self.btn2, 3, 1)
        self.box.addWidget(self.pbar2, 4, 0)
        self.box.addWidget(self.pbar, 5, 0)
        self.box.addWidget(self.tabs_area, 6, 0)
        # self.box.addWidget(self.mw, 6, 0)
        # self.box.addWidget(self.txtArea, 6, 0)
        self.box.addWidget(self.start, 7, 1)
        self.pbar.hide()
        self.pbar2.hide()
        # self.box.addWidget(self.strPbar1, 4, 1)

        # self.show()

    def click_btn1(self):
        fileName = self.fileOpener.openFileNameDialog()
        if fileName != '':
            self.line1.setText(fileName)
            self.txtArea.appendPlainText("Загружен файл базы данных студентов:\n" + fileName)
            self.ifOpenBD = True
            if self.ifOpenBD == self.ifOpenFilesOfStudents:
                self.start.setEnabled(True)

    def click_btn2(self):
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
        self.pbar2.show()
        self.enabledElements(False)
        # self.strPbar1.setStyleSheet("QLabel {background-color:yellow}")
        s = Controller()
        decisions, name_students = s.checkDecisions(self.pbar, self.pbar2)
        # self.strPbar1.setText('Формирование таблицы')
        self.mw.setRowsTable(decisions, name_students, self.pbar, self.pbar2)
        # self.strPbar1.setText('Обработка завершена')
        # self.strPbar1.setStyleSheet("QLabel {background-color:rgb(240,240,240)}")
        self.enabledElements(True)
        self.pbar.hide()
        self.pbar2.hide()
        print(123)
        s.addedTable()
        print(213)

    def openWindowError(self, error):
        WindowError(self.application, error)

    def enabledElements(self, boolean):
        for element in self.enabledElement:
            element.setEnabled(boolean)

    def click_save(self):
        self.fileOpener.openFileSave()

    def setSaveAction(self, saveAction):
        self.saveAction = saveAction
        self.saveAction.setDisabled(True)
        self.enabledElement.append(saveAction)

    def clearTable(self):
        s = Controller()
        s.clearDataTable()
        self.mw = Tabs()
        self.mw.setMinimumWidth(600)
        self.tabs_area.updateTable(self.mw)
        # self.tabs_area = Insets(self.mw, self.txtArea)
        # self.box.addWidget(self.tabs_area, 6, 0)
        s.clearTable()
