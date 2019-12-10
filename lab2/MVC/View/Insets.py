from PyQt5 import QtWidgets


class Insets(QtWidgets.QTabWidget):
    def __init__(self, mw, txtArea):
        super(Insets, self).__init__()
        self.all_tabs = []
        self.build_widgets(mw, txtArea)

    def build_widgets(self, mw, txtArea):
        self.all_tabs.append(txtArea)
        self.addTab(self.all_tabs[0], 'Логи')
        self.all_tabs.append(mw)
        self.addTab(self.all_tabs[1], 'Таблица')

    def updateTable(self, mw):
        index = self.currentIndex()
        print(index)
        self.removeTab(index)
        self.all_tabs[1] = mw
        self.addTab(self.all_tabs[1], 'Таблица')