# task_service/rabbitmq_producer.py
import pika
import json

def publish_message(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Publish the message
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    print(f"Message sent to queue '{queue_name}': {message}")
    connection.close()
    
if __name__ == "__main__":
    queue_name = 'task_queue'
    message = {'task': 'Test message'}
    publish_message(queue_name, message)