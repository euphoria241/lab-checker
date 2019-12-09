from PyQt5.QtWidgets import *
from MVC.Controller.Controller import Controller

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

        #self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Проводник", "", "Text file (*.txt)",
                                                  options=options)

        if fileName:
            s = Controller()
            s.setDictStudents(fileName)
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