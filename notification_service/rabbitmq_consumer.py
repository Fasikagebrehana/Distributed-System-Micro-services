import pika
import json

def callback(ch, method, properties, body):
    message = json.loads(body)  # Deserialize the JSON message
    print(f"Received message: {message}")
    # Add your logic here (e.g., sending email, SMS, etc.)

def consume_messages(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    print("Connected to RabbitMQ")
    channel = connection.channel()

    # Declare the queue (must match producer)
    channel.queue_declare(queue=queue_name, durable=True)
    print(f"Queue '{queue_name}' declared.")

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Waiting for messages in {queue_name}. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    queue_name = 'task_queue'
    consume_messages(queue_name)