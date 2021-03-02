import json
import os
import datetime

from flask import Blueprint, request

from .models import User, Item
from .utils import authenticate, save_file_tmp_folder, FileStorage, RMQ, LoggerMsg


upload = Blueprint('upload', __name__)

EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.tiff'}


@upload.route('/upload', methods=['POST'])
def store_file():    
    
    email = request.form.get('email')
    password = request.form.get('password')
    priority = request.form.get('priority')

    # Get user id from auth container.
    user_id = authenticate(email=email, password=password)

    if not user_id:
        return 'Invalid credentials.', 401


    rmq = RMQ()

    # Logger.
    msg = 'User [{}] logging in at [{}]'.format(
        email, datetime.datetime.now()
    )
    m = LoggerMsg(t='info', msg=msg, l_name='uploader_api')

    rmq.publish(msg=m.toJSON(), exchange='logs')

    f = request.files['file']
    _, file_extension = os.path.splitext(f.filename)

    if not file_extension in EXTENSIONS:
        return 'Invalid file type', 503

    user = User(user_id)

    # Create user if not exists.
    user.validate_user()
    # Get the amount of submitted jobs.
    count = user.get_count()

    item = Item(user.id, count)
    # Set the uploaded binary.
    item.set(f)

    storage = FileStorage(user.id)

    # Connect and store file in Samba server.
    if not storage.upload(item.raw_item, item.storage_name):

        # Save item to tmp folder.
        save_file_tmp_folder(f, item.job_id, user.id, file_extension)

        msg = 'User [{}] temporarily stored [{}]'.format(user.id, item.original_name)
        m = LoggerMsg(t='warning', msg=msg, l_name='uploader_api')

        rmq.publish(msg=m.toJSON(), exchange='logs')

        rmq.close()
        return 'File uploaded successfully.', 200

    user.increase()

    # Logger.
    msg = 'User [{}] stored [{}] as [{}] at [{}]'.format(
        user.id, item.original_name, item.storage_name, datetime.datetime.now())

    m = LoggerMsg(t='info', msg=msg, l_name='uploader_api')

    rmq.publish(
        msg=m.toJSON(), exchange='logs'
    )


    message = {
        'storage_name': item.storage_name,
        'priority': priority,
        'job_id': item.job_id,
        'user_id': user.id,
        'extension': file_extension  
    }
        
        
    m = json.dumps(message)

    # Publish job to broker.
    rmq.publish(
        msg=m, exchange='preprocess'
    )

    rmq.close()

    # Upload done - success.
    return 'File uploaded successfully.', 200
