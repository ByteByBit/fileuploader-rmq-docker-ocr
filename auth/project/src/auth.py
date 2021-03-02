from flask import Blueprint, request
from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/auth', methods=['POST'])
def authenticate():
    ''' Authenticate user.'''

    params = request.get_json(silent=True)
    email = params['email']
    password = params['password']

    user = User.query.filter_by(email=email).first()    

    if  user and user.check_password(password):

        # Auth success,
        return user.user_id, 200
        
    # Auth failed.
    return 'Invalid', 401
