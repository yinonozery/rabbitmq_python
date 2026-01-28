#!/bin/bash
set -e

export RABBITMQ_HOST="localhost"
export RABBITMQ_USER="guest"
export RABBITMQ_PASS="guest"
export RABBITMQ_EXCHANGE_NAME="logs"

echo "🚀 Starting Fanout (Publish/Subscribe) Demo..."

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

# 3. Start Two Consumers (Subscribers)
# Each will create its own temporary queue
gnome-terminal --title="Subscriber 1" -- bash -c "python3 consumer.py; exec bash" &
gnome-terminal --title="Subscriber 2" -- bash -c "python3 consumer.py; exec bash" &

sleep 3

# 4. Start Publisher to broadcast a message
gnome-terminal --title="Publisher (Emitter)" -- bash -c "
echo '🚀 Broadcasting messages to all subscribers...';
python3 publisher.py '[INFO] Log Entry #1: System Booted';
python3 publisher.py '[INFO] Log Entry #2: User Logged In';
python3 publisher.py '[ERROR] Log Entry #3: Disk Space Low';
python3 publisher.py '[WARNING] Log Entry #4: High Memory Usage';
python3 publisher.py;

exec bash" &

echo "✨ Watch both Subscriber windows. They should receive the EXACT same messages!"