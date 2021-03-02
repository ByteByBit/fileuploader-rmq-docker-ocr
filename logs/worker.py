import logging
import logging.config
import json 

from rmq import RMQ


logging.config.fileConfig(
    'logging.conf', defaults={'logfilename': '/var/log/mylog.log'})

def callback(ch, method, properties, body):
    
    d = json.loads(body)
    msg = d['msg']
    logger_name = d['logger_name']
    logger = logging.getLogger(logger_name)
        
    if d['type'] == 'warning':
        logger.warning(msg=msg)
    elif d['type'] == 'debug':
        logger.debug(msg=msg)
    elif d['type'] == 'error':
        logger.error(msg=msg)
    elif d['type'] == 'critical':
        logger.critical(msg=msg)
    else:
        logger.info(msg=msg)

rmq = RMQ()
rmq.start_consumer('logs', callback, 0)