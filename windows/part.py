from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QListWidgetItem

from widgets import AddOperation

from requests import get, put, post

from info import URL

 
class Part(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/part.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.add.clicked.connect(self.add_operation)
        self.delete_operation.clicked.connect(self.del_operation)

        self.loading_materials()

    def loading_materials(self):
        self.materials.addItem('')

        materials = get(URL + f'/api/materials?ids=all').json()['result']['materials']
        for indx, material in enumerate(materials):
            self.materials.addItem(material['title'])
            self.materials.setItemData(indx + 1, material['id'], Qt.UserRole)
    
    def del_operation(self):
        self.operations.removeItemWidget(self.operations.takeItem(self.operations.currentRow()))

    def add_operation(self):
        window = AddOperation()
        window.exec()
        o_id = window.o_id
        if o_id != 0:
            item = QListWidgetItem(f'{window.o_title}; {window.o_time} ч.')
            item.setData(Qt.UserRole, (window.o_id, window.o_time))
            self.operations.addItem(item)

    def adding(self):
        title = self.title.text()
        material_id = self.materials.currentData()
        count = self.count.value()

        if not title or not material_id or not count:
            QMessageBox.warning(self, 'Ошибка', 'Заполнены не все поля')
        else:
            post(URL + 
                 f'/api/part/0?title={title}&material_id={material_id}&material_count={count}')
            part_id = get(URL + '/api/parts?ids=all').json()['result']['parts'][-1]['id']
            for indx in range(self.operations.count()):
                o_id, time = self.operations.item(indx).data(Qt.UserRole)
                post(URL + f'/api/operationpart?operation_id={o_id}&part_id={part_id}&time={time}')
            self.close()


class Parts(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/part.ui', self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)