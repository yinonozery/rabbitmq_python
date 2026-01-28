import os
import time
import pika
import random

# Load configuration from environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "ABC")
CONSUMER_PREFETCH_COUNT = int(os.getenv("CONSUMER_PREFETCH_COUNT", "1"))

def main():
    # Setup connection credentials and parameters
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

    # Ensure queue exists and is durable (survives broker restart)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Fair dispatch: tells RabbitMQ not to give more than one message to a worker at a time
    channel.basic_qos(prefetch_count=CONSUMER_PREFETCH_COUNT)

    def on_message(ch, method, properties, body):
        """Processes the received message with a simulated random delay."""
        msg = body.decode("utf-8", errors="replace")
        
        # Simulate variable task complexity
        processing_time = random.randint(1, 5)
        
        print(f"[consumer] received <- {msg} (Processing time: {processing_time}s)")

        # Block the execution to simulate heavy work
        time.sleep(processing_time) 

        # Manually acknowledge the message after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[consumer] finished -> {msg}")

    print(f"[consumer] Waiting for messages in '{QUEUE_NAME}'.")
    print("[consumer] Auto-shutdown: 6 seconds of inactivity.")

    try:
        # Using a generator to consume messages with an inactivity timeout
        # This allows the consumer to exit gracefully if the queue is empty
        for method_frame, properties, body in channel.consume(QUEUE_NAME, inactivity_timeout=6):
            if method_frame is None:
                print("[consumer] Idle timeout reached. No more messages. Closing...")
                break
            
            # Manually trigger the processing function
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
