#!/bin/bash

# Aatra AI Setup Script
# This script sets up the complete Aatra AI system

set -e

echo "🚀 Setting up Aatra AI - Anti-India Campaign Monitoring System"
echo "=============================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating environment configuration..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your configurations (especially Twitter API keys)"
fi

# Build and start services
echo "🔨 Building Docker containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if backend is healthy
echo "🏥 Checking backend health..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy!"
        break
    else
        echo "⏳ Attempt $attempt/$max_attempts - Backend not ready yet..."
        sleep 5
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Backend failed to start properly"
    docker-compose logs backend
    exit 1
fi

# Initialize database
echo "📊 Initializing database with sample data..."
docker-compose exec -T backend python scripts/init_db.py

echo ""
echo "🎉 Aatra AI Setup Complete!"
echo "=============================================="
echo ""
echo "🌐 Frontend:    http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/docs"
echo ""
echo "🏃‍♂️ To stop the system:    docker-compose down"
echo "📋 To view logs:          docker-compose logs -f"
echo "🔄 To restart:            docker-compose restart"
echo ""
echo "🛡️ Happy Monitoring! Jai Hind! 🇮🇳"