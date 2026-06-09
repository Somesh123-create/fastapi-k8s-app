#!/bin/bash

# Run Minikube for local Kubernetes development

set -e

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube not found. Installing Minikube..."
    # Installation instructions
    echo "Please install Minikube from https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

echo "🚀 Starting Minikube..."

# Start Minikube
minikube start --driver=docker --cpus=4 --memory=8192

# Get Minikube Docker environment
echo ""
echo "📝 Setting up Docker environment..."
eval $(minikube docker-env)

# Build Docker image in Minikube
echo "🐳 Building Docker image in Minikube..."
docker build -t fastapi-k8s-app:latest .

# Deploy to Minikube
echo "⚙️ Deploying to Minikube..."
kubectl apply -f kubernetes/dev/

# Wait for deployment
kubectl rollout status deployment/fastapi-app -n default

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)
echo ""
echo "✅ Minikube setup complete!"
echo ""
echo "Access your application:"
echo "  kubectl port-forward svc/fastapi-app 8000:80"
echo "  http://localhost:8000"
echo ""
echo "View Minikube dashboard:"
echo "  minikube dashboard"
echo ""
