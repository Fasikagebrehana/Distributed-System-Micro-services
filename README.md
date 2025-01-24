# Taskify: Distributed Task Management System

Taskify is a distributed task management system designed to work across multiple platforms, including desktop and mobile. The project incorporates advanced socket-based communication using RabbitMQ for efficient messaging, along with microservices for backend functionality.

This project has been developed to meet the requirements of a distributed system application as outlined in the instructor's instructions:

- **Support for multiple platforms**: Desktop and Android.
- **Distributed architecture**: Incorporates message-oriented communication using RabbitMQ.
- **Advanced socket features**: Implements publish-subscribe features for selective message multicasting.
- **Modular design**: Employs microservices architecture for scalability and maintainability.

## Project Structure

### Root Directory
- `db.sqlite3`: SQLite database for backend storage.
- `manage.py`: Script for managing the backend services.

### Main Components

#### 1. **Client**
- **Desktop App (`desktop_app`)**:
  - Contains GUI and utility scripts for the desktop application.
  - Implements task submission and status retrieval features.
- **Socket Client (`socket_client.py`)**:
  - Manages communication with RabbitMQ for sending and receiving messages.
- **Virtual Environment (`venv`)**:
  - Contains dependencies for the desktop client.

#### 2. **Mobile App (`mobile_app`)**
- Built with Flutter, supporting Android and cross-platform development.
  - Contains the Dart source code, platform-specific directories, and configurations.
  - Allows users to manage tasks and view notifications.

#### 3. **Backend Services**
- **Mobile Backend (`mobile_backend`)**:
  - Serves as the main entry point for backend APIs.
  - Manages communication between the frontend and microservices.
- **Notification Service (`notification_service`)**:
  - Handles RabbitMQ message consumption and socket communication.
  - Sends notifications to clients based on updates.
- **Task Service (`task_service`)**:
  - Manages task-related operations such as creation, updating, and retrieval.
- **User Service (`user_service`)**:
  - Handles user-related operations, including authentication and profile management.
- **Virtual Environment (`venv`)**:
  - Contains dependencies for backend services.

## Features

1. **Advanced Socket Communication**:
   - Implements Publish-Subscribe and Topic Exchange models using RabbitMQ.
   - Supports selective message multicasting for efficient communication.

2. **Cross-Platform Support**:
   - Desktop application built with Python.
   - Mobile application built with Flutter, supporting Android.

3. **Microservices Architecture**:
   - Separate services for tasks, notifications, and users.
   - Modular design for scalability and maintainability.

## Setup Instructions

### Prerequisites
- Python 3.8+
- RabbitMQ
- Flutter SDK

### Backend Setup
1. Clone the repository.
2. Navigate to the backend directory:
   ```bash
   cd mobile_backend
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python app.py
   ```

### RabbitMQ Setup
1. Install RabbitMQ on your system.
2. Start RabbitMQ service:
   ```bash
   rabbitmq-server
   ```
3. Configure exchanges and queues for Publish-Subscribe and Topic models.

### Desktop App Setup
1. Navigate to the desktop client directory:
   ```bash
   cd client/desktop_app
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Run the desktop app:
   ```bash
   python gui.py
   ```

### Mobile App Setup
1. Navigate to the mobile app directory:
   ```bash
   cd client/mobile_app
   ```
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Run the app on your desired platform:
   ```bash
   flutter run
   ```

## Socket Communication

- **Socket Client (`socket_client.py`)**:
  - Manages RabbitMQ connections and message handling for the client.
  - Implements Publish-Subscribe for selective messaging.

- **Socket Server (`socket_server.py`)**:
  - Handles RabbitMQ connections and message routing on the backend.
  - Routes messages to appropriate services (tasks, notifications, users).

## Testing

1. **Integration Testing**:
   - Verify end-to-end communication between the desktop app, mobile app, and backend.

2. **Unit Testing**:
   - Run tests for individual components:
     ```bash
     python manage.py test
     ```

## Future Improvements

- Add robust error handling and logging across all components.
- Deploy RabbitMQ and backend services to cloud platforms (e.g., AWS, Heroku).
- Optimize mobile app for performance on low-end devices.

---

This README provides a comprehensive overview of the Taskify system, its structure, and how to set up and run the project. For further details or troubleshooting, please refer to the respective service documentation or contact the project maintainers.

![image](https://github.com/user-attachments/assets/a41d3a0e-82ba-45a1-9296-4de1f845e88f)
![image](https://github.com/user-attachments/assets/4caf9641-5bdb-4f7e-ad8c-e4db35e918b5)

![image](https://github.com/user-attachments/assets/a488d138-e359-4d6f-ba84-86e01de6574b)
