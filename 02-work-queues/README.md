
# 02. Work Queues (Task Distribution)

## Overview

This directory demonstrates the **Work Queue** pattern, used to distribute heavy tasks among multiple workers. Instead of sending a message to a single consumer, this pattern enables **Scalability** and **Parallel** Processing.

By running multiple consumers, RabbitMQ balances the load, ensuring that tasks are handled efficiently by whichever worker is available.

## Technology Stack

* **Language:** Python 3.x
* **Message Broker:** RabbitMQ
* **Library:** `pika` (Python RabbitMQ client)

---

## Messaging Features Demonstrated

* **Fair Dispatch (`prefetch_count=1`):** Ensures a worker only receives one message at a time, preventing a single worker from being overwhelmed while others are idle.
* **Message Acknowledgment (ACK):** The worker sends an acknowledgment only **after** the task is finished, ensuring no messages are lost if a worker crashes.
* **Queue Durability & Persistence:** Both the queue and messages are marked to survive RabbitMQ restarts.
* **Auto-Shutdown:** The consumers are configured with an `inactivity_timeout` to gracefully exit after 6 seconds of idle time.

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


### Step 2: Start the Consumer

Open **TWO** separate terminals and run the consumer in each:

```bash
python3 consumer.py
```

### Step 3: Run the Publisher

Execute the publisher to send a batch of 10 tasks:

```bash
python3 publisher.py
```

**Result:** You will observe the tasks being distributed between the two workers. Since each task has a  **random processing time (1-5s)** , you will see the "Fair Dispatch" in action - the faster worker will process more messages than the slower one. Both workers will automatically close after the queue is empty.
