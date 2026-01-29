import os
import pika
import sys

# Configuration
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

    # Declare a 'topic' exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

    # Usage: python3 publisher.py taxi.tel-aviv.premium "New ride request"
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <routing_key> <message>")
    routing_key = sys.argv[1] if len(sys.argv) > 1 else 'taxi.anonymous.standard'
    message = ' '.join(sys.argv[2:]) or "New taxi booking request"

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message
    )

    print(f"Sent '{routing_key}':'{message}'")
    connection.close()

if __name__ == "__main__":
    main()
