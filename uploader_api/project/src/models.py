import datetime
from os.path import splitext
from werkzeug.utils import secure_filename

from .. import db

class Uploads(db.Model):
    '''Upload counter table.'''

    __tablename__ = 'user_uploads_count'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.String(37),
        unique=True,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=db.func.now()
    )
    last_updated = db.Column(
        db.DateTime,  
        onupdate=datetime.datetime.now
    )
    count = db.Column(
        db.Integer,
        default=0
    )


class User:

    def __init__(self, user_id: str):

        self.id = user_id
        self.folder = '/' + self.id + '/'
        self.count = 0

    def validate_user(self):
        ''' '''

        user = db.session.query(Uploads) \
            .filter_by(user_id=self.id).first()
        if not user:
            self.create_user()      

    def create_user(self):

        uploads= Uploads(
            user_id=self.id,
            count=0
        )
        db.session.add(uploads)
        db.session.commit()
    
    def increase(self):
        ''' Increase user submitted jobs. '''

        db.session.query(Uploads).filter_by(user_id=self.id) \
            .update({'count': Uploads.count + 1})
        db.session.commit()
    
    def get_count(self):
        ''' Get the amount the user submitted. '''

        count = db.session.query(Uploads).filter_by(user_id=self.id) \
            .first().count

        if not count:
            count = 0

        return count 


class Item:
    ''' Document item. '''

    __tablename__ = 'items'

    def __init__(self, user_id: str, count: int):

        self.user_id = user_id
        self.raw_item = None
        self.extension = None
        self.storage_name = None
        self.original_name = None
        self.striped_filename = None
        self.created_ts = datetime.datetime.now()
        self.job_id = count

    def set(self, original_file):

        file_name = secure_filename(original_file.filename)
        
        self.original_name = file_name
        name, ext = splitext(self.original_name)
       
        self.striped_filename = name
        self.extension = ext
        self.raw_item = original_file.stream

        self.storage_name = self.get_filename()

    def get_filename(self):
        ''' Construct a filename for the storage server. '''
        return '{}{}'.format(
            str(self.job_id),
            self.extension
        )
