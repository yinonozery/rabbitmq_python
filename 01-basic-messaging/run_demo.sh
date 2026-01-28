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

# 3. Run Scripts
echo "🏁 Running Publisher and Consumer..."
python3 consumer.py &
CONSUMER_PID=$!
sleep 2
python3 publisher.py
echo "✅ Demo finished. Cleaning up..."
wait $CONSUMER_PID

echo "🎉 All done!"