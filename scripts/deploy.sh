#!/bin/bash

echo "Deploying GitHub Multi-Agent Automation System..."

if [ ! -f .env ]; then
    echo ".env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

mkdir -p logs repos vector_store monitoring/grafana/dashboards

echo "Building and starting containers..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 30

echo "Setting up Ollama models..."
docker exec github-automation-ollama ollama pull codellama:7b

echo "Checking service health..."
if curl -f http://localhost:8000/health; then
    echo "GitHub Agent is healthy"
else
    echo "GitHub Agent health check failed"
    docker-compose logs github-agent
    exit 1
fi

echo "Setting up initial repository configurations..."
docker exec github-automation-github-agent-1 python config/setup.py

echo "Deployment completed successfully!"
echo ""
echo "Services available at:"
echo "   - GitHub Agent API: http://localhost:8000"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3000 (admin/admin)"
echo "   - Ollama: http://localhost:11434"
echo ""
echo "Next steps:"
echo "   1. Configure GitHub webhook: http://your-domain:8000/webhook/github"
echo "   2. Add repository configurations via API"
echo "   3. Monitor workflows in Grafana dashboard"