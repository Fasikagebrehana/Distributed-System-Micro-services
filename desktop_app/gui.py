import tkinter as tk
from tkinter import messagebox
import pika
import threading
import json

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taskify Desktop App")

        # Task Entry Fields
        tk.Label(root, text="Task Description:").grid(row=0, column=0)
        self.task_desc_entry = tk.Entry(root, width=40)
        self.task_desc_entry.grid(row=0, column=1)

        tk.Label(root, text="Priority:").grid(row=1, column=0)
        self.priority_entry = tk.Entry(root, width=40)
        self.priority_entry.grid(row=1, column=1)

        # Add Task Button
        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=2, column=0, columnspan=2)

        # Task Updates Section
        tk.Label(root, text="Task Updates:").grid(row=3, column=0, columnspan=2)
        self.updates_box = tk.Text(root, height=10, width=50)
        self.updates_box.grid(row=4, column=0, columnspan=2)

        # Start RabbitMQ Consumer Thread
        self.start_consumer_thread()

    def add_task(self):
        task_description = self.task_desc_entry.get()
        priority = self.priority_entry.get()

        if not task_description or not priority:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        task = {
            "description": task_description,
            "priority": priority
        }

        # Publish task to RabbitMQ
        self.publish_to_queue(task)
        messagebox.showinfo("Success", "Task added successfully!")

    def publish_to_queue(self, task):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='task_updates', exchange_type='fanout')
        channel.basic_publish(exchange='task_updates', routing_key='', body=json.dumps(task))
        connection.close()

    def start_consumer_thread(self):
        thread = threading.Thread(target=self.consume_updates, daemon=True)
        thread.start()

    # def consume_updates(self):
    #     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    #     channel = connection.channel()
    #     channel.exchange_declare(exchange='task_notifications', exchange_type='fanout')
    #     result = channel.queue_declare(queue='', exclusive=True)
    #     queue_name = result.method.queue
    #     channel.queue_bind(exchange='task_notifications', queue=queue_name)

    #     def callback(ch, method, properties, body):
    #         message = json.loads(body)
    #         self.updates_box.insert(tk.END, f"New Update: {message}\n")
    #         self.updates_box.see(tk.END)

    #     channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    #     channel.start_consuming()
    def consume_updates(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Use 'topic' since the exchange is already declared as a topic exchange
        channel.exchange_declare(exchange='task_notifications', exchange_type='topic')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
       
        channel.queue_bind(exchange='task_notifications', queue=queue_name, routing_key="#")

        def callback(ch, method, properties, body):
            message = json.loads(body)
            self.updates_box.insert(tk.END, f"New Update: {message}\n")
            self.updates_box.see(tk.END)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()
