from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

from app import models


def get_db_session() -> db.Session:
    return db.session

login_manager = LoginManager(app)

from app.data import posts_api, users_api, posts_callback

api = Api(app)
# api.add_resource(users_api.UsersResource, '')

# app.register_blueprint(users_api.blueprint)