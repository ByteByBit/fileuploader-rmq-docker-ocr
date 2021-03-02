import datetime
import click
from smb.SMBConnection import SMBConnection
from flask import Blueprint

from .models import User
from .. import db
from .rmq import RMQ, LoggerMsg
from project.config import SMBConfig


class StorageFolders(SMBConfig):
    
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self._conn = None
        #self.upload_folder = self.user.folder  + '/' + self.ORIGINAL_FOLDER + '/'
        #self.preprocess_folder = self.user.folder  + '/' + self.PREPROCESSED_FOLDER 

    def connect(self):
        if not self._conn == None:
            return False
        
        self._conn = SMBConnection(
            self.USERNAME,self.PASSWORD, "","",use_ntlm_v2 = True)

        if self._conn.connect(self.HOST, self.PORT):
            return True

        return False


    def _directory_exist(self, dir: str):
        # ! exception handling.
        try:
            
            self._conn.listPath(self.ROOT_FOLDER, dir)
            return True
        except:
            return False

    def _create_dir(self, dir: str):
        # ! exception handling.
        try:
            self._conn.createDirectory(self.ROOT_FOLDER, dir)
            return True
        except:
            return False

    def create(self):
        # Main user folder.
        if not self._directory_exist(self.user_id):
            self._create_dir(self.user_id)
        user_root = self.user_id + '/'
        if not self._directory_exist(user_root + 'original'):
            self._create_dir(user_root + 'original')
        if not self._directory_exist(user_root + 'preprocessed'):
            self._create_dir(user_root + 'preprocessed')
        if not self._directory_exist(user_root + 'ocr_result'):
            self._create_dir(user_root + 'ocr_result')

        return True
user_cmd_bp = Blueprint('users', __name__)

@user_cmd_bp.cli.command('create')
@click.argument('name', nargs=1)
@click.argument('mail', nargs=1)
@click.argument('password', nargs=1)
def create(name, mail, password):

    rmq = RMQ()
    for i in range(5):
        str_i = str(i)
        m = str_i + mail
        user = User.query.filter_by(email=m).first() 
        if user:
            return 'User exist', 409 # HTTP 409 Conflic.

        user = User(
            username=name,
            email=m        
        )
        user.set_password(password=password)
        user.set_user_id()
        db.session.add(user)
        db.session.commit()
        sf = StorageFolders(user.user_id)
        # Logger.
        msg = 'User [{}], ID [{}] created  at [{}]'.format(
            m, user.user_id, datetime.datetime.now()
        )
        m = LoggerMsg(t='info', msg=msg, l_name='auth')

        rmq.publish(msg=m.toJSON(), exchange='logs')
        
        # Samba connection.
        if not sf.connect():
            # ! Implement temporary storage
            # ! and reporting issue.
            msg = 'Connecting to file storage server failed at [{}]'.format(datetime.datetime.now())
            m = LoggerMsg(t='critical', msg=msg, l_name='uploader_api')
            rmq.publish(msg=m.toJSON(), exchange='logs')

        # Samba connection.
        if not sf.create():
            # ! Implement temporary storage
            # ! and reporting issue.
            msg = 'Creating user folders failed. [{}]'.format(datetime.datetime.now())
            m = LoggerMsg(t='critical', msg=msg, l_name='uploader_api')
            rmq.publish(msg=m.toJSON(), exchange='logs')


    rmq.close()
    return 'User created! Email: {}, User_ID: {}'.format(mail, user.user_id)
