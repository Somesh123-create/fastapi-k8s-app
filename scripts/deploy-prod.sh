#!/bin/bash

# Deploy to Kubernetes - Production Environment

set -e

NAMESPACE="production"
RELEASE_NAME="fastapi-app"
CHART_PATH="./helm/fastapi-k8s-app"
VALUES_FILE="./helm/fastapi-k8s-app/values-prod.yaml"

echo "🚀 Deploying to Kubernetes Production Environment..."

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

# Confirmation
echo "⚠️  This will deploy to PRODUCTION"
read -p "Are you sure? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Deployment cancelled"
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
    --timeout 10m

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/$RELEASE_NAME -n $NAMESPACE

# Run smoke tests
echo "🧪 Running smoke tests..."
PODS=$(kubectl get pods -n $NAMESPACE -l "app.kubernetes.io/name=fastapi-k8s-app" -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n $NAMESPACE $PODS -- curl -f http://localhost:8000/health || {
    echo "❌ Health check failed"
    exit 1
}

# Get deployment info
echo ""
echo "✅ Production deployment successful!"
echo ""
echo "📊 Deployment Information:"
kubectl get pods -n $NAMESPACE -l "app.kubernetes.io/name=fastapi-k8s-app"
echo ""
echo "🔗 Checking service:"
kubectl get svc -n $NAMESPACE
echo ""
