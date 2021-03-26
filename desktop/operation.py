from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QTableWidgetItem

from requests import get, put, post

from desktop import URL, UI_PATH

 
class Operation(QDialog):
    def __init__(self, mode='a', o_id=1):
        super().__init__()
        uic.loadUi(UI_PATH + 'operation.ui', self)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.loading_machines()

        self.mode = mode
        self.id = o_id

        if self.mode == 'p':
            self.load()

    def loading_machines(self):
        self.machines.addItem('')

        machines = get(URL + f'/api/machines?ids=all').json()['result']['machines']
        for indx, machine in enumerate(machines):
            self.machines.addItem(machine['title'])
            self.machines.setItemData(indx + 1, machine['id'], Qt.UserRole)

    def adding(self):
        title = self.title.text()
        machine_id = self.machines.currentData()

        if title == '' or machine_id == None:
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        else:
            if self.mode == 'p':
                put(URL + f'/api/operation/{self.id}?title={title}&machine_id={machine_id}')
                self.close()
            elif self.mode == 'a':
                post(URL + f'/api/operation/0?title={title}&machine_id={machine_id}')
                self.close()

    def load(self):
        operation = get(URL + f'/api/operation/{self.id}').json()['result']['operation']

        self.title.setText(operation['title'])


class Operations(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'operations.ui', self)
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.table.cellClicked.connect(self.row_focus)
        self.table.cellDoubleClicked.connect(self.edit_operation)

        self.fields = 0
        self.load()

    def row_focus(self):  # select all column of chosen film
        for i in range(self.fields):
            self.table.item(self.table.currentRow(), i).setSelected(True)

    def edit_operation(self):
        self.row_focus()

        o_id = self.table.currentItem().data(Qt.UserRole)

        window = Operation(mode='p', o_id=o_id)
        window.exec()

        self.load()

    def load(self):
        operations = get(URL + f'/api/operations?ids=all').json()['result']['operations']

        if not operations:
            QMessageBox.warning(self, 'Внимание', 'Операций нет')
            return

        self.fields = len(operations[0].keys()) - 1

        self.table.setColumnCount(self.fields)
        self.table.setHorizontalHeaderLabels(('Название', 'Оборудование'))

        self.table.setRowCount(0)
        for i, operation in enumerate(operations):
            self.table.setRowCount(self.table.rowCount() + 1)

            item = QTableWidgetItem(operation['title'])
            item.setData(Qt.UserRole, operation['id'])
            self.table.setItem(i, 0, item)

            item = QTableWidgetItem(str(operation['machine']['title']))
            item.setData(Qt.UserRole, operation['id'])
            self.table.setItem(i, 1, item)

        self.table.resizeColumnsToContents()
