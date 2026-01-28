#!/bin/bash
set -e

export RABBITMQ_HOST="localhost"
export RABBITMQ_PORT="5672"
export RABBITMQ_USER="guest"
export RABBITMQ_PASS="guest"
export RABBITMQ_QUEUE_NAME="ABC"
export CONSUMER_PREFETCH_COUNT="1"

echo "🚀 Starting RabbitMQ Demo Setup..."

# 1. Check for Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker daemon is not running. Please start Docker and try again."
    exit 1
fi

# 2. Start RabbitMQ Container
echo "📦 Starting RabbitMQ container..."
docker rm -f rabbitmq 2>/dev/null || true
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
echo "⏳ Waiting for RabbitMQ to start (15s)..."
sleep 15

# 3. Open Terminals for Workers and Publisher
echo "🏁 Opening terminals for Workers and Publisher..."

# Worker 1
gnome-terminal --title="Worker 1" -- bash -c "python3 consumer.py; exec bash" &

# Worker 2
gnome-terminal --title="Worker 2" -- bash -c "python3 consumer.py; exec bash" &

# Publisher
gnome-terminal --title="Publisher (Running...)" -- bash -c "

echo '🚀 Sending 10 tasks now...';
python3 publisher.py; 
echo '✅ All tasks sent. This terminal will stay open for manual runs.';
exec bash" &

echo "✨ Demo is running! Watch the Worker terminals to see the random processing times."
