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

from app.api_resources import material, materials

api.add_resource(material.MaterialResource, '/api/material/<int:m_id>')
api.add_resource(materials.MaterialsResource, '/api/materials')

from app.api_resources import worker, workers

api.add_resource(worker.WorkerResource, '/api/worker/<int:w_id>')
api.add_resource(workers.WorkersResource, '/api/workers')

from app.api_resources import machine, machines

api.add_resource(machine.MachineResource, '/api/machine/<int:m_id>')
api.add_resource(machines.MachinesResource, '/api/machines')

from app.api_resources import operation, operations

api.add_resource(operation.OperationResource, '/api/operation/<int:o_id>')
api.add_resource(operations.OperationsResource, '/api/operations')

from app.api_resources import additional, additionals

api.add_resource(additional.AdditionalResource, '/api/additional/<int:a_id>')
api.add_resource(additionals.AdditionalsResource, '/api/additionals')

from app.api_resources import constant, constants

api.add_resource(constant.ConstantResource, '/api/constant/<int:c_id>')
api.add_resource(constants.ConstantsResource, '/api/constants')