import pika
import json
from django.http import JsonResponse

def create_task(request):
    if request.method == 'POST':
        # Example task data (replace with real data from request.POST)
        task_data = {
            "task_id": 1,
            "task_name": "Sample Task",
            "assigned_to": "User123",
        }

        # RabbitMQ connection
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        
        # Declare the queue
        channel.queue_declare(queue='task_queue')

        # Publish JSON-serialized task data
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(task_data)  # Convert dictionary to JSON string
        )
        connection.close()

        return JsonResponse({"message": "Task created and published successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=400)
