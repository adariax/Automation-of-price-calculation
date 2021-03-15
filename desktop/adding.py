from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QListWidgetItem

from requests import get, put, post

from desktop import URL, UI_PATH

 
class AddOperation(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'add_operation.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        self.o_id = 0
        self.o_title = 0
        self.o_time = 0.0

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.loading()


    def loading(self):
        self.operations.addItem('')

        operations = get(URL + f'/api/operations?ids=all').json()['result']['operations']
        for indx, operation in enumerate(operations):
            self.operations.addItem(operation['title'])
            self.operations.setItemData(indx + 1, operation['id'], Qt.UserRole)

    def adding(self):
        operation_id = self.operations.currentData()
        time = self.time.value()

        if not operation_id or time == 0.0:
            QMessageBox.warning(self, 'Ошибка', 'Зполнены не все поля!')
        else:
            self.o_id = operation_id
            self.o_title = self.operations.currentText()
            self.o_time = round(time / (60 * 60), 3)

            self.close()


class AddAdditional(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/add_additional.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        self.a_id = 0
        self.a_title = 0
        self.a_count = 0.0

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.loading()


    def loading(self):
        self.additionals.addItem('')

        additionals = get(URL + f'/api/additionals?ids=all').json()['result']['additionals']
        for indx, additional in enumerate(additionals):
            self.additionals.addItem(additional['title'])
            self.additionals.setItemData(indx + 1, additional['id'], Qt.UserRole)

    def adding(self):
        additional_id = self.additionals.currentData()
        count = self.count.value()

        if not additional_id or count == 0.0:
            QMessageBox.warning(self, 'Ошибка', 'Зполнены не все поля!')
        else:
            self.a_id = additional_id
            self.a_title = self.additionals.currentText()
            self.a_count = count

            self.close()


class AddPart(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/parts.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        self.p_id = 0
        self.p_title = 0

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.loading()

    def loading(self):
        self.parts.addItem('')

        parts = get(URL + f'/api/parts?ids=all').json()['result']['parts']
        for indx, part in enumerate(parts):
            self.parts.addItem(part['title'])
            self.parts.setItemData(indx + 1, part['id'], Qt.UserRole)

    def adding(self):
        part_id = self.parts.currentData()

        if not part_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберете деталь!')
        else:
            self.p_id = part_id
            self.p_title = self.parts.currentText()

            self.close()
