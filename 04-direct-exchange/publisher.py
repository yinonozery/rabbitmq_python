import os
import pika
import sys

# Load configuration
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

    # Define a 'direct' exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

    # Get severity and message from command line
    # Usage: python3 publisher.py [<severity>] [message]
    severity = sys.argv[1] if len(sys.argv) > 1 else '[severity_example]'
    message = ' '.join(sys.argv[2:]) or "Example log message"

    # Publish with specific routing key
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=severity,
        body=message
    )

    print(f"Sent [{severity.upper()}] {message}")
    connection.close()

if __name__ == "__main__":
    main()