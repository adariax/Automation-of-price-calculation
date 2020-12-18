import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QListWidgetItem

from requests import get, put, post, delete

from info import DOMEN

 
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)

        '''self.del_o.clicked.connect(self.delette_product_operation)
        self.add_o.clicked.connect(self.add_product_operation)

        self.del_a.clicked.connect(self.delette_product_additional)
        self.add_a.clicked.connect(self.add_product_additional)

        self.del_p.clicked.connect(self.delette_product_part)
        self.add_ex.clicked.connect(self.add_existing_part)
        self.crt_new.clicked.connect(self.create_add_part)

        self.act.clicked.connect(self.product_act)'''

        self.load()
    
    def load(self):
        response = get('http://' + DOMEN + '/api/product/1')
        if not response:
            return

        product_info = response.json()['result']['product']

        self.ID.setText(str(product_info['id']))

        self.name.setText(product_info['title'])
        self.r_cost.setText(str(product_info['retale cost']))
        self.w_cost.setText(str(product_info['wholesale cost']))
        self.profitability.setText(str(product_info['profitability']))

        for add in product_info['additionals']:
            item = QListWidgetItem(f"{add['title']} x{add['count']}")
            item.setData(Qt.UserRole, add['id'])
            self.additionals_list.addItem(item)
        
        for oper in product_info['operations']:
            item = QListWidgetItem(f"{oper['title']}; время {oper['time']} ч.")
            item.setData(Qt.UserRole, oper['id'])
            self.operations_list.addItem(item)
        
        for part in product_info['parts']:
            item = QListWidgetItem(part['title'])
            item.setData(Qt.UserRole, part['id'])
            self.parts_list.addItem(item)


descktop_app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(descktop_app.exec_())