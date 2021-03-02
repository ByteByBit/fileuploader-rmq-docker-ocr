import os
import json 

import pika
from smb.SMBConnection import SMBConnection

from ..config import SMBConfig, RMQConfig


def authenticate(email: str, password: str):
    ''' 
    Authenticate upload request by sending
    a request to 'auth' docker container. 
    '''

    import requests

    req_data = {
        'email': email,
        'password': password
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    res = requests.post(os.environ.get('AUTH_URI'), json=req_data, headers=headers)

    if res.status_code == 200 and len(res.text) == 36:
        #  Auth returned the UID of the user.
        return res.text

    # Auth failed.
    return False


def save_file_tmp_folder(file, job_id: str, user_id: str, ext: str):
    ''' Save file to tmp folder. '''

    full_path = './tmp/{}-{}{}'.format(job_id, user_id, ext)
    file.save(full_path)


class FileStorage(SMBConfig):
    ''' Store file in Samba file server. '''

    def __init__(self, user_id: str):

        super().__init__()
        self._conn = None
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


    def upload(self, img, file_name):
        ''' Upload file to file server. '''

        if not self.connect():
            return False

        # Create full path with filename.
        full_path = os.path.join(self.original_folder, file_name)
        
        img.seek(0)

        # Uploading failed.
        if not self._conn.storeFile(self.ROOT_FOLDER, full_path, img):
            return False

        return True

class LoggerMsg():
    ''' Log message object for 'Logger' container. '''

    def __init__(self, t: str, msg: str, l_name: str):

        # Log level.
        self.type = t
        self.msg = msg
        # Logger name.
        self.logger_name = l_name

    def toJSON(self):
        ''' Convert itself to JSON. '''

        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class RMQ(RMQConfig):

    ''' RabbitMQ, connect and publish. '''

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

    def publish(self, msg: json, exchange: str):
        ''' Publish message to broker. '''
        
        self._channel.exchange_declare(
            exchange=exchange, exchange_type='fanout'
        )

        self._channel.basic_publish(
            exchange=exchange, routing_key='', body=msg
        )

    def close(self):
        self._conn.close()
