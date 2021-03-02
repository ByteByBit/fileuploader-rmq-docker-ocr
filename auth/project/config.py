from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class FlaskConfig:

    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")


class SMBConfig:

    HOST = environ.get('SAMBA_HOST')
    USERNAME = environ.get('SAMBA_USERNAME')
    PASSWORD = environ.get('SAMBA_PASSWORD')
    PORT = int(environ.get('SAMBA_PORT'))
    ROOT_FOLDER = environ.get('SAMBA_ROOT_FOLDER')
    ORIGINAL_FOLDER = environ.get('SAMBA_ORIGINAL_FOLDER')
    PREPROCESSED_FOLDER = environ.get('SAMBA_PREPROCESSED_FOLDER')


class RMQConfig:

    HOST = environ.get('RMQ_HOST')
    PORT = environ.get('RMQ_PORT')
    USERNAME = environ.get('RMQ_USER')
    PASSWORD = environ.get('RMQ_PASSWORD')