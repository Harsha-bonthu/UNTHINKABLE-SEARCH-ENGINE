#!/bin/bash

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
echo "💡 Tip: Edit .env file to add your OpenAI API key for better responses"