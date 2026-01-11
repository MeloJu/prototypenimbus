#!/bin/bash
# Deployment script for Music Generator Company

set -e

echo "🚀 Deploying Music Generator Company..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if Ollama container is running
if docker-compose ps | grep -q "ollama"; then
    echo "📦 Pulling llama2 model in Ollama..."
    docker-compose exec -T ollama ollama pull llama2 || echo "⚠️  Model pull failed, will retry later"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Web interface: http://localhost:5000"
echo "🤖 Ollama API: http://localhost:11434"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
echo ""
