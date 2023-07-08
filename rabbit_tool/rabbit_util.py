from rabbit_tool.rabbit_manager import QueueManager, rabbitmq_manager


# Define a callback function to process received messages
def callback(ch, method, properties, body):
    print(f'Received message: {body.decode()}')


def rabbit_publish_msg(queue_name: str, message: str):
    # Create a channel
    channel = rabbitmq_manager.create_channel()

    # Create a queue manager instance
    queue_manager = QueueManager(channel)

    # Declare a queue
    queue_manager.declare_queue(queue_name)

    # Publish a message to the queue
    return queue_manager.publish_message(queue_name, message)


def rabbit_consume_msg(queue_name: str,):
    # Create a channel
    channel = rabbitmq_manager.create_channel()

    # Create a queue manager instance
    queue_manager = QueueManager(channel)

    queue_manager.declare_queue(queue_name)

    # Consume messages from the queue
    queue_manager.consume_queue(queue_name, callback)
