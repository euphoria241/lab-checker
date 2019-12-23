import time

from MVC.Model.Connected import Connected
import datetime

from MVC.Model.FileCSV import FileCSV
from MVC.Model.FileXLSX import FileXLSX
from MVC.Model.LogSave import LogSave
from MVC.View.VerificationWindow import VerificationWindow


class Controller(object):
    obj = None  # Атрибут для хранения единственного экземпляра

    def __new__(cls, *dt, **mp):  # класса Singleton.
        if cls.obj is None:  # Если он еще не создан, то
            cls.obj = object.__new__(cls, *dt, **mp)  # вызовем __new__ родительского класса
        return cls.obj  # вернем синглтон

    def setDictStudents(self, dict_students):
        self.dict_students = dict_students
        print(self.dict_students)

    def setArrayOfSolutions(self, fileNames):
        self.array_of_solutions = dict()
        for fileName in fileNames:
            name = fileName.split("/").pop().split(".")[0]
            decision_json = {"question_id": "",
                             "lang": "python3",
                             "typed_code": ""}
            typed_code = "class Solution:\n"
            flag = True
            with open(fileName, encoding="utf8") as file:
                for line in file:
                    if flag:
                        a = line.find('(') + 1
                        line = line[:a] + 'self, ' + line[a:]
                        flag = False
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
        # for i in range(len(name_students)):
        #     self.log_save.write_log('\n' + str(self.date) + ' [' + name_students[i] + ']: ' + decisions[i])
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
        # self.log_save = LogSave()
        status, incorrect, verification = self.connected.authorization()
        if verification:
            self.verificatinOpenWindow()
            return
        if status != 200 or not incorrect:
            self.interface.openWindowError(self.error_authorization)
        self.interface.authorizationMessage()

    def saveFile(self, path):
        if path.endswith('.csv'):
            fileCSV = FileCSV()
            pars = fileCSV.dataPars(self.bd_desicions, self.bd_names)
            fileCSV.saveFile(path, pars)
        elif path.endswith('.xlsx') or path.endswith('.xls'):
            fileXLSX = FileXLSX()
            pars = fileXLSX.dataPars(self.bd_desicions, self.bd_names)
            fileXLSX.saveFile(path, pars)
        self.interface.saveTableMessage()
        self.mainWindow.saveMessage()

    def addedTable(self):
        self.mainWindow.addedTable()

    def verificatinOpenWindow(self):
        self.mainWindow.hideWindow()
        self.verifyWin = VerificationWindow(self, self.mainWindow)

    def verification(self, code):
        self.connected.verifyGit(code)
        self.verifyWin.close()
        self.mainWindow.showWindow()

    def clearDataTable(self):
        self.bd_desicions = []
        self.bd_names = []

    def clearTable(self):
        self.mainWindow.clearTable()