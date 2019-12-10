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
        self.setColumnCount(8)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.setHorizontalHeaderLabels(["Студент", "Статус", "Время выполнения", "Память", "Input", "Output", "Expected", "Error"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.horizontalHeaderItem(2).setToolTip("Column 3 ")
        self.horizontalHeaderItem(3).setToolTip("Column 4 ")
        self.horizontalHeaderItem(4).setToolTip("Column 5 ")
        self.horizontalHeaderItem(5).setToolTip("Column 6 ")
        self.horizontalHeaderItem(6).setToolTip("Column 7 ")
        self.horizontalHeaderItem(7).setToolTip("Column 8 ")

        # Устанавливаем выравнивание на заголовки
        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)

        # заполняем первую строку

        self.row = 0
        self.resizeColumnsToContents()
        # grid_layout.addWidget(self, 0, 0)  # Добавляем таблицу в сетку
        self.show()

    def setRowsTable(self, decisions, name_students, pbar, pbar2):
        self.pbar = pbar
        self.pbar2 = pbar2
        self.pbar.setValue(0)
        self.setRowCount(len(decisions))  # и одну строку в таблице
        self.size = 100 // len(decisions)
        r = 0
        for i in range(self.row, len(decisions)):
            self.setItem(i, 0, QTableWidgetItem(name_students[i]))
            self.setItem(i, 1, QTableWidgetItem(decisions[i]['status_msg']))
            self.setItem(i, 2, QTableWidgetItem(decisions[i]['status_runtime']))
            self.setItem(i, 3, QTableWidgetItem(decisions[i]['status_memory']))
            self.setItem(i, 4, QTableWidgetItem(decisions[i]['input']))
            self.setItem(i, 5, QTableWidgetItem(decisions[i]['code_output']))
            self.setItem(i, 6, QTableWidgetItem(decisions[i]['expected_output']))
            self.setItem(i, 7, QTableWidgetItem(decisions[i]['full_compile_error']))
            if decisions[i]['status_msg'] == 'Accepted':
                color = QColor(78, 255, 150)
            else:
                color = QColor(255, 121, 118)
            for j in range(8):
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