from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QTableWidgetItem

from requests import get, put, post

from info import URL

 
class Machine(QDialog):
    def __init__(self, mode='a', m_id=1):
        super().__init__()
        uic.loadUi('./ui/machine.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.loading_workers()

        self.mode = mode
        self.id = m_id

        if self.mode == 'p':
            self.load()

    def loading_workers(self):
        self.workers.addItem('')

        workers = get(URL + f'/api/workers?ids=all').json()['result']['workers']
        for indx, worker in enumerate(workers):
            self.workers.addItem(worker['title'])
            self.workers.setItemData(indx + 1, worker['id'], Qt.UserRole)

    def adding(self):
        title = self.title.text()
        price = self.price.value()
        worker_id = self.workers.currentData()

        if title == '' or worker_id == None or price == 0.0:
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        else:
            if self.mode == 'p':
                put(URL + f'/api/machine/{self.id}?title={title}&worker_id={worker_id}&price={price}')
                self.close()
            elif self.mode == 'a':
                post(URL + f'/api/machine/0?title={title}&worker_id={worker_id}&price={price}')
                self.close()

    def load(self):
        machine = get(URL + f'/api/machine/{self.id}').json()['result']['machine']

        self.title.setText(machine['title'])
        self.price.setValue(machine['price'])


class Machines(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/machines.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.table.cellClicked.connect(self.row_focus)
        self.table.cellDoubleClicked.connect(self.edit_machine)

        self.fields = 0
        self.load()

    def row_focus(self):  # select all column of chosen film
        for i in range(self.fields):
            self.table.item(self.table.currentRow(), i).setSelected(True)

    def edit_machine(self):
        self.row_focus()

        m_id = self.table.currentItem().data(Qt.UserRole)

        window = Machine(mode='p', m_id=m_id)
        window.exec()

        self.load()

    def load(self):
        machines = get(URL + f'/api/machines?ids=all').json()['result']['machines']

        self.fields = len(machines[0].keys()) - 1

        self.table.setColumnCount(self.fields)
        self.table.setHorizontalHeaderLabels(('Название', 'Цена', 'Рабочий'))

        self.table.setRowCount(0)
        for i, machine in enumerate(machines):
            self.table.setRowCount(self.table.rowCount() + 1)

            item = QTableWidgetItem(machine['title'])
            item.setData(Qt.UserRole, machine['id'])
            self.table.setItem(i, 0, item)

            item = QTableWidgetItem(str(machine['price']))
            item.setData(Qt.UserRole, machine['id'])
            self.table.setItem(i, 1, item)

            item = QTableWidgetItem(str(machine['worker']['title']))
            item.setData(Qt.UserRole, machine['id'])
            self.table.setItem(i, 2, item)

        self.table.resizeColumnsToContents()
