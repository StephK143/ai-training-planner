#!/bin/bash

# Build and start the AI Training Planner with MCP Server
# This script builds all Docker containers and starts the complete application

set -e

echo "🚀 Starting AI Training Planner with MCP Server..."

# Build all services
echo "📦 Building Docker containers..."
docker-compose build --no-cache

# Start all services
echo "🔄 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🏥 Checking service health..."

echo "Frontend health check..."
if curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ Frontend is healthy (port 3000)"
else
    echo "❌ Frontend health check failed"
fi

echo "Backend health check..."
if curl -s http://localhost:5002/api/health > /dev/null; then
    echo "✅ Backend is healthy (port 5002)"
else
    echo "❌ Backend health check failed"
fi

echo "MCP Server health check..."
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ MCP Server is healthy (port 8080)"
else
    echo "❌ MCP Server health check failed"
fi

echo "Ollama health check..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is healthy (port 11434)"
else
    echo "❌ Ollama health check failed"
fi

echo "
🎉 AI Training Planner is running!

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5002
- MCP Server: http://localhost:8080
- Ollama: http://localhost:11434

To view logs: docker-compose logs -f [service-name]
To stop: docker-compose down
"
