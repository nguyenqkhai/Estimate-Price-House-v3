#!/bin/bash

# Script deploy cho EC2
# Script này nên được chạy trên EC2 instance

set -e

# Cấu hình
DOCKER_IMAGE="house-price-estimator"
CONTAINER_NAME="house-price-app"
PORT="8501"

echo "Bắt đầu deployment..."

# Cập nhật system packages
echo "Đang cập nhật system packages..."
sudo apt-get update

# Cài đặt Docker nếu chưa có
if ! command -v docker &> /dev/null; then
    echo "Đang cài đặt Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker đã được cài đặt. Vui lòng logout và login lại để group changes có hiệu lực."
fi

# Cài đặt Docker Compose nếu chưa có
if ! command -v docker-compose &> /dev/null; then
    echo "Đang cài đặt Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Dừng và xóa container hiện tại nếu có
echo "Đang dừng container hiện tại..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Pull image mới nhất
echo "Đang pull Docker image mới nhất..."
docker pull $DOCKERHUB_USERNAME/$DOCKER_IMAGE:latest

# Chạy container mới
echo "Đang khởi động container mới..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    -p $PORT:$PORT \
    $DOCKERHUB_USERNAME/$DOCKER_IMAGE:latest

# Dọn dẹp old images
echo "Đang dọn dẹp old images..."
docker image prune -f

# Kiểm tra container có đang chạy không
echo "Đang kiểm tra trạng thái container..."
if docker ps | grep -q $CONTAINER_NAME; then
    echo "✅ Deployment thành công! Container đang chạy."
    echo "🌐 Ứng dụng có thể truy cập tại: http://$(curl -s ifconfig.me):$PORT"
else
    echo "❌ Deployment thất bại! Container không chạy."
    echo "Đang kiểm tra logs..."
    docker logs $CONTAINER_NAME
    exit 1
fi

echo "Deployment hoàn tất!"
