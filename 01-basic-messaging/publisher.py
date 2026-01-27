import os
import time
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "")

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=30,
    )

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # ensure queue exists (idempotent)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    for i in range(1, 11):
        msg = f"message No.{i}"
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=msg.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            ),
        )
        print(f"[publisher] sent -> {msg}")
        time.sleep(0.2)

    connection.close()
    print("[publisher] done")

if __name__ == "__main__":
    main()