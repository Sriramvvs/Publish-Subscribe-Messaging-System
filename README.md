# 📬 Publish-Subscribe Messaging System

This project is a simplified simulation of a real-world publish-subscribe (Pub/Sub) messaging system built using Python. It mimics how modern systems handle push notifications, topic-based subscriptions, and message routing across multiple services.

## 🔧 Project Structure

- broker.py # Message broker logic
- subscriber.py # Subscriber-side GUI (Tkinter)
- publisher.py # Publisher-side GUI (Flask)
- notification.py # Handles email delivery via SMTP
- user_login.py # Manages user login and topic subscriptions
- topic_server.py # Central topic registry and broker mapping
- register.py # Registration logic for new users


## 📢 Overview

This system is designed to show how messages can be routed from publishers to subscribers via brokers and topic-based routing, using GUI and backend modules.

### 🧠 Key Components

- **Topic Server (`topic_server.py`)**  
  Acts as a central registry to assign topics to brokers and keep track of broker-topic mappings.

- **Broker (`broker.py`)**  
  The intermediary that receives messages from publishers, checks for topic subscriptions, and forwards messages to the notification module.

- **Notification Server (`notification.py`)**  
  Sends messages to subscribers via email using SMTP. App password support in Gmail is used for secure delivery.

- **User Login Server (`user_login.py`, `register.py`)**  
  Handles user sign-in, registration, and subscription tracking using SQLite.

- **Subscriber GUI (`subscriber.py`)**  
  Built with Tkinter, this app allows users to log in, subscribe to topics, and receive messages.

- **Publisher GUI (`publisher.py`)**  
  A Flask-based UI where publishers can enter a topic and message, which is then routed to relevant subscribers.

## 💡 Features

- Topic-based message delivery  
- GUI-based user interaction (Publisher & Subscriber)  
- SQLite database for user and topic data  
- Email-based notifications with secure SMTP setup  
- Modular architecture (can extend to support multiple brokers or advanced routing)

## 📦 Technologies Used

- Python 3.x  
- Flask (for publisher UI)  
- Tkinter (for subscriber UI)  
- SQLite  
- smtplib (for sending emails)

## 🛠️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pub-sub-system.git
   cd pub-sub-system
2. Start each component in separate terminals:
    ```bash
    python topic_server.py  
    python broker.py  
    python notification.py  
    python user_login.py  
    python subscriber.py  
    python publisher.py  


## 👨‍💻 Author Contributions

This project was built by a team of three members, with tasks equally distributed to ensure collaborative development:

Venkata Sai Sriram Valluri focused on the implementation of the Topic Server and User Login modules, including subscription management and data persistence.

Rumana Taj Shaik designed and implemented the Notification Server and Broker logic, ensuring correct message routing and delivery.

Snigdha Setty Chandaluri worked on the Publisher Flask UI and Subscriber Tkinter App, building user-facing interfaces and integrating backend APIs.

All members participated in debugging, testing, and documentation.
