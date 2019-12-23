import time

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *


class Tabs(QTableWidget):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        super().__init__()
        # grid_layout = QGridLayout()  # Создаём QGridLayout

        # self.table = QTableWidget()  # Создаём таблицу
        self.setColumnCount(11)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.setHorizontalHeaderLabels(["Студент", "Время", "Статус", "Время выполнения", "Быстрее, чем", "Память", "Меньше, чем", "Входные", "Выходные",
                                        "Ожидаемые", "Ошибка"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.horizontalHeaderItem(2).setToolTip("Column 3 ")
        self.horizontalHeaderItem(3).setToolTip("Column 4 ")
        self.horizontalHeaderItem(4).setToolTip("Column 5 ")
        self.horizontalHeaderItem(5).setToolTip("Column 6 ")
        self.horizontalHeaderItem(6).setToolTip("Column 7 ")
        self.horizontalHeaderItem(7).setToolTip("Column 8 ")
        self.horizontalHeaderItem(8).setToolTip("Column 9 ")
        self.horizontalHeaderItem(9).setToolTip("Column 10 ")
        self.horizontalHeaderItem(10).setToolTip("Column 11 ")

        # Устанавливаем выравнивание на заголовки
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)

        # заполняем первую строку

        self.row = 0
        self.resizeColumnsToContents()
        # grid_layout.addWidget(self, 0, 0)  # Добавляем таблицу в сетку
        # self.show()

    def setRowsTable(self, decisions, name_students, pbar, pbar2):
        self.pbar = pbar
        self.pbar2 = pbar2
        self.pbar.setValue(0)
        self.setRowCount(self.rowCount() + len(decisions))  # и одну строку в таблице
        self.size = 100 // len(decisions)
        r = 0
        rows = self.row + len(decisions)
        for i in range(self.row, rows):
            self.setItem(i, 0, QTableWidgetItem(name_students[r]))
            self.setItem(i, 1, QTableWidgetItem(decisions[r]['time']))
            self.setItem(i, 2, QTableWidgetItem(decisions[r]['status_msg']))
            self.setItem(i, 3, QTableWidgetItem(decisions[r]['status_runtime']))
            if decisions[r]['status_msg'] == 'Accepted':
                self.setItem(i, 4, QTableWidgetItem(str(round(decisions[r]['runtime_percentile']))+'%'))
            else:
                self.setItem(i, 4, QTableWidgetItem(decisions[r]['runtime_percentile']))
            self.setItem(i, 5, QTableWidgetItem(decisions[r]['status_memory']))
            if decisions[r]['status_msg'] == 'Accepted':
                self.setItem(i, 6, QTableWidgetItem(str(round(decisions[r]['memory_percentile']))+'%'))
            else:
                self.setItem(i, 6, QTableWidgetItem(decisions[r]['memory_percentile']))
            self.setItem(i, 7, QTableWidgetItem(decisions[r]['input']))
            self.setItem(i, 8, QTableWidgetItem(decisions[r]['code_output']))
            self.setItem(i, 9, QTableWidgetItem(decisions[r]['expected_output']))
            self.setItem(i, 10, QTableWidgetItem(decisions[r]['full_compile_error']))
            if decisions[r]['status_msg'] == 'Accepted':
                color = QColor(78, 255, 150)
            else:
                color = QColor(255, 121, 118)
            for j in range(11):
                self.item(i, j).setBackground(color)
            QTimer.singleShot(0, self.startLoop)
            qApp.processEvents()
            r += 1
        # делаем ресайз колонок по содержимому
        self.row += r
        QTimer.singleShot(0, self.startLoop)
        qApp.processEvents()
        self.resizeColumnsToContents()
        self.pbar.reset()
        self.pbar2.reset()

    def startLoop(self):
        time.sleep(0.05)
        value = self.pbar.value() + self.size
        self.pbar.setValue(value)

    def startLoop2(self):
        time.sleep(0.05)
        value = self.pbar2.value() + self.size
        self.pbar2.setValue(value)
