from PyQt5.QtWidgets import *
from MVC.Controller.Controller import Controller
import pyzipper


class FileOpener(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Проводник'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Проводник", "", "Archive file (*.zip)",
                                                  options=options)
        dict_students = dict()
        with pyzipper.AESZipFile(fileName, 'r') as file:
            file.pwd = b'567812'
            with file.open('db.txt', 'r') as db:
                for line in db:
                    key, value = line.decode('utf_8_sig').split()
                    dict_students[key] = value
        if fileName:
            s = Controller()
            s.setDictStudents(dict_students)
        return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Проводник", "", "Python files (*.py)",
                                                    options=options)
        if fileNames:
            s = Controller()
            s.setArrayOfSolutions(fileNames)
        return fileNames

    def openFileSave(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Проводник", "", "Table file (*.csv *.xlsx *.xls)",
                                                  options=options)
        if fileName:
            s = Controller()
            s.saveFile(fileName)
