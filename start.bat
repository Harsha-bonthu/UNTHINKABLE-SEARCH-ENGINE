@echo off
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
pause