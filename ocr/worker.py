#!/usr/bin/env python
from io import BytesIO
import datetime
import json 

from utils import FileStorage, get_txt, RMQ, LoggerMsg

                 
def callback(ch, method, properties, body):
    
    body = json.loads(body)

    user_id = body['user_id']
    storage_name = body['storage_name']
    job_id = body['job_id']
    extension = body['extension']
    priority = body['priority']

    # Logger.
    msg = 'Start, user [{}], storage name [{}], job ID [{}]'.format(user_id, storage_name, job_id)
    m = LoggerMsg(t='info', msg=msg, l_name='ocr')
    rmq.publish(msg=m.toJSON(), exchange='logs')

    storage = FileStorage(user_id)
    # Samba connection.
    if not storage.connect():
        # ! Implement temporary storage
        # ! and reporting issue.
        msg = 'Connecting to file storage server failed at [{}]'.format(datetime.datetime.now())
        m = LoggerMsg(t='critical', msg=msg, l_name='ocr')
        rmq.publish(msg=m.toJSON(), exchange='logs')
        return False

    if not storage.download(storage_name):
        # ! Implement temporary storage
        # ! and reporting issue.
        msg = 'Downloading file from storage server failed at [{}]'.format(datetime.datetime.now())
        m = LoggerMsg(t='critical', msg=msg, l_name='ocr')
        rmq.publish(msg=m.toJSON(), exchange='logs')
        return False

    result = get_txt(storage.file, 'dan')
    
    f_name = '{}.txt'.format(job_id)
    file = BytesIO(bytes(result,'ascii'))

    if not storage.upload(file, storage.ocr_folder, f_name):
        msg = 'Failed to store preprocessed file at [{}] user [{}], storage name [{}], job ID [{}]'.format(user_id, f_name, job_id, datetime.datetime.now())
        m = LoggerMsg(t='critical', msg=msg, l_name='ocr')
        rmq.publish(msg=m.toJSON(), exchange='logs')
        return False
    
    # Logger.
    msg = 'Done, user [{}], storage name [{}], job ID [{}] at [{}]'.format(user_id, f_name, job_id, datetime.datetime.now())
    m = LoggerMsg(t='info', msg=msg, l_name='ocr')
    rmq.publish(msg=m.toJSON(), exchange='logs')

rmq = RMQ()
rmq.start_consumer('ocr', callback)
