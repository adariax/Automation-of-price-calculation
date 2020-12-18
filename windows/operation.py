from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog

from requests import get, put, post

from info import URL

 
class Operation(QDialog):
    def __init__(self, mode='a', o_id=1):
        super().__init__()
        uic.loadUi('./ui/operation.ui', self)
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


class Operations(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/operations.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        pass
