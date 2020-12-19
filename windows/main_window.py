import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QListWidgetItem

from widgets import *

from requests import get, put, post, delete

from info import URL

 
class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)

        self.product_a.triggered.connect(self.create_prod)
        self.part_a.triggered.connect(self.create_part)

        self.operation_a.triggered.connect(self.create_operation)
        self.machine_a.triggered.connect(self.create_machine)
        self.worker_a.triggered.connect(self.create_worker)
        self.additional_a.triggered.connect(self.create_additional)
        self.material_a.triggered.connect(self.create_material)

        self.product_c.triggered.connect(self.change_product)

        self.operation_list.triggered.connect(self.see_operation)
        self.machine_list.triggered.connect(self.see_machine)
        self.worker_list.triggered.connect(self.see_worker)
        self.additional_list.triggered.connect(self.see_additional)
        self.material_list.triggered.connect(self.see_material)

        self.add_o.clicked.connect(self.add_operation)
        self.del_o.clicked.connect(self.del_operation)

        self.add_a.clicked.connect(self.add_additional)
        self.del_a.clicked.connect(self.del_additional)

        self.add_p.clicked.connect(self.add_part)
        self.del_p.clicked.connect(self.del_part)

        self.act.clicked.connect(self.product_upd)

        self.load(1)

    def create_part(self):
        window = Part()
        window.exec()

    def create_prod(self):
        post(URL + f'/api/product/0?title=title&r_coef=0.0&r_cost=1&w_cost=1')
        product_id = get(URL + '/api/products?ids=all').json()['result']['products'][-1]['id']
        self.ID.setText(str(product_id))
        self.load(product_id)

    def change_product(self):
        window = Product()
        window.exec()
        p_id = window.p_id
        if p_id != 0:
            self.load(p_id)

    def create_operation(self):
        window = Operation()
        window.exec()

    def create_machine(self):
        window = Machine()
        window.exec()

    def create_worker(self):
        window = Worker()
        window.exec()

    def create_additional(self):
        window = Additional()
        window.exec()

    def create_material(self):
        window = Material()
        window.exec()

    def see_operation(self):
        window = Operations()
        window.exec()

    def see_machine(self):
        window = Machines()
        window.exec()

    def see_worker(self):
        window = Workers()
        window.exec()

    def see_additional(self):
        window = Additionals()
        window.exec()

    def see_material(self):
        window = Materials()
        window.exec()

    def add_operation(self):
        window = AddOperation()
        window.exec()
        o_id = window.o_id
        if o_id != 0:
            item = QListWidgetItem(f'{window.o_title}; {window.o_time} ч.')
            item.setData(Qt.UserRole, (window.o_id, window.o_time))
            self.operations_list.addItem(item)

    def del_operation(self):
        id = self.ID.text()
        item = self.operations_list.takeItem(self.operations_list.currentRow())
        if item:
            o_id = item.data(Qt.UserRole)[0]
            delete(URL + f'/api/operationproduct?operation_id={o_id}&product_id={id}')
            self.parts_list.removeItemWidget(item)

    def add_additional(self):
        window = AddAdditional()
        window.exec()
        a_id = window.a_id
        if a_id != 0:
            item = QListWidgetItem(f'{window.a_title} x{window.a_count}')
            item.setData(Qt.UserRole, (window.a_id, window.a_count))
            self.additionals_list.addItem(item)

    def del_additional(self):
        id = self.ID.text()
        item = self.additionals_list.takeItem(self.additionals_list.currentRow())
        if item:
            a_id = item.data(Qt.UserRole)[0]
            delete(URL + f'/api/additionalproduct?additional_id={a_id}&product_id={id}')
            self.parts_list.removeItemWidget(item)

    def add_part(self):
        window = AddPart()
        window.exec()
        p_id = window.p_id
        if p_id != 0:
            item = QListWidgetItem(f'{window.p_title}')
            item.setData(Qt.UserRole, window.p_id)
            self.parts_list.addItem(item)

    def del_part(self):
        id = self.ID.text()
        item = self.parts_list.takeItem(self.parts_list.currentRow())
        if item:
            p_id = item.data(Qt.UserRole)
            delete(URL + f'/api/partproduct?part_id={p_id}&product_id={id}')
            self.parts_list.removeItemWidget(item)

    def product_upd(self):
        id = self.ID.text()

        title = self.name.text()
        r_coef = self.profitability.text()
        if not r_coef:
            r_coef = 0.0
        
        put(URL + f'/api/product/{id}?title={title}&r_coef={r_coef}')

        for indx in range(self.operations_list.count()):
            o_id, time = self.operations_list.item(indx).data(Qt.UserRole)
            post(URL + f'/api/operationproduct?operation_id={o_id}&product_id={id}&time={time}')

        for indx in range(self.additionals_list.count()):
            a_id, count = self.additionals_list.item(indx).data(Qt.UserRole)
            post(URL + 
                     f'/api/additionalproduct?additional_id={a_id}&product_id={id}&count={count}')

        for indx in range(self.parts_list.count()):
            p_id = self.parts_list.item(indx).data(Qt.UserRole)
            post(URL + f'/api/partproduct?part_id={p_id}&product_id={id}')

        get(URL + f'/api/productcost/{id}')

        self.load(id)
    
    def load(self, p_id):
        response = get(URL + f'/api/product/{p_id}')
        if not response:
            self.create_prod()
            return

        self.operations_list.clear()
        self.additionals_list.clear()
        self.parts_list.clear()

        product_info = response.json()['result']['product']

        self.ID.setText(str(product_info['id']))

        self.name.setText(product_info['title'])
        self.r_cost.setText(str(product_info['retale cost']))
        self.w_cost.setText(str(product_info['wholesale cost']))
        self.profitability.setText(str(product_info['profitability']))

        for add in product_info['additionals']:
            item = QListWidgetItem(f"{add['title']} x{add['count']}")
            item.setData(Qt.UserRole, (add['id'], add['count']))
            self.additionals_list.addItem(item)
        
        for oper in product_info['operations']:
            item = QListWidgetItem(f"{oper['title']}; время {oper['time']} ч.")
            item.setData(Qt.UserRole, (oper['id'], oper['time']))
            self.operations_list.addItem(item)
        
        for part in product_info['parts']:
            item = QListWidgetItem(part['title'])
            item.setData(Qt.UserRole, part['id'])
            self.parts_list.addItem(item)


descktop_app = QApplication(sys.argv)
ex = Application()
ex.show()
sys.exit(descktop_app.exec_())
