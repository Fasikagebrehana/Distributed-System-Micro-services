from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the exchange (topic type for fine-grained routing)
exchange_name = 'task_notifications'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

# Declare the queue (to store messages for consuming)
queue_name = 'taskify_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Bind the queue to the exchange with a routing key
binding_key = 'task.#'  # Listens to all messages starting with 'task.'
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    message = data.get('message', '')
    routing_key = data.get('routing_key', '')

    try:
        print(f"Publishing message: {message} to routing key: {routing_key}")
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
        return jsonify({"status": "Message published successfully!"}), 200
    except Exception as e:
        print(f"Error publishing message: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/consume', methods=['GET'])
def consume():
    try:
        method_frame, header_frame, body = channel.basic_get("taskify_queue", auto_ack=False)
        if method_frame:
            message = body.decode()
            print(f"Consumed message: {message}")  # Log the consumed message
            channel.basic_ack(method_frame.delivery_tag)
            return jsonify({"messages": [message]}), 200
        else:
            return jsonify({"messages": []}), 200
    except Exception as e:
        print(f"Error in /consume: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)