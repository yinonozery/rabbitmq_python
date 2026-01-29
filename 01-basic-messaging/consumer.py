import os
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "")
CONSUMER_PREFETCH_COUNT = int(os.getenv("CONSUMER_PREFETCH_COUNT", "1"))

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

    # fair dispatch: don't give more than 1 unacked msg at a time
    channel.basic_qos(prefetch_count=CONSUMER_PREFETCH_COUNT)

    def on_message(ch, method, properties, body):
        msg = body.decode("utf-8", errors="replace")
        print(f"[consumer] received <- {msg}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

        on_message.count += 1
        if on_message.count >= 10:
            print("[consumer] received 10 messages, stopping...")
            ch.stop_consuming()

    on_message.count = 0

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)

    print("[consumer] waiting for messages. Press CTRL+C to exit.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    finally:
        channel.cancel()
        connection.close()
        print("[consumer] closed")

if __name__ == "__main__":
    main()