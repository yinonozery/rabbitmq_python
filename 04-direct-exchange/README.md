# 4. Routing (Direct Exchange)

## Overview

This directory demonstrates the **Routing** pattern using a  **Direct Exchange** . Unlike the Fanout exchange which broadcasts to everyone, a Direct exchange delivers messages only to queues that are bound with a matching  **Routing Key** .

This pattern is essential for selective message delivery, such as separating log messages by their severity (info, warning, error).

## Technology Stack

* **Language:** Python 3.x
* **Message Broker:** RabbitMQ
* **Library:** `pika` (Python RabbitMQ client)

---

## Messaging Features Demonstrated

* **Direct Exchange:** Routes messages to queues based on an exact match between the message's routing key and the queue's binding key.
* **Multiple Bindings:** A single queue can be bound to an exchange with multiple routing keys (e.g., a consumer listening for both 'info' and 'warning').
* **Selective Consumption:** Consumers decide exactly which "types" of messages they want to receive.
* **Auto-Shutdown:** Consumers use an `inactivity_timeout` of 6 seconds to exit once the work is done.

---

## Setup & Prerequisites

### 1. Install Dependencies

```bash
pip install pika
```

### 2. Environment Configuration

The project is pre-configured with default values within the scripts.

* Note: If you use the automated script (`run_demo.sh`), it will handle all environment variables and Docker setup for you automatically.

---

## Running the Demo

### *Automated*

The automated script launches two specific subscribers and a publisher that sends logs with different severities:

* **Subscriber 1:** **Listens for** `info` **and** `warning` **messages.**
* **Subscriber 2:** **Listens only for** `error` **messages.**

```bash
chmod +x run_demo.sh
./run_demo.sh
```

---

### *Manual*

If you prefer to run the components manually, open multiple terminal tabs:

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

### Step 2: Start Selective Consumers

* **Terminal 1 (General):** `python3 consumer.py info warning`
* **Terminal 2 (Errors):** `python3 consumer.py error`

### Step 3: Run the Publisher

In a third terminal, send messages with different keys:

```bash
python3 publisher.py error "System crash detected!"
python3 publisher.py info "System heartbeat is normal."
```

**Result:** You will see that the "General" terminal receives the info log, while the "Errors" terminal receives only the error log. This proves the **Selective Routing** capabilities of RabbitMQ.
