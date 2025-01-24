import socketio
import pika
import json
import threading

# Initialize a Socket.IO server
sio = socketio.Server(cors_allowed_origins="*")  # Allow cross-origin requests
app = socketio.WSGIApp(sio)

# RabbitMQ Consumer Thread
def rabbitmq_consumer(exchange_name, routing_key=None, exchange_type='fanout'):
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    # Declare a temporary queue
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue
    if exchange_type == 'topic' and routing_key:
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
    else:
        channel.queue_bind(exchange=exchange_name, queue=queue_name)

    print(f"[*] Waiting for messages in exchange '{exchange_name}'. To exit press CTRL+C")

    # Callback to process messages
    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f" [x] Received message: {message}")

        # Emit message to all connected clients
        sio.emit("message", message)

    # Start consuming
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Run the RabbitMQ consumer in a separate thread
def start_rabbitmq_consumer():
    exchange_name = "task_notifications"  # Topic exchange
    routing_key = "user.manager"  # Change as needed
    thread = threading.Thread(target=rabbitmq_consumer, args=(exchange_name, routing_key, 'topic'))
    thread.daemon = True  # Ensure the thread closes with the main program
    thread.start()

# Socket.IO Events
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Main Entry Point
if __name__ == "__main__":
    print("[*] Starting RabbitMQ consumer thread...")
    start_rabbitmq_consumer()

    print("[*] Starting Socket.IO server...")
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
