from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog

from requests import get, put, post

from info import URL

 
class Additional(QDialog):
    def __init__(self, mode='a', a_id=1):
        super().__init__()
        uic.loadUi('./ui/additional.ui', self)
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
        self.price.valueFromText(str(additional['price']))


class Additionals(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/additionals.ui', self)

        pass
