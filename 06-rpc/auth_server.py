import pika
import os
import time

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RPC_QUEUE_NAME = os.getenv("RPC_QUEUE_NAME", "auth_rpc_queue")

# Mock database with credit limits
USERS_DB = {
    "alice": {"status": "Active", "credit": 500},
    "bob": {"status": "Blocked", "credit": 0},
    "charlie": {"status": "Active", "credit": 50}
}

def validate_transaction(username, amount):
    """Business logic: Check status and credit limit"""
    time.sleep(1.5) # Simulate processing
    user = USERS_DB.get(username.lower())
    
    if not user:
        return f"ERROR: User '{username}' not found."
    
    if user['status'] != "Active":
        return f"REJECTED: User '{username}' account is {user['status']}."
    
    if user['credit'] < amount:
        return f"REJECTED: Insufficient credit. Needs {amount}, has {user['credit']}."
    
    return f"SUCCESS: Transaction of {amount} units approved for {username}."

def on_message(ch, method, props, body):
    # Parsing the request (Expecting "username,amount")
    try:
        request_data = body.decode().split(",")
        username = request_data[0]
        try:
            amount = float(request_data[1])
        except ValueError:
            raise ValueError("Amount must be a number.")
        
        print(f" [.] Validating: {username} requesting {amount}")
        response = validate_transaction(username, amount)
    except Exception as e:
        response = f"INVALID_REQUEST_FORMAT: {str(e)}"

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=response
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RPC_QUEUE_NAME)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RPC_QUEUE_NAME, on_message_callback=on_message)

    print("Auth Server: Awaiting validation requests...")
    channel.start_consuming()

if __name__ == "__main__":
    main()