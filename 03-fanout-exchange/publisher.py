import os
import pika
import sys

# Load configuration from environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME", "logs")

def main():
    # Setup connection
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    # Declare a 'fanout' exchange
    # This type broadcasts every message it receives to all the queues it knows
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

    # Read message from command line arguments or use default
    message = ' '.join(sys.argv[1:]) or "[INFO]: Example log message"

    # Publish the message to the exchange
    # routing_key is empty because fanout ignores it
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key='',
        body=message
    )

    print(f" [x] Sent '{message}' to Fanout Exchange: {EXCHANGE_NAME}")

    connection.close()

if __name__ == "__main__":
    main()
