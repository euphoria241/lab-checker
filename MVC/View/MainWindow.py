import time

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("Работа с QTableWidget")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setColumnCount(8)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["Студент", "Статус", "Время выполнения", "Память", "Input", "Output", "Expected", "Error"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.table.horizontalHeaderItem(2).setToolTip("Column 3 ")
        self.table.horizontalHeaderItem(3).setToolTip("Column 4 ")
        self.table.horizontalHeaderItem(4).setToolTip("Column 5 ")
        self.table.horizontalHeaderItem(5).setToolTip("Column 6 ")
        self.table.horizontalHeaderItem(6).setToolTip("Column 7 ")
        self.table.horizontalHeaderItem(7).setToolTip("Column 8 ")

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)

        # заполняем первую строку


        grid_layout.addWidget(self.table, 0, 0)  # Добавляем таблицу в сетку

    def setRowsTable(self, decisions, name_students, pbar):
        self.pbar = pbar
        self.pbar.setValue(0)
        self.table.setRowCount(len(decisions))  # и одну строку в таблице
        self.size = 100 // len(decisions)
        for i in range(len(decisions)):
            self.table.setItem(i, 0, QTableWidgetItem(name_students[i]))
            self.table.setItem(i, 1, QTableWidgetItem(decisions[i]['status_msg']))
            self.table.setItem(i, 2, QTableWidgetItem(decisions[i]['status_runtime']))
            self.table.setItem(i, 3, QTableWidgetItem(decisions[i]['status_memory']))
            self.table.setItem(i, 4, QTableWidgetItem(decisions[i]['input']))
            self.table.setItem(i, 5, QTableWidgetItem(decisions[i]['code_output']))
            self.table.setItem(i, 6, QTableWidgetItem(decisions[i]['expected_output']))
            self.table.setItem(i, 7, QTableWidgetItem(decisions[i]['full_compile_error']))
            QTimer.singleShot(0, self.startLoop)
            qApp.processEvents()
        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()
        self.pbar.reset()

    def startLoop(self):
        time.sleep(0.05)
        value = self.pbar.value() + self.size
        self.pbar.setValue(value)