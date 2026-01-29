# 06. RPC (Remote Procedure Call) - Auth Service

## Overview

This directory demonstrates the **RPC (Remote Procedure Call)** pattern. This is the most complex pattern in RabbitMQ as it implements a **Request/Response** mechanism over an asynchronous message broker.

In this scenario, we simulate a  **Distributed User Validation Service** . A client (e.g., an E-commerce checkout) requests user verification from a remote Auth Service and waits for a specific approval or rejection response.

## Technology Stack

* **Language:** Python 3.x
* **Message Broker:** RabbitMQ
* **Library:** `pika` (Python RabbitMQ client)

---

## Messaging Features Demonstrated

- **Reply Queue (`reply_to`):** The client specifies a private, temporary queue where the server should send the response.
- **Correlation ID:** A unique identifier used to match a specific response to its corresponding request in a multi-client environment.
- **Data Encapsulation:** Sending complex payloads (Username + Transaction Amount) instead of simple strings.

---

## The Simulation Scenario

- **Client (`checkout_client.py`):** Sends a payload like `Alice,250`. It blocks execution until the server returns an approval or rejection.
- **Server (`auth_server.py`):** Holds a mock database of users and their credit limits. It validates if the user exists, is active, and has enough funds to cover the requested amount.

---

## Execution Example

The server processes the request and returns status messages such as:

- `SUCCESS: Transaction of 200 units approved for Alice.`
- `REJECTED: Insufficient credit. Needs 100, has 50.`
- `ERROR: User 'Stranger' not found.`

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

The automated script will launch the RabbitMQ container, start the Auth Server, and then run three different client requests for different users:

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

### Step 2: Start the RPC Server

```bash
python3 auth_server.py
```

### Step 3: Run the RPC Client

Execute the client and provide a username and a transaction amount as arguments:

```bash
# Format: python3 checkout_client.py <username> <amount>
python3 checkout_client.py Alice 50
```

**Result:** You will see the client waiting for a few seconds (simulating a database lookup) before receiving the personalized response from the server.
