import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLineEdit, QLabel, QMainWindow, QGridLayout


class VerificationWindow(QMainWindow):

    def __init__(self, controller, parent):
        # Обязательно нужно вызвать метод супер класса
        super(VerificationWindow, self).__init__(parent)
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.str = QLabel('Введите код верификации отправленный\nна почту t*************@mail.ru', self)
        self.line = QLineEdit()
        self.line.setMinimumWidth(50)
        self.setMaximumWidth(100)
        self.setMaximumHeight(100)
        self.setWindowTitle('Window Verification')
        self.btn = QPushButton('Open', self)
        self.btn.clicked.connect(self.click_btn)
        q = QWidget(self)
        box = QGridLayout(self)
        box.addWidget(self.str, 0, 0)
        box.addWidget(self.line, 1, 0)
        box.addWidget(self.btn, 2, 0)
        q.setLayout(box)
        self.setCentralWidget(q)
        self.show()

    def click_btn(self):
        if self.line.text() != '':
            self.controller.verification(self.line.text())
