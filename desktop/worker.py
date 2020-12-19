from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QTableWidgetItem

from requests import get, put, post

from info import URL

 
class Worker(QDialog):
    def __init__(self, mode='a', w_id=1):
        super().__init__()
        uic.loadUi('ui/worker.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.mode = mode
        self.id = w_id

        if self.mode == 'p':
            self.load() 

    def adding(self):
        title = self.title.text()
        price = self.price.value()

        if title == '' or price == '':
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        else:
            if self.mode == 'p':
                put(URL + f'/api/worker/{self.id}?title={title}&price={price}')
                self.close()
            elif self.mode == 'a':
                post(URL + f'/api/worker/0?title={title}&price={price}')
                self.close()

    def load(self):
        worker = get(URL + f'/api/worker/{self.id}').json()['result']['worker']

        self.title.setText(worker['title'])
        self.price.setValue(worker['price'])


class Workers(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/workers.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.table.cellClicked.connect(self.row_focus)
        self.table.cellDoubleClicked.connect(self.edit_worker)

        self.fields = 0
        self.load()

    def row_focus(self):  # select all column of chosen film
        for i in range(self.fields):
            self.table.item(self.table.currentRow(), i).setSelected(True)

    def edit_worker(self):
        self.row_focus()

        w_id = self.table.currentItem().data(Qt.UserRole)

        window = Worker(mode='p', w_id=w_id)
        window.exec()

        self.load()

    def load(self):
        workers = get(URL + f'/api/workers?ids=all').json()['result']['workers']

        self.fields = len(workers[0].keys()) - 2

        self.table.setColumnCount(self.fields)
        self.table.setHorizontalHeaderLabels(('Название', 'Цена'))

        self.table.setRowCount(0)
        for i, worker in enumerate(workers):
            self.table.setRowCount(self.table.rowCount() + 1)

            item = QTableWidgetItem(worker['title'])
            item.setData(Qt.UserRole, worker['id'])
            self.table.setItem(i, 0, item)

            item = QTableWidgetItem(str(worker['price']))
            item.setData(Qt.UserRole, worker['id'])
            self.table.setItem(i, 1, item)

        self.table.resizeColumnsToContents()
