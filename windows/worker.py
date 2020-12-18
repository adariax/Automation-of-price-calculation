from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog

from requests import get, put, post

from info import URL

 
class Worker(QDialog):
    def __init__(self, mode='a', w_id=1):
        super().__init__()
        uic.loadUi('./ui/worker.ui', self)
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
        self.price.valueFromText(str(worker['price']))


class Workers(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/workers.ui', self)

        pass
