![img](https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/RabbitMQ_logo.svg/500px-RabbitMQ_logo.svg.png "RabbitMQ")

# RabbitMQ Messaging Patterns with Python

A comprehensive, hands-on guide to mastering RabbitMQ using Python and the `pika` library. This repository contains a step-by-step progression through all major messaging patterns, from simple queues to complex RPC systems.

## 🚀 Overview

Each directory represents a core messaging pattern, complete with its own automated Docker setup, implementation scripts, and detailed documentation.

### 📚 Learning Path

1. **[01-basic-messaging](./01-basic-messaging)**: Introduction to Point-to-Point (P2P) messaging.
2. **[02-work-queues](./02-work-queues)**: Distributing heavy tasks among multiple workers using Fair Dispatch.
3. **[03-fanout-exchange](./03-fanout-exchange)**: Broadcasting messages to multiple consumers using **Fanout Exchange**.
4. **[04-direct-exchange](./04-direct-exchange)**: Selective message delivery based on severity levels using **Direct Exchange**.
5. **[05-topic-exchange](./05-topic-exchange)**: Advanced pattern-based routing using Wildcards (`*`, `#`) and **Topic Exchange**.
6. **[06-rpc](./06-rpc)**: Implementing Request/Reply communication (Remote Procedure Call).

---

## 🛠 Tech Stack

- **Broker:** RabbitMQ (via Docker)
- **Language:** Python 3.x
- **Client Library:** [Pika](https://pika.readthedocs.io)
- **Automation:** Bash scripting for multi-terminal orchestration.

---

## 🏁 Quick Start

Every pattern includes a `run_demo.sh` script that automates the entire process:

1. Starts the RabbitMQ container.
2. Waits for the broker to be healthy.
3. Launches multiple terminals for Workers and Publishers.

```bash
# Example: Running the Routing pattern
cd 04-direct-exchange
chmod +x run_demo.sh
./run_demo.sh
```

---

## 📖 Key Concepts Covered

* **Reliability:**Message persistence and manual acknowledgments (ACKs).
* **Scalability:** Load balancing between multiple consumers.
* **Flexibility:** Dynamic routing using various Exchange types.
* **Automation:** Health-checking the broker before execution.

---

*Created by Yinon Ozery - Feel free to explore and use this as a reference for your own distributed systems*
