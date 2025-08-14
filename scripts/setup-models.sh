#!/bin/bash

echo "Setting up AI models..."

echo "Pulling CodeLlama model..."
docker exec github-automation-ollama ollama pull codellama:7b

echo "Pulling additional models (optional)..."
docker exec github-automation-ollama ollama pull llama2:7b

echo "Models setup completed!"

echo "Installed models:"
docker exec github-automation-ollama ollama list