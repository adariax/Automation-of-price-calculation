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


from app.api import material

api = Api(app)
api.add_resource(material.MaterialResource, '/api/material/<int:m_id>')
