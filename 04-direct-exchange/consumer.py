import os
import pika
import sys

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME", "direct_logs")

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # Create a temporary exclusive queue
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Read severities from command line arguments
    severities = sys.argv[1:]
    if not severities:
        print("Usage: python3 consumer.py [<severity>]...")
        sys.exit(1)

    # Bind the queue to the exchange for each severity provided
    for severity in severities:
        channel.queue_bind(
            exchange=EXCHANGE_NAME, 
            queue=queue_name, 
            routing_key=severity
        )

    print(f" [*] Waiting for logs: {severities}. Press CTRL+C to exit.")

    def on_message(ch, method, properties, body):
        print(f"[{method.routing_key.upper()}] {body.decode()}")

    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=on_message, 
        auto_ack=True
    )

    try:
        for method_frame, properties, body in channel.consume(queue_name, inactivity_timeout=6):
            if method_frame is None:
                print("[consumer] Idle timeout reached. No more messages. Closing...")
                break
            on_message(channel, method_frame, properties, body)
    except KeyboardInterrupt:
        pass
    finally:
        channel.cancel()
        connection.close()

if __name__ == "__main__":
    main()