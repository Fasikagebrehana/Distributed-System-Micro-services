import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected to the Socket.IO server!")

@sio.event
def disconnect():
    print("Disconnected from the Socket.IO server!")

@sio.on("task_notification")
def handle_notification(data):
    print("Received notification:", data)

sio.connect("http://localhost:5000")

sio.wait()
