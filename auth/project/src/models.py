import uuid

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db

class User(UserMixin, db.Model):
    '''User model.'''

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    user_id = db.Column(
        db.String(37),
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=db.func.now()
    )

    def set_user_id(self):
        ''' Set a unique 10 char long user id. '''
        
        id = uuid.uuid4()
        self.user_id = str(id)

    def set_password(self, password):
        '''Set hashed password.'''

        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        '''Validate password.'''

        return check_password_hash(self.password, password)
