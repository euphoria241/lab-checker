from MVC.Model.Connected import Connected
import time

from PyQt5.QtWidgets import qApp

from MVC.Model.FileCSV import FileCSV
from MVC.View.VerificationWindow import VerificationWindow


class Controller(object):
    obj = None  # Атрибут для хранения единственного экземпляра

    def __new__(cls, *dt, **mp):  # класса Singleton.
        if cls.obj is None:  # Если он еще не создан, то
            cls.obj = object.__new__(cls, *dt, **mp)  # вызовем __new__ родительского класса
        return cls.obj  # вернем синглтон

    def setDictStudents(self, fileName):
        self.dict_students = dict()
        with open(fileName, encoding="utf8") as file:
            for line in file:
                key, value = line.split()
                self.dict_students[key] = value
        print(self.dict_students)

    def setArrayOfSolutions(self, fileNames):
        self.array_of_solutions = dict()
        for fileName in fileNames:
            name = fileName.split("/").pop().split(".")[0]
            decision_json = {"question_id": "",
                             "lang": "python3",
                             "typed_code": ""}
            typed_code = "class Solution:\n"
            with open(fileName, encoding="utf8") as file:
                for line in file:
                    typed_code += "\t" + line
            decision_json["typed_code"] = typed_code
            self.array_of_solutions[name] = decision_json
        print(self.array_of_solutions)

    def checkDecisions(self, pbar, pbar2):
        # count = 1
        size = len(self.array_of_solutions)
        # strPbar1.setText('Обработано задач: 0 из ' + str(size))
        # qApp.processEvents()
        decisions = []
        name_students = []
        self.connected.setPbar(pbar, pbar2, size)
        for name_student in self.array_of_solutions:
            dec = self.connected.solve(self.array_of_solutions[name_student],
                                                  self.dict_students[name_student])
            if dec == 'Error':
                self.interface.openWindowError(self.error_connect)
                break
            decisions.append(dec)
            self.bd_desicions.append(dec)
            name_students.append(name_student)
            self.bd_names.append(name_student)
            time.sleep(5)
            # strPbar1.setText('Обработано задач: ' + str(count) + ' из ' + str(size))
            # qApp.processEvents()
            # count += 1
        self.array_of_solutions = dict()
        return decisions, name_students

    def initController(self, interface, mainWindow):
        self.interface = interface
        self.mainWindow = mainWindow
        self.dict_students = dict()
        self.array_of_solutions = dict()
        self.connected = Connected()
        self.error_connect = 'Ошибка подключения к серверу.\nПроверьте соединение с интернетом и запустите программу снова.'
        self.error_authorization = 'Не удалось авторизоваться.\nПроверьте соединение с интернетом и запустите программу снова.'
        self.bd_desicions = []
        self.bd_names = []
        status, incorrect, verification = self.connected.authorization()
        if verification:
            self.verificatinOpenWindow()
            return
        if status != 200 or not incorrect:
            self.interface.openWindowError(self.error_authorization)

    def saveFile(self, path):
        fileCSV = FileCSV()
        pars = fileCSV.dataPars(self.bd_desicions, self.bd_names)
        fileCSV.saveFile(path, pars)
        self.mainWindow.saveMessage()

    def addedTable(self):
        self.mainWindow.addedTable()

    def verificatinOpenWindow(self):
        VerificationWindow(self, self.mainWindow)

    def verification(self, code):
        print(code)

    def clearDataTable(self):
        self.bd_desicions = []
        self.bd_names = []

    def clearTable(self):
        self.mainWindow.clearTable()