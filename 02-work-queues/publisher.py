import os
import time
import pika

# Load configuration from environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "ABC")

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

    # Declare the queue (idempotent: only creates if it doesn't exist)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Publish 10 sample tasks to the queue
    for i in range(1, 11):
        msg = f"Task No.{i}"
            
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=msg.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent (saved to disk)
            ),
        )
        print(f"[publisher] sent -> {msg}")
        
        # Short delay between sends to demonstrate sequential publishing
        time.sleep(0.1)

    # Close the connection once finished
    connection.close()
    print("[publisher] all tasks sent successfully. Connection closed.")

if __name__ == "__main__":
    main()
