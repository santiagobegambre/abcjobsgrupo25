import logging

import pika


class rabbitMQServer():
    """
    Producer component that will publish message and handle
    connection and channel interactions with RabbitMQ.
    """

    def __init__(self, queue, host, routing_key, username, password, exchange=''):
        self._queue = queue
        self._host = host
        self._routing_key = routing_key
        self._exchange = exchange
        self._username = username
        self._password = password
        self.start_server()

    def start_server(self):
        self.create_channel()
        self.create_exchange()
        self.create_bind()
        logging.info("Channel created...")

    def create_channel(self):
        credentials = pika.PlainCredentials(username=self._username, password=self._password)
        parameters = pika.ConnectionParameters(self._host, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        logging.info("Create_channel...")

    def create_exchange(self):
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='direct',
            passive=False,
            durable=True,
        )
        self._channel.queue_declare(queue=self._queue, durable=False)
        logging.info("Create exchange...")

    def create_bind(self):
        self._channel.queue_bind(
            queue=self._queue,
            exchange=self._exchange,
            routing_key=self._routing_key
        )
        self._channel.basic_qos(prefetch_count=1)
        logging.info("Create bind...")

    @staticmethod
    def callback(channel, method, properties, body):
        logging.info(f'Consumed message {body.decode()} from queue on {channel}')

    def get_messages(self):
        try:
            self._channel.basic_consume(
                queue=self._queue,
                on_message_callback=rabbitMQServer.callback,
                auto_ack=True
            )
            self._channel.start_consuming()
            self._channel.close()
            logging.info("Receiver Message End")
        except Exception as e:
            logging.debug(f'Exception: {e}')
