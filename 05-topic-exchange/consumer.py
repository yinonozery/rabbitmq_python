import os
import pika
import sys

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME", "taxi_topics")

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

    # Temporary exclusive queue
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Binding keys (patterns) from CLI
    binding_keys = sys.argv[1:]
    if not binding_keys:
        print("Usage: python3 consumer.py [binding_key]...")
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange=EXCHANGE_NAME, 
            queue=queue_name, 
            routing_key=binding_key
        )

    print(f" [*] Waiting for taxi orders matching: {binding_keys}")

    def on_message(ch, method, properties, body):
        print(f" [received] {method.routing_key} -> {body.decode()}")

    # Using our smart timeout generator for auto-shutdown
    try:
        for method_frame, properties, body in channel.consume(queue_name, inactivity_timeout=6):
            if method_frame is None:
                print("[timeout] No more taxi orders. Closing...")
                break
            on_message(channel, method_frame, properties, body)
    except KeyboardInterrupt:
        pass
    finally:
        channel.cancel()
        connection.close()

if __name__ == "__main__":
    main()
