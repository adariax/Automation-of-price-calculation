from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QListWidgetItem

from requests import get, put, post

from info import URL

 
class AddOperation(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/add_operation.ui', self)
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

        if operation_id == None or time == 0.0:
            QMessageBox.warning(self, 'Ошибка', 'Зполнены не все поля!')
        else:
           self.o_id = operation_id
           self.o_title = self.operations.currentText()
           self.o_time = time

           self.close()

