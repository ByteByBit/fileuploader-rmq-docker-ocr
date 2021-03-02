import tempfile
from io import BytesIO
import os
from os import environ, path
from dotenv import load_dotenv
import json

from PIL import Image
from smb.SMBConnection import SMBConnection
import pytesseract
import pika

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class SMBConfig:

    HOST = os.environ.get('HOST')
    USERNAME = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    PORT = int(os.environ.get('PORT'))
    ROOT_FOLDER = os.environ.get('ROOT_FOLDER')
    ORIGINAL_FOLDER = os.environ.get('ORIGINAL_FOLDER')
    PREPROCESSED_FOLDER = os.environ.get('PREPROCESSED_FOLDER')
    OCR_FOLDER = os.environ.get('OCR_FOLDER')

class FileStorage(SMBConfig):
    
    def __init__(self, user_id: str):
        super().__init__()
        self._conn = None
        self.user_id = user_id
        self.file = None
        self.original_folder = os.path.join(user_id, self.ORIGINAL_FOLDER)
        self.preproc_folder = os.path.join(user_id, self.PREPROCESSED_FOLDER)
        self.ocr_folder = os.path.join(user_id, self.OCR_FOLDER)

    def connect(self):
        self._conn = SMBConnection(
            self.USERNAME,self.PASSWORD, "","",use_ntlm_v2 = True)

        if self._conn.connect(self.HOST, self.PORT):
            return True

        return False

    def upload(self, file, folder, file_name):

        full_path = os.path.join(folder, file_name)

        if self._conn.storeFile(self.ROOT_FOLDER, full_path, file):
            return True

        return False
    
    def download(self, file_name):
        
        self.file = tempfile.NamedTemporaryFile()

        full_path = os.path.join(self.preproc_folder, file_name)

        if self._conn.retrieveFile(self.ROOT_FOLDER, full_path,  self.file):
            return True
        
        return False


class LoggerMsg():

    def __init__(self, t: str, msg: str, l_name: str):
        self.type = t
        self.msg = msg
        self.logger_name = l_name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class RMQConfig:

    HOST = os.environ.get('RMQ_HOST')
    USERNAME = os.environ.get('RMQ_USER')
    PASSWORD = os.environ.get('RMQ_PASSWORD')
    PORT = int(os.environ.get('RMQ_PORT'))

class RMQ(RMQConfig):

    def __init__(self):
        super().__init__()
        self._creds = pika.PlainCredentials(
            self.USERNAME, self.PASSWORD
        )

        self._conn =  pika.BlockingConnection(
            pika.ConnectionParameters(
            host=self.HOST, 
            port=self.PORT, 
            credentials=self._creds)
        )
        self._channel = self._conn.channel()

    def publish(self, msg, exchange: str):

        self._channel.exchange_declare(
            exchange=exchange, exchange_type='fanout'
        )

        self._channel.basic_publish(
            exchange=exchange, routing_key='', body=msg
        )

    def start_consumer(self, exchange: str, callback, *args):

        self._channel.exchange_declare(
            exchange=exchange, exchange_type='fanout'
        )
        res = self._channel.queue_declare(queue='', exclusive=True)
        queue_name = res.method.queue
        self._channel.queue_bind(exchange=exchange, queue=queue_name)
        print(' [*] Waiting for ocr tasks. To exit press CTRL+C')

        self._channel.basic_consume(
            queue=queue_name, 
            on_message_callback=callback, 
            auto_ack=True
        )
        self._channel.start_consuming()

    def close(self):
        self._conn.close()


def get_txt(img, lang: str = 'en'):

    image = Image.open(img)
    txt = pytesseract.image_to_string(image, lang=lang)
    return txt