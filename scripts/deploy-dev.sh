#!/bin/bash

# Deploy to Kubernetes - Development Environment

set -e

NAMESPACE="default"
RELEASE_NAME="fastapi-app"
CHART_PATH="./helm/fastapi-k8s-app"
VALUES_FILE="./helm/fastapi-k8s-app/values-dev.yaml"

echo "🚀 Deploying to Kubernetes Development Environment..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl."
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "❌ helm not found. Please install helm."
    exit 1
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t fastapi-k8s-app:latest .

# Create namespace if it doesn't exist
echo "📝 Ensuring namespace exists..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Deploy using Helm
echo "⚙️ Deploying with Helm..."
helm upgrade --install $RELEASE_NAME $CHART_PATH \
    --namespace $NAMESPACE \
    --values $VALUES_FILE \
    --wait \
    --timeout 5m

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/$RELEASE_NAME -n $NAMESPACE

# Get deployment info
echo ""
echo "✅ Deployment successful!"
echo ""
echo "📊 Deployment Information:"
kubectl get pods -n $NAMESPACE -l "app.kubernetes.io/name=fastapi-k8s-app"
echo ""
echo "🔗 Port forwarding (optional):"
echo "kubectl port-forward svc/$RELEASE_NAME 8000:80 -n $NAMESPACE"
echo ""
