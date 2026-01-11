# Production Deployment Guide

## Quick Start (3 Steps)

### 1. Install Ollama
Download from: https://ollama.com/download
```powershell
# After installation, pull the model:
ollama pull llama2
```

### 2. Install Python Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application
```powershell
# Start web server
python web_app.py
```
Access: http://127.0.0.1:5000

## System Requirements

- Python 3.8+
- 2GB RAM minimum
- Ollama (for AI music generation)
- Windows/Linux/Mac

## Manual CLI Mode

If you only want to test without web interface:
```powershell
python main.py
```

## Production Deployment

### Using a Production Server (Gunicorn recommended)

1. Install gunicorn:
```bash
pip install gunicorn
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 4. Run Application

**Development:**
```bash
python web_app.py
```

**Production (with Gunicorn):**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 web_app:app
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t music-generator .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/twitter_schedule.json:/app/twitter_schedule.json \
  --name music-generator \
  music-generator
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_MODEL` | Ollama model to use | `llama2` |
| `OLLAMA_TEMPERATURE` | LLM temperature | `0.7` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `FLASK_HOST` | Web server host | `0.0.0.0` |
| `FLASK_PORT` | Web server port | `5000` |
| `TWITTER_API_KEY` | Twitter API key (optional) | - |
| `TWITTER_API_SECRET` | Twitter API secret (optional) | - |
| `TWITTER_ACCESS_TOKEN` | Twitter access token (optional) | - |
| `TWITTER_ACCESS_SECRET` | Twitter access secret (optional) | - |

### Twitter API Setup (Optional)

1. Go to https://developer.twitter.com/
2. Create a new app
3. Generate API keys and tokens
4. Add credentials to `.env` file

**Note:** Application works in simulation mode without Twitter API credentials.

## Features

### Web Interface (http://localhost:5000)

1. **Ollama Prompt Interface**
   - Send custom prompts to Ollama
   - Real-time response streaming
   - Works only when Ollama is available

2. **Music Generation**
   - Generate tracks with AI or fallback mode
   - View track details (genre, mood, title)
   - Automatic knowledge base update

3. **Daily Operations**
   - Run all company operations
   - Generate music, process billing, create marketing
   - View detailed results

4. **Twitter Integration**
   - Post immediately
   - Schedule posts for specific times
   - View pending and posted content
   - Automatic background processing

5. **System Status**
   - Real-time service health monitoring
   - Ollama availability check
   - Twitter API status

## Monitoring

### Health Check

```bash
curl http://localhost:5000/api/status
```

### Logs

**Docker:**
```bash
docker-compose logs -f web
```

**Manual:**
```bash
# Check logs directory
tail -f logs/app.log
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000
# Linux/Mac:
lsof -i :5000

# Change port in .env or docker-compose.yml
```

### Ollama Not Available

```bash
# Install Ollama
# Visit: https://ollama.ai

# Pull model
ollama pull llama2

# Verify
ollama list
```

### Docker Issues

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check container status
docker-compose ps

# View container logs
docker-compose logs web
```

### Database/Storage Issues

```bash
# Reset vector database
rm -rf chroma_db/

# Reset Twitter schedule
rm twitter_schedule.json

# Restart application
```

## Performance Tuning

### Gunicorn Workers

```bash
# Formula: (2 x CPU cores) + 1
# For 4 cores:
gunicorn --workers 9 --bind 0.0.0.0:5000 web_app:app
```

### Ollama Optimization

```bash
# Use smaller model for faster inference
OLLAMA_MODEL=llama2:7b

# Or use faster alternatives
OLLAMA_MODEL=mistral
```

## Security

### Production Checklist

- [ ] Set strong secrets in `.env`
- [ ] Use HTTPS (reverse proxy with nginx/traefik)
- [ ] Limit API rate limits
- [ ] Enable firewall rules
- [ ] Keep dependencies updated
- [ ] Monitor logs regularly
- [ ] Backup `chroma_db/` and schedules

### Reverse Proxy (nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Backup

```bash
# Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz \
  chroma_db/ \
  twitter_schedule.json \
  knowledge_base.json

# Restore
tar -xzf backup-20260111.tar.gz
```

## Scaling

### Horizontal Scaling

1. Use external database (PostgreSQL) instead of JSON
2. Use Redis for session management
3. Deploy multiple instances behind load balancer
4. Use external vector store (Pinecone, Weaviate)

### Vertical Scaling

1. Increase Gunicorn workers
2. Use faster hardware
3. Optimize Ollama with GPU

## Support

For issues, check:
- Application logs
- Docker container logs
- System resource usage (CPU, memory)
- Network connectivity

## Maintenance

### Regular Tasks

- Review logs weekly
- Update dependencies monthly
- Backup data daily
- Monitor disk space
- Check scheduled posts

### Updates

```bash
# Pull latest code
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart services
docker-compose restart
```
