import pika
import uuid
import os
import sys

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RPC_QUEUE_NAME = os.getenv("RPC_QUEUE_NAME", "auth_rpc_queue")

class AuthRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_message,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_message(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()

    # Sends a combined payload of username and amount to the auth service.
    def verify_transaction(self, username, amount):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        # We send a comma-separated string
        request_payload = f"{username},{amount}"

        self.channel.basic_publish(
            exchange='',
            routing_key=RPC_QUEUE_NAME,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request_payload)
        
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == "__main__":
    client = AuthRpcClient()
    
    # Usage: python3 rpc_client.py <username> <amount>
    if len(sys.argv) < 2:
        print("Usage: python3 checkout_client.py <username> <amount>")
        sys.exit(1)
    user, amount = sys.argv[1], sys.argv[2]
    
    print(f" [x] Requesting: {user} wants to spend {amount}")
    response = client.verify_transaction(user, amount)
    print(f" [.] Server Response: {response}")
