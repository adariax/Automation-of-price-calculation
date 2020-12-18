from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QDialog

from requests import get, put, post

from info import URL

 
class Material(QDialog):
    def __init__(self, mode='a', m_id=1):
        super().__init__()
        uic.loadUi('./ui/material.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.mode = mode
        self.id = m_id

        if self.mode == 'p':
            self.load() 

    def adding(self):
        title = self.title.text()
        price = self.price.value()
        waste = self.waste.value()

        if title == '' or price == 0.0 or waste == 0.0:
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        else:
            if self.mode == 'p':
                put(URL + f'/api/material/{self.id}?title={title}&waste_coef={waste}&price={price}')
                self.close()
            elif self.mode == 'a':
                post(URL + f'/api/material/0?title={title}&waste_coef={waste}&price={price}')
                self.close()

    def load(self):
        material = get(URL + f'/api/material/{self.id}').json()['result']['material']

        self.title.setText(material['title'])
        self.price.valueFromText(str(material['price']))
        self.waste.valueFromText(str(material['waste_coef']))


class Materials(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/materials.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        pass
