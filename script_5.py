# Create environment and configuration files

files_content = {}

# 9. .env.template
files_content['.env.template'] = '''# Environment Configuration for RAG Knowledge Base

# OpenAI API Configuration (Optional - system works without it)
# Get your API key from: https://platform.openai.com/account/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Environment
ENVIRONMENT=development

# Embedding Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Vector Store Configuration
VECTOR_INDEX_PATH=data/vector_index.faiss
VECTOR_METADATA_PATH=data/vector_metadata.pkl

# Document Processing
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_FILE_SIZE_MB=50

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# Logging
LOG_LEVEL=INFO'''

# 10. .gitignore
files_content['.gitignore'] = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
uploads/
data/
logs/
vector_data/
*.faiss
*.pkl
.env

# Docker
.docker/

# Logs
*.log

# Database
*.db
*.sqlite

# Temporary files
*.tmp
*.temp

# Model files (if large)
models/
checkpoints/

# Test outputs
test_outputs/'''

# 11. start.sh
files_content['start.sh'] = '''#!/bin/bash

# RAG Knowledge Base - Quick Start Script
# This script helps you get the RAG system running quickly

set -e

echo "🔍 RAG Knowledge Base - Quick Start"
echo "=================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.template .env
    echo "✅ Created .env file from template"
    echo "💡 You can edit .env to add your OpenAI API key (optional)"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads data logs
echo "✅ Directories created"

# Build and start the services
echo "🚀 Building and starting services..."
docker-compose down --remove-orphans 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are healthy
echo "🔍 Checking service health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend service is healthy"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend service failed to start"
        echo "📋 Checking logs:"
        docker-compose logs rag-api
        exit 1
    fi
    sleep 2
done

# Check if frontend is accessible
if curl -s http://localhost > /dev/null 2>&1; then
    echo "✅ Frontend service is healthy"
else
    echo "❌ Frontend service is not accessible"
    echo "📋 Checking logs:"
    docker-compose logs nginx
    exit 1
fi

echo ""
echo "🎉 RAG Knowledge Base is now running!"
echo "=================================="
echo "🌐 Web Interface:    http://localhost"
echo "📚 API Documentation: http://localhost/docs"
echo "🔍 Health Check:     http://localhost/health"
echo ""
echo "📖 Usage:"
echo "1. Open http://localhost in your browser"
echo "2. Upload a document (PDF, DOCX, TXT, or MD)"
echo "3. Ask questions about your document"
echo ""
echo "🛑 To stop the system:"
echo "   docker-compose down"
echo ""
echo "📋 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "💡 Tip: Edit .env file to add your OpenAI API key for better responses"'''

# 12. start.bat
files_content['start.bat'] = '''@echo off
REM RAG Knowledge Base - Quick Start Script for Windows

echo.
echo 🔍 RAG Knowledge Base - Quick Start
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first:
    echo    https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first:
    echo    https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating environment file...
    copy .env.template .env
    echo ✅ Created .env file from template
    echo 💡 You can edit .env to add your OpenAI API key optional
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist uploads mkdir uploads
if not exist data mkdir data
if not exist logs mkdir logs
echo ✅ Directories created

REM Build and start the services
echo 🚀 Building and starting services...
docker-compose down --remove-orphans >nul 2>&1
docker-compose build --no-cache
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are healthy
echo 🔍 Checking service health...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend service failed to start
    echo 📋 Checking logs:
    docker-compose logs rag-api
    pause
    exit /b 1
)
echo ✅ Backend service is healthy

REM Check if frontend is accessible
curl -s http://localhost >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend service is not accessible
    echo 📋 Checking logs:
    docker-compose logs nginx
    pause
    exit /b 1
)
echo ✅ Frontend service is healthy

echo.
echo 🎉 RAG Knowledge Base is now running!
echo ==================================
echo 🌐 Web Interface:      http://localhost
echo 📚 API Documentation:  http://localhost/docs
echo 🔍 Health Check:       http://localhost/health
echo.
echo 📖 Usage:
echo 1. Open http://localhost in your browser
echo 2. Upload a document PDF, DOCX, TXT, or MD
echo 3. Ask questions about your document
echo.
echo 🛑 To stop the system:
echo    docker-compose down
echo.
echo 📋 To view logs:
echo    docker-compose logs -f
echo.
echo 💡 Tip: Edit .env file to add your OpenAI API key for better responses
echo.
pause'''

# Create files
for filename, content in files_content.items():
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✅ Created {filename}")

print("Created environment and startup files")