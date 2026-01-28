
# 3. Publish/Subscribe (Fanout Exchange)

## Overview

This directory demonstrates the **Publish/Subscribe** pattern using a  **Fanout Exchange** . Unlike the Work Queue pattern where a message is delivered to exactly one worker, the Fanout exchange **broadcasts** every message to **all** available consumers simultaneously.

This is ideal for systems that need to notify multiple independent services about the same event (e.g., a "User Created" event that triggers both an Email Service and a Logging Service).

## Technology Stack

* **Language:** Python 3.x
* **Message Broker:** RabbitMQ
* **Library:** `pika` (Python RabbitMQ client)

---

## Messaging Features Demonstrated

* **Fanout Exchange:** A broadcast mechanism that ignores routing keys and delivers messages to all bound queues.
* **Temporary Queues:** Consumers create fresh, empty, and random-named queues upon connection (`exclusive=True`).
* **Bindings:** The process of linking an exchange to a queue so messages know where to flow.
* **Auto-Shutdown:** Consumers use an `inactivity_timeout` to exit gracefully after 6 seconds of silence.

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

### Running the Demo

### *Automated*

The automated script will launch two worker terminals and one publisher terminal. It also manages the RabbitMQ Docker container:

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

## Step 2: Start Multiple Subscribers

Open **TWO** separate terminals and run the consumer in each:

```bash
python3 consumer.py
```

### Step 3: Run the Publisher

In a third terminal, send a broadcast message:

```bash
python3 publisher.py "[INFO]: Example log message"
```

**Result:** You will see the message appearing in **both** subscriber terminals at the same time. If you stop one subscriber and send another message, only the active one will receive it.
