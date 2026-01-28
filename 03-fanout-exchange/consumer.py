import os
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME", "logs")

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the same exchange to ensure it exists
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

    # Create a temporary, random queue for this specific consumer
    # exclusive=True means the queue will be deleted when the connection is closed
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the temporary queue to the Fanout exchange
    # This creates the link: Exchange -> Queue
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

    print(f" [*] Waiting for logs in temporary queue: {queue_name}. To exit press CTRL+C")

    def on_message(ch, method, properties, body):
        """Callback function to handle incoming broadcast messages."""
        print(f" [x] Received log: {body.decode()}")

    # In Fanout, usually we use auto_ack=True because logs are often non-critical
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=on_message, 
        auto_ack=True
    )
    
    print(f" [*] Waiting for logs. Will exit after 6s of inactivity.")
    
    try:
        for method_frame, properties, body in channel.consume(queue_name, inactivity_timeout=6):
            if method_frame is None:
                print("[consumer] Idle timeout reached. No more messages. Closing...")
                break
            on_message(channel, method_frame, properties, body)
    except KeyboardInterrupt:
        print("[consumer] Manual stop triggered by user (Ctrl+C).")
    finally:
        # Clean up: cancel the consumer and close the connection safely
        channel.cancel()
        connection.close()
        print("[consumer] connection closed.")

if __name__ == "__main__":
    main()
