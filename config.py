class Config(object):
    FLASK_APP = 'main.py'

    SECRET_KEY = ''

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db\\db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    TESTING = False
    DEBUG = True
