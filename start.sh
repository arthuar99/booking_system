#!/bin/bash

# Booking Platform Startup Script

echo " Starting Booking Platform..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo " Docker daemon is not running!"
    echo ""
    echo "Please ensure Docker Desktop is running and the daemon is ready."
    echo "You can check by running: docker info"
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Build and start containers
echo "📦 Building and starting containers..."
docker compose up -d --build

if [ $? -eq 0 ]; then
    echo ""
    echo " Booking Platform is starting!"
    echo ""
    echo "📊 Container status:"
    docker compose ps
    echo ""
    echo "🌐 Application will be available at: http://localhost:8000"
    echo ""
    echo "📝 Useful commands:"
    echo "  - View logs:        docker compose logs -f"
    echo "  - Stop containers:  docker compose down"
    echo "  - Restart:          docker compose restart"
else
    echo ""
    echo " Failed to start containers"
    exit 1
fi

