# TEC Enhanced Persona System - Windows Deployment Script

Write-Host "🚀 TEC Enhanced Persona System - Windows Deployment" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "   Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose not found. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Create data directories
Write-Host "📁 Creating data directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "data" | Out-Null
New-Item -ItemType Directory -Force -Path "backups" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "config" | Out-Null

# Copy environment template if it doesn't exist
if (!(Test-Path ".env")) {
    Write-Host "📝 Creating environment file..." -ForegroundColor Green
    
    $envContent = @"
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
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    
    Write-Host "⚠️  Please edit .env file with your API keys before continuing!" -ForegroundColor Yellow
    Write-Host "   notepad .env" -ForegroundColor Yellow
    Read-Host "Press Enter when you've updated the .env file"
}

# Build the Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Green
docker build -t tec-persona:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

# Start the services
Write-Host "🚀 Starting TEC Enhanced Persona System..." -ForegroundColor Green
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services!" -ForegroundColor Red
    exit 1
}

# Wait for services to start
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service health
Write-Host "🏥 Checking service health..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ TEC Persona API is running!" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ API health check failed. Checking logs..." -ForegroundColor Red
    docker-compose logs tec-persona
}

# Display status
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host "🌐 Enhanced Interface: http://localhost:8000/tec_enhanced_interface.html" -ForegroundColor Cyan
Write-Host "🎮 Complete Interface: http://localhost:8000/tec_complete_interface.html" -ForegroundColor Cyan
Write-Host "📋 API Health: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "📊 System Stats: http://localhost:8000/api/system/stats" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Useful Commands:" -ForegroundColor Yellow
Write-Host "   View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop services: docker-compose down" -ForegroundColor White
Write-Host "   Restart: docker-compose restart" -ForegroundColor White
Write-Host "   Backup data: docker-compose exec tec-persona python -m tec_tools.data_persistence backup" -ForegroundColor White
Write-Host ""

# Initialize character lore
Write-Host "🎭 Initializing character lore..." -ForegroundColor Green
docker-compose exec tec-persona python scripts/initialize_character_lore.py

Write-Host "✨ TEC Enhanced Persona System is ready!" -ForegroundColor Green
Write-Host "   Access the enhanced interface at: http://localhost:8000/tec_enhanced_interface.html" -ForegroundColor Cyan

# Open browser
Write-Host "🌐 Opening enhanced interface in browser..." -ForegroundColor Green
Start-Process "http://localhost:8000/tec_enhanced_interface.html"
