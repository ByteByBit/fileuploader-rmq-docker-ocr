import tempfile
from io import BytesIO
import os
import json

from PIL import Image
from smb.SMBConnection import SMBConnection
import pika

from config import SMBConfig, RMQConfig


class FileStorage(SMBConfig):
    ''' Store file in Samba file server. '''
    
    def __init__(self, user_id: str):

        super().__init__()
        self._conn = None
        self.file = None

        self.original_folder = os.path.join(user_id, self.ORIGINAL_FOLDER)
        self.preproc_folder = os.path.join(user_id, self.PREPROCESSED_FOLDER)


    def connect(self):
        ''' Connect to file server. '''

        self._conn = SMBConnection(
            self.USERNAME,self.PASSWORD, "","",use_ntlm_v2 = True)

        # Connection successful.
        if self._conn.connect(self.HOST, self.PORT):
            return True

        return False

    def upload(self, file, folder: str, file_name: str):
        ''' Upload file to file server. '''

        full_path = os.path.join(folder, file_name)

        # Upload successful.
        if self._conn.storeFile(self.ROOT_FOLDER, full_path, file):
            return True

        return False
    
    def download(self, folder: str, file_name: str):

        self.file = tempfile.NamedTemporaryFile()
        
        full_path = os.path.join(folder, file_name)

        # Download successful.
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

        print(' [*] Waiting for preprocess tasks.')

        self._channel.basic_consume(
            queue=queue_name, 
            on_message_callback=callback, 
            auto_ack=True
        )
        self._channel.start_consuming()

    def close(self):
        self._conn.close()


def resize(img, t):
    ''' Image resizer utility function. '''

    base_w = 600
    original_w = float(img.size[0])
    original_h = float(img.size[1])

    w_perc = float(base_w / original_w)
    new_height = int(original_h * w_perc)

    return img.resize((base_w, new_height), t)

def grayscale(img):
    ''' Grayscale image. '''

    return img.convert('LA')

def preprocess_img(image):
    ''' Convert image to grayscale and resize. '''

    img = Image.open(image)
    grayscaled = grayscale(img)
    resized = resize(grayscaled, Image.LANCZOS)

    new_img = BytesIO()
    resized.save(new_img, 'PNG', quality=100, optimize=True, progressive=True)
    new_img.seek(0)

    return new_img