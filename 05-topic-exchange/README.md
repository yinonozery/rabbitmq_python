# 05. Topic Exchange (Taxi Dispatch System)

## Overview

This directory demonstrates the  **Topic Exchange** , the most flexible routing model in RabbitMQ. Unlike a Direct exchange that requires an exact match, a Topic exchange allows for routing based on **patterns** using wildcards.

In this demo, we simulate a **National Taxi Dispatch System** where ride requests are routed based on their location and service type using a structured routing key: `taxi.<city>.<type>`.

## Technology Stack

* **Language:** Python 3.x
* **Message Broker:** RabbitMQ
* **Library:** `pika` (Python RabbitMQ client)

---

## Messaging Features Demonstrated

* **Topic Exchange:** Routes messages based on wildcard matches between the routing key and the binding pattern.
* **Wildcard `*` (Star):** Replaces exactly one word (e.g., `taxi.tel-aviv.*` matches any service type in Tel Aviv).
* **Wildcard `#` (Hash):** Replaces zero or more words (e.g., `taxi.#` matches every taxi-related message in the system).
* **Pattern-Based Subscriptions:** Multiple consumers can subscribe to different cross-sections of the data flow.

---

## The Simulation Scenario

* **Publisher:** Emits taxi bookings like `taxi.tel-aviv.standard` or `taxi.haifa.premium`.
* **Subscriber 1 (Local Dispatcher):** Listens for `taxi.tel-aviv.*` (All rides in Tel Aviv).
* **Subscriber 2 (Premium Service):** Listens for `taxi.*.premium` (Only Premium rides, regardless of the city).
* **Subscriber 3 (National Monitor):** Listens for `taxi.#` (Every single ride request in the country).

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

The automated script will launch the RabbitMQ container, wait for it to be ready, and open 4 terminals (3 specialized subscribers and 1 publisher):

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

### Step 2: Start Specialized Consumers

* **Terminal 1:** `python3 consumer.py "taxi.tel-aviv.*"`
* **Terminal 2:** `python3 consumer.py "taxi.*.premium"`
* **Terminal 3:** `python3 consumer.py "taxi.#"`

### Step 3: Run the Publisher

In a fourth terminal, send messages with different topic keys:

```bash
python3 publisher.py taxi.tel-aviv.premium "VIP ride in TLV"
python3 publisher.py taxi.haifa.standard "Standard ride in Haifa"
```

**Result:** Observe how a single message can land in one, two, or all three consumer windows depending on how well the topic matches their specific wildcard pattern.
