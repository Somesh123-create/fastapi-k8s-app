#!/bin/bash

# Build Docker image and push to registry

set -e

REGISTRY=${1:-"ghcr.io"}
IMAGE_NAME=${2:-"fastapi-k8s-app"}
VERSION=${3:-"latest"}

FULL_IMAGE_NAME="$REGISTRY/$IMAGE_NAME:$VERSION"

echo "🐳 Building Docker image: $FULL_IMAGE_NAME"

# Build image
docker build -t "$FULL_IMAGE_NAME" .

echo "✅ Docker image built successfully"
echo ""
echo "To push to registry:"
echo "  docker push $FULL_IMAGE_NAME"
echo ""
