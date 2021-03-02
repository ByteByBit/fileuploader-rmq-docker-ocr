from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class RMQConfig:

    HOST = environ.get('RMQ_HOST')
    PORT = int(environ.get('RMQ_PORT'))
    USERNAME = environ.get('RMQ_USER')
    PASSWORD = environ.get('RMQ_PASSWORD')