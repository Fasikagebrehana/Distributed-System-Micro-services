# desktop_app/utils.py
import pika
import json

# Publish a message to a RabbitMQ exchange
def publish_message(exchange_name, exchange_type, routing_key, message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        # Publish the message
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(message))
        print(f"Message sent to {exchange_type} exchange '{exchange_name}' with routing key '{routing_key}': {message}")

        connection.close()
    except Exception as e:
        print(f"Error publishing message: {e}")

# Consume messages from a RabbitMQ queue
def consume_messages(queue_name, callback):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=queue_name)

        # Start consuming messages
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"Waiting for messages in queue '{queue_name}'. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        print(f"Error consuming messages: {e}")
