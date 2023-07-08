import pika

from webhook import settings


class RabbitMQManager:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)

    def get_connection(self):
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials
        )
        return pika.BlockingConnection(parameters)

    def create_channel(self):
        connection = self.get_connection()
        return connection.channel()


class QueueManager:
    def __init__(self, channel):
        self.channel = channel

    def declare_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)

    def publish_message(self, queue_name, message):
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    def consume_queue(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()


# RabbitMQ connection details
RABBITMQ_HOST = settings.RABBITMQ_HOST
RABBITMQ_PORT = settings.RABBITMQ_PORT
RABBITMQ_USERNAME = settings.RABBITMQ_USERNAME
RABBITMQ_PASSWORD = settings.RABBITMQ_PASSWORD

# Create a RabbitMQ manager instance
rabbitmq_manager = RabbitMQManager(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    username=RABBITMQ_USERNAME,
    password=RABBITMQ_PASSWORD
)
