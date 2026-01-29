#!/bin/bash
set -e

# Environment Settings
export RABBITMQ_HOST="localhost"
export RABBITMQ_USER="guest"
export RABBITMQ_PASS="guest"
export RABBITMQ_EXCHANGE_NAME="taxi_topics"

echo "🚀 Starting Topic Exchange (Routing) Demo..."

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

# 3. Start Topic-Based Consumers
echo "🏁 Opening terminals for Topic-Based Workers..."

# Subscriber 1: Tel Aviv Expert (All taxi types in Tel Aviv)
gnome-terminal --title="Tel Aviv Dispatcher" -- bash -c "python3 consumer.py 'taxi.tel-aviv.*'; exec bash" &

# Subscriber 2: Premium Hunter (Premium taxis in ANY city)
gnome-terminal --title="Premium Hunter" -- bash -c "python3 consumer.py 'taxi.*.premium'; exec bash" &

# Subscriber 3: Big Brother (Monitor EVERYTHING under taxi)
gnome-terminal --title="National Monitor" -- bash -c "python3 consumer.py 'taxi.#'; exec bash" &

sleep 5

# 4. Start Publisher and send messages with different topics
echo "🚀 Triggering the Taxi Dispatcher..."
gnome-terminal --title="Taxi Dispatcher" -- bash -c "
python3 publisher.py taxi.tel-aviv.standard 'Standard ride in TLV';
python3 publisher.py taxi.tel-aviv.premium 'VIP ride in TLV';
python3 publisher.py taxi.haifa.premium 'VIP ride in Haifa';
python3 publisher.py taxi.jerusalem.standard 'Standard ride in Jerusalem';
exec bash" &

echo "✨ Demo is active! Observe how messages are routed based on topics to different subscribers."