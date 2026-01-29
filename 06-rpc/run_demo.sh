#!/bin/bash
set -e

echo "🚀 Starting RPC Demo..."

# Environment Settings
export RABBITMQ_HOST="localhost"
export RPC_QUEUE_NAME="auth_rpc_queue"

# 1. Check for Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker daemon is not running. Please start Docker and try again."
    exit 1
fi

# 2. Start RabbitMQ Container
echo "📦 Starting RabbitMQ container..."
docker rm -f rabbitmq 2>/dev/null || true
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
sleep 5
echo "⏳ Waiting for RabbitMQ to be fully operational..."
set +e 
while true; do

  docker exec rabbitmq rabbitmqctl status > /dev/null 2>&1

  if [ $? -eq 0 ]; then
    echo "✅ RabbitMQ is up and running!"
    break
  fi

  echo "Still starting... (checking every 3s)"
  sleep 3
done
set -e

# 2. Start Auth Server
gnome-terminal --title="Auth Service (Server)" -- bash -c "python3 auth_server.py; exec bash" &

sleep 5

# 3. Run Clients for different users
# Alice should pass (has 500)
gnome-terminal --title="Alice - Approved" -- bash -c "python3 checkout_client.py Alice 200; exec bash" &

# Charlie should fail (has only 50)
gnome-terminal --title="Charlie - Low Credit" -- bash -c "python3 checkout_client.py Charlie 100; exec bash" &

# Bob should fail (Blocked)
gnome-terminal --title="Bob - Blocked" -- bash -c "python3 checkout_client.py Bob 10; exec bash" &

# Unknown user should fail (not in DB)
gnome-terminal --title="Unknown - Blocked" -- bash -c "python3 checkout_client.py UnknownUser 10; exec bash" &

echo "✨ Multi-user validation demo started!"
