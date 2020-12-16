from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

from app import models

db.create_all()


def get_db_session() -> db.Session:
    return db.session


api = Api(app)  # TODO: check user's possibility to change data

from app.api_resources import material

api.add_resource(material.MaterialResource, '/api/material/<int:m_id>')
api.add_resource(material.MaterialsResource, '/api/materials')

from app.api_resources import worker

api.add_resource(worker.WorkerResource, '/api/worker/<int:w_id>')
api.add_resource(worker.WorkersResource, '/api/workers')

from app.api_resources import machine

api.add_resource(machine.MachineResource, '/api/machine/<int:m_id>')
api.add_resource(machine.MachinesResource, '/api/machines')

from app.api_resources import operation

api.add_resource(operation.OperationResource, '/api/operation/<int:o_id>')
api.add_resource(operation.OperationsResource, '/api/operations')

from app.api_resources import additional

api.add_resource(additional.AdditionalResource, '/api/additional/<int:a_id>')
api.add_resource(additional.AdditionalsResource, '/api/additionals')

from app.api_resources import constant

api.add_resource(constant.ConstantResource, '/api/constant/<int:c_id>')
api.add_resource(constant.ConstantsResource, '/api/constants')

from app.api_resources import part

api.add_resource(part.PartResource, '/api/part/<int:p_id>')
api.add_resource(part.PartsResource, '/api/parts')

from app.api_resources import product

api.add_resource(product.ProductResource, '/api/product/<int:p_id>')
api.add_resource(product.ProductsResource, '/api/products')
