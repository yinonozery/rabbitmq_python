# 01. Basic Messaging (Simple Queue)

## Overview
This directory contains the foundational implementation of a Point-to-Point (P2P) messaging pattern. It demonstrates how a **Publisher** sends a batch of 10 messages to a specific queue and how a **Consumer** retrieves and processes them.

This example highlights the decoupling of systems: the publisher doesn't need to know if the consumer is active when the messages are sent.

## Technology Stack
- **Language:** Python 3.x
- **Message Broker:** RabbitMQ
- **Library:** `pika` (Python RabbitMQ client)

---

## Messaging Features Demonstrated
- **Queue Durability:** The `ABC` queue is marked as durable to survive broker restarts.
- **Message Persistence:** Messages are marked as persistent to prevent data loss.
- **Manual Acknowledgments (ACK):** The consumer explicitly tells RabbitMQ when a message is processed.
- **Fair Dispatch:** Uses `prefetch_count=1` to ensure the consumer only receives one message at a time.

---

## Setup & Prerequisites

### 1. Install Dependencies
```bash
pip install pika
```

### 2. Environment Configuration
The project is pre-configured with default values. You can find a template in `.env.example.`
* Note: If you use the automated script (`run_demo.sh`), it will handle all environment variables for you automatically.

---

### Running the Demo
### *Automated*
The easiest way to run the project on Linux/macOS is using the provided shell script. It handles Docker setup, environment variables, and execution in one command:
```bash
chmod +x run_demo.sh
./run_demo.sh
```

***

### *Manual*
If you prefer to run the components manually, follow these steps:
### Step 1: Run RabbitMQ

**Option A: Using Docker (Recommended)**
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

**Option B: Local Installation (No Docker)**

If you prefer not to use Docker, follow the official installation guides:
* Windows: Install via Chocolatey (`choco install rabbitmq`) or the official installer.
* macOS: Install via Homebrew (`brew install rabbitmq`).
* Linux (Ubuntu/Debian): `sudo apt-get install rabbitmq-server`.
Once installed, ensure the service is running: `sudo service rabbitmq-server start`.

### Step 2: Start the Consumer
The consumer will wait for messages to arrive in the `ABC` queue.
```bash
python3 consumer.py
```

### Step 3: Run the Publisher
The publisher will send 10 messages to the queue and then exit.
```bash
python3 publisher.py
```

**Result:** You will see the consumer receive, process, and acknowledge each of the 10 messages in real-time.