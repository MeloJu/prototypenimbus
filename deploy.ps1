# Deployment script for Windows
# Run with: .\deploy.ps1

Write-Host "🚀 Deploying Music Generator Company..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker version | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Create .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env file with your configuration" -ForegroundColor Yellow
}

# Build and start services
Write-Host "🏗️  Building Docker images..." -ForegroundColor Cyan
docker-compose build

Write-Host "🚀 Starting services..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if Ollama container is running
if (docker-compose ps | Select-String "ollama") {
    Write-Host "📦 Pulling llama2 model in Ollama..." -ForegroundColor Cyan
    try {
        docker-compose exec -T ollama ollama pull llama2
    } catch {
        Write-Host "⚠️  Model pull failed, will retry later" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Web interface: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🤖 Ollama API: http://localhost:11434" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 View logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "🛑 Stop services: docker-compose down" -ForegroundColor Yellow
Write-Host ""
