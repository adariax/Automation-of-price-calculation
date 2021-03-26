from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QTableWidgetItem

from requests import get, put, post

from desktop import URL, UI_PATH

 
class Additional(QDialog):
    def __init__(self, mode='a', a_id=1):
        super().__init__()
        uic.loadUi(UI_PATH + 'additional.ui', self)
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.mode = mode
        self.id = a_id

        if self.mode == 'p':
            self.load() 

    def adding(self):
        title = self.title.text()
        price = self.price.value()

        if title == '' or price == '':
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        else:
            if self.mode == 'p':
                put(URL + f'/api/additional/{self.id}?title={title}&price={price}')
                self.close()
            elif self.mode == 'a':
                post(URL + f'/api/additional/0?title={title}&price={price}')
                self.close()

    def load(self):
        additional = get(URL + f'/api/additional/{self.id}').json()['result']['additional']

        self.title.setText(additional['title'])
        self.price.setValue(additional['price'])


class Additionals(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'additionals.ui', self)
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.table.cellClicked.connect(self.row_focus)
        self.table.cellDoubleClicked.connect(self.edit_additional)

        self.fields = 0
        self.load()

    def row_focus(self):  # select all column of chosen film
        for i in range(self.fields):
            self.table.item(self.table.currentRow(), i).setSelected(True)

    def edit_additional(self):
        self.row_focus()

        a_id = self.table.currentItem().data(Qt.UserRole)

        window = Additional(mode='p', a_id=a_id)
        window.exec()

        self.load()

    def load(self):
        additionals = get(URL + f'/api/additionals?ids=all').json()['result']['additionals']

        if not additionals:
            QMessageBox.warning(self, 'Внимание', 'Доп. комплектующих нет')
            return

        self.fields = len(additionals[0].keys()) - 1

        self.table.setColumnCount(self.fields)
        self.table.setHorizontalHeaderLabels(('Название', 'Цена'))

        self.table.setRowCount(0)
        for i, additional in enumerate(additionals):
            self.table.setRowCount(self.table.rowCount() + 1)

            item = QTableWidgetItem(additional['title'])
            item.setData(Qt.UserRole, additional['id'])
            self.table.setItem(i, 0, item)

            item = QTableWidgetItem(str(additional['price']))
            item.setData(Qt.UserRole, additional['id'])
            self.table.setItem(i, 1, item)

        self.table.resizeColumnsToContents()
