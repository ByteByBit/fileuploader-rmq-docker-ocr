import json 

import pika

from project.config import RMQConfig

class LoggerMsg():

    def __init__(self, t: str, msg: str, l_name: str):
        self.type = t
        self.msg = msg
        self.logger_name = l_name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class RMQ():

    HOST = 'rmq_server'
    PORT = 5672
    USERNAME = 'guest1'
    PASSWORD = 'guest1'

    def __init__(self):
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

    def close(self):
        self._conn.close()