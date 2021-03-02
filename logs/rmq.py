import time

import pika

from config import RMQConfig


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

    def start_consumer(self, exchange: str, callback, wait_time: int, *args):
        time.sleep(wait_time)
        
        self._channel.exchange_declare(
            exchange=exchange, exchange_type='fanout'
        )
        res = self._channel.queue_declare(queue='', exclusive=True)
        queue_name = res.method.queue
        self._channel.queue_bind(exchange=exchange, queue=queue_name)
        print(' [*] Waiting for logger tasks. To exit press CTRL+C')

        self._channel.basic_consume(
            queue=queue_name, 
            on_message_callback=callback, 
            auto_ack=True
        )
        self._channel.start_consuming()

    def close(self):
        self._conn.close()