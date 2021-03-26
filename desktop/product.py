from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog

from requests import get

from desktop import URL, UI_PATH

 
class Product(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH + 'product.ui', self)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        self.p_id = 0

        self.ok.clicked.connect(self.adding)
        self.closing.clicked.connect(self.close)

        self.loading()


    def loading(self):
        self.products.addItem('')

        products = get(URL + f'/api/products?ids=all').json()['result']['products']
        for indx, product in enumerate(products):
            self.products.addItem(product['title'])
            self.products.setItemData(indx + 1, product['id'], Qt.UserRole)

    def adding(self):
        product_id = self.products.currentData()

        if not product_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберете продукт!')
        else:
            self.p_id = product_id

            self.close()
