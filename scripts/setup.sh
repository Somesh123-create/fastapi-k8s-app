#!/bin/bash

# Setup development environment

set -e

echo "🚀 Setting up FastAPI Kubernetes development environment..."

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [ "$PYTHON_VERSION" != "3.12" ]; then
    echo "⚠️  Python 3.12 is recommended (found: $PYTHON_VERSION)"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Edit .env with your configuration"
fi

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run 'make run' to start the application"
echo "3. Visit http://localhost:8000/docs for API documentation"
echo ""
