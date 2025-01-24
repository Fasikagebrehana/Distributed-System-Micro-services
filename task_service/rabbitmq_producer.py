import pika
import json

# Create Task (Task-specific logic)
def create_task(task_id, task_status):
    # Prepare exchange and routing key
    exchange_name = "task_notifications"
    routing_key = "task.create"
    message = {"task_id": task_id, "status": task_status}
    
    # Publish the task creation event
    try:
        publish_to_topic_exchange(exchange_name, routing_key, message)
        print(f"Task creation event published: {message}")
    except Exception as e:
        print(f"Failed to publish task creation event: {e}")

# Fanout Exchange
def publish_to_fanout_exchange(exchange_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    channel.basic_publish(exchange=exchange_name, routing_key='', body=json.dumps(message))
    print(f"Message broadcasted to fanout exchange '{exchange_name}': {message}")
    connection.close()

# Topic Exchange
def publish_to_topic_exchange(exchange_name, routing_key, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(message))
    print(f"Message sent to topic exchange '{exchange_name}' with routing key '{routing_key}': {message}")
    connection.close()

# Example usage
if __name__ == "__main__":
    # Example: Broadcast message to all consumers
    publish_to_fanout_exchange('task_updates', {'system': 'update', 'message': 'All systems operational'})

    # Example: Send specific task notifications
    publish_to_topic_exchange('task_notifications', 'user.manager', {'task_id': 1, 'status': 'completed'})
    publish_to_topic_exchange('task_notifications', 'user.worker', {'task_id': 2, 'status': 'in_progress'})

    # Example: Create a task and publish the event
    create_task(3, "pending")
