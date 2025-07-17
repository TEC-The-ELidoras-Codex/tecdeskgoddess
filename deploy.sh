#!/bin/bash

# TEC Enhanced Persona System - Docker Deployment Script
# For deploying to Linux machines

set -e

echo "🚀 TEC Enhanced Persona System - Docker Deployment"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data
mkdir -p backups
mkdir -p logs
mkdir -p config

# Set permissions for Linux
chmod 755 data backups logs config

# Copy environment template if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cat > .env << EOF
# TEC Enhanced Persona System Environment Variables
ENVIRONMENT=production
DATABASE_PATH=/app/data/tec_database.db
BACKUP_ENABLED=true
BACKUP_INTERVAL=3600
LOG_LEVEL=INFO

# API Keys (replace with your keys)
GITHUB_TOKEN=your_github_token_here
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Redis settings
REDIS_URL=redis://redis:6379/0
EOF
    echo "⚠️  Please edit .env file with your API keys before continuing!"
    echo "   nano .env"
    read -p "Press Enter when you've updated the .env file..."
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t tec-persona:latest .

# Start the services
echo "🚀 Starting TEC Enhanced Persona System..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ TEC Persona API is running!"
else
    echo "❌ API health check failed. Checking logs..."
    docker-compose logs tec-persona
fi

# Display status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 Deployment Complete!"
echo "==============================================="
echo "🌐 Enhanced Interface: http://localhost:8000/tec_enhanced_interface.html"
echo "🎮 Complete Interface: http://localhost:8000/tec_complete_interface.html"
echo "📋 API Health: http://localhost:8000/health"
echo "📊 System Stats: http://localhost:8000/api/system/stats"
echo ""
echo "📝 Useful Commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Backup data: docker-compose exec tec-persona python -m tec_tools.data_persistence backup"
echo ""

# Initialize character lore
echo "🎭 Initializing character lore..."
docker-compose exec tec-persona python scripts/initialize_character_lore.py

echo "✨ TEC Enhanced Persona System is ready!"
echo "   Access the enhanced interface at: http://localhost:8000/tec_enhanced_interface.html"
