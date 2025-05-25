#!/bin/bash

# Deploy script for EC2
# This script should be run on the EC2 instance

set -e

# Configuration
DOCKER_IMAGE="house-price-estimator"
CONTAINER_NAME="house-price-app"
PORT="8501"

echo "Starting deployment..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker installed. Please log out and log back in for group changes to take effect."
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Stop and remove existing container if it exists
echo "Stopping existing container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Pull the latest image
echo "Pulling latest Docker image..."
docker pull $DOCKERHUB_USERNAME/$DOCKER_IMAGE:latest

# Run the new container
echo "Starting new container..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    -p $PORT:$PORT \
    $DOCKERHUB_USERNAME/$DOCKER_IMAGE:latest

# Clean up old images
echo "Cleaning up old images..."
docker image prune -f

# Check if container is running
echo "Checking container status..."
if docker ps | grep -q $CONTAINER_NAME; then
    echo "✅ Deployment successful! Container is running."
    echo "🌐 Application is available at: http://$(curl -s ifconfig.me):$PORT"
else
    echo "❌ Deployment failed! Container is not running."
    echo "Checking logs..."
    docker logs $CONTAINER_NAME
    exit 1
fi

echo "Deployment completed!"
