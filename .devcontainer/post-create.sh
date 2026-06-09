#!/bin/bash

# Post-create script for development container

set -e

echo "🚀 Setting up FastAPI K8s App development environment..."

# Update package lists
apt-get update
apt-get install -y --no-install-recommends \
    postgresql-client-15 \
    redis-tools \
    curl \
    git

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements-dev.txt

# Initialize Git hooks
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "✅ Pre-commit hooks installed"
fi

echo "✅ Development environment setup complete!"
echo ""
echo "📚 Quick start commands:"
echo "  make install       - Install dependencies"
echo "  make run          - Run the application"
echo "  make test         - Run tests"
echo "  make lint         - Run linting"
echo "  make docker-build - Build Docker image"
echo "  make k8s-deploy-dev - Deploy to Kubernetes dev"
echo ""
