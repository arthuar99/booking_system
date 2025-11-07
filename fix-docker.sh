#!/bin/bash

# Docker Troubleshooting Script for Booking Platform

echo "🔧 Docker Troubleshooting Script"
echo "=================================="
echo ""

# Function to check Docker status
check_docker() {
    if docker info > /dev/null 2>&1; then
        echo "✅ Docker daemon is running!"
        return 0
    else
        echo "❌ Docker daemon is NOT running"
        return 1
    fi
}

# Check if Docker Desktop app is running
echo "1. Checking Docker Desktop application..."
if pgrep -f "Docker.app" > /dev/null; then
    echo "   ✅ Docker Desktop app is running"
else
    echo "   ❌ Docker Desktop app is NOT running"
    echo ""
    echo "   → Please open Docker Desktop from Applications"
    echo "   → Or run: open -a Docker"
    exit 1
fi

# Check Docker daemon
echo ""
echo "2. Checking Docker daemon..."
if check_docker; then
    echo ""
    echo "🎉 Docker is ready! You can now run:"
    echo "   ./start.sh"
    echo "   or"
    echo "   docker compose up -d --build"
    exit 0
fi

# Docker Desktop is running but daemon isn't ready
echo ""
echo "3. Docker Desktop is running but daemon is not ready."
echo ""
echo "   This usually means:"
echo "   - Docker Desktop is still starting up (wait 30-60 seconds)"
echo "   - Docker daemon has an I/O error (needs reset)"
echo ""

# Check for socket file
echo "4. Checking Docker socket..."
if [ -S ~/.docker/run/docker.sock ]; then
    echo "   ✅ Docker socket exists"
else
    echo "   ❌ Docker socket not found at ~/.docker/run/docker.sock"
fi

echo ""
echo "5. Recommended fixes:"
echo ""
echo "   Option A: Wait and retry (if Docker is still starting)"
echo "   → Wait 30-60 seconds, then run this script again"
echo ""
echo "   Option B: Reset Docker Desktop (if I/O errors persist)"
echo "   → Open Docker Desktop"
echo "   → Click Settings (gear icon)"
echo "   → Go to 'Troubleshoot'"
echo "   → Click 'Reset to factory defaults' or 'Clean / Purge data'"
echo "   → Wait for Docker to restart"
echo ""
echo "   Option C: Restart Docker Desktop"
echo "   → Right-click Docker icon in menu bar → Quit"
echo "   → Wait 10 seconds"
echo "   → Open Docker Desktop again"
echo "   → Wait 30-60 seconds"
echo ""

# Try to restart Docker Desktop
read -p "Would you like to try restarting Docker Desktop now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Restarting Docker Desktop..."
    killall Docker 2>/dev/null
    sleep 3
    open -a Docker
    echo ""
    echo "Waiting 30 seconds for Docker to start..."
    sleep 30
    
    if check_docker; then
        echo ""
        echo "🎉 Docker is now ready!"
        exit 0
    else
        echo ""
        echo "⚠️  Docker is still not ready. Please try Option B (Reset) above."
        exit 1
    fi
fi

echo ""
echo "Please follow one of the options above to fix Docker."

