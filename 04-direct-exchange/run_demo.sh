#!/bin/bash
set -e

# Environment Settings
export RABBITMQ_HOST="localhost"
export RABBITMQ_USER="guest"
export RABBITMQ_PASS="guest"
export RABBITMQ_EXCHANGE_NAME="direct_logs"

echo "🚀 Starting Direct Exchange (Routing) Demo..."

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

# 3. Start Selective Consumers
echo "🏁 Opening terminals for Selective Workers..."

# Subscriber 1: Listens for 'info' and 'warning'
gnome-terminal --title="Info/Warning - Subscriber 1" -- bash -c "python3 consumer.py info warning; exec bash" &

# Subscriber 2: Listens ONLY for 'error'
gnome-terminal --title="Error - Subscriber 2" -- bash -c "python3 consumer.py error; exec bash" &

sleep 3

# 4. Start Publisher and send messages with different severities
echo "🚀 Triggering the Publisher..."
gnome-terminal --title="Publisher" -- bash -c "
echo '🚀 Sending logs with different routing keys...';
python3 publisher.py error 'Database connection failed!';
python3 publisher.py info 'User logged in successfully';
python3 publisher.py warning 'Memory usage at 85%';
echo '✅ Tasks sent. Check the subscriber windows to see selective routing.';
exec bash" &

echo "✨ Demo is active! Notice how Subscriber 2 ignores 'info' and 'warning' messages."