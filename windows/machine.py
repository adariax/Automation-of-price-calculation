from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog

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
        self.price.valueFromText(str(machine['price']))


class Machines(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/machines.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        pass
