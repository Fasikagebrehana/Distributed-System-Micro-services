import pika
import json
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def callback(ch, method, properties, body):
    """
    Callback function to process incoming messages.
    """
    try:
        message = json.loads(body)
        logging.info(f"Received message: {message}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode message: {body}. Error: {e}")

# Consume from Fanout Exchange
def consume_from_fanout_exchange(exchange_name):
    """
    Connects to RabbitMQ and listens to a fanout exchange.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

        # Declare a temporary queue
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind the queue to the exchange
        channel.queue_bind(exchange=exchange_name, queue=queue_name)

        logging.info(f"Waiting for messages in fanout exchange '{exchange_name}'. To exit press CTRL+C")
        
        # Start consuming messages
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Error in fanout exchange consumer: {e}")
        sys.exit(1)

# Consume from Topic Exchange
def consume_from_topic_exchange(exchange_name, binding_key):
    """
    Connects to RabbitMQ and listens to a topic exchange with a specific binding key.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

        # Declare a temporary queue
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind the queue to the exchange with the routing key
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

        logging.info(f"Waiting for messages in topic exchange '{exchange_name}' with binding key '{binding_key}'. To exit press CTRL+C")
        
        # Start consuming messages
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Error in topic exchange consumer: {e}")
        sys.exit(1)

# Main Function
if __name__ == "__main__":
    # Exchange and routing key configurations
    fanout_exchange = 'task_updates'
    topic_exchange = 'task_notifications'
    topic_binding_key = 'user.manager'

    # Choose which consumer to run (Uncomment the desired one)
    # Fanout exchange consumer
    # consume_from_fanout_exchange(fanout_exchange)

    # Topic exchange consumer
    consume_from_topic_exchange(topic_exchange, topic_binding_key)
