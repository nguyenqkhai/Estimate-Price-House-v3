#!/bin/bash

# Script để lấy AWS secrets cho GitHub Actions
# Chạy script này sau khi đã configure AWS CLI

echo "🔍 Đang lấy thông tin AWS..."

# Kiểm tra AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI chưa được cài đặt. Vui lòng cài đặt AWS CLI trước."
    exit 1
fi

# Kiểm tra AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials chưa được configure. Chạy 'aws configure' trước."
    exit 1
fi

echo "✅ AWS CLI đã sẵn sàng"
echo ""

# Lấy Account ID
echo "📋 AWS Account ID:"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID"
echo ""

# Lấy Region hiện tại
echo "🌍 AWS Region:"
AWS_REGION=$(aws configure get region)
echo "AWS_REGION=$AWS_REGION"
echo ""

# Tạo ECR repository nếu chưa có
echo "🐳 Tạo ECR Repository..."
REPO_NAME="house-price-estimator"

# Kiểm tra repository đã tồn tại chưa
if aws ecr describe-repositories --repository-names $REPO_NAME --region $AWS_REGION &> /dev/null; then
    echo "✅ ECR Repository '$REPO_NAME' đã tồn tại"
else
    echo "🔨 Tạo ECR Repository '$REPO_NAME'..."
    aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION > /dev/null
    echo "✅ Đã tạo ECR Repository"
fi

# Lấy ECR URI
ECR_URI=$(aws ecr describe-repositories --repository-names $REPO_NAME --query 'repositories[0].repositoryUri' --output text --region $AWS_REGION)
echo "ECR_REPOSITORY_URI=$ECR_URI"
echo ""

# Tạo ECS Cluster nếu chưa có
echo "🚀 Tạo ECS Cluster..."
CLUSTER_NAME="house-price-cluster"

# Kiểm tra cluster đã tồn tại chưa
if aws ecs describe-clusters --clusters $CLUSTER_NAME --region $AWS_REGION --query 'clusters[0].status' --output text 2>/dev/null | grep -q "ACTIVE"; then
    echo "✅ ECS Cluster '$CLUSTER_NAME' đã tồn tại"
else
    echo "🔨 Tạo ECS Cluster '$CLUSTER_NAME'..."
    aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $AWS_REGION > /dev/null
    echo "✅ Đã tạo ECS Cluster"
fi

echo "ECS_CLUSTER_NAME=$CLUSTER_NAME"
echo "ECS_SERVICE_NAME=house-price-service"
echo ""

# Tạo CloudWatch Log Group
echo "📊 Tạo CloudWatch Log Group..."
LOG_GROUP="/ecs/house-price"

if aws logs describe-log-groups --log-group-name-prefix $LOG_GROUP --region $AWS_REGION --query 'logGroups[0].logGroupName' --output text 2>/dev/null | grep -q "$LOG_GROUP"; then
    echo "✅ Log Group '$LOG_GROUP' đã tồn tại"
else
    echo "🔨 Tạo Log Group '$LOG_GROUP'..."
    aws logs create-log-group --log-group-name $LOG_GROUP --region $AWS_REGION
    echo "✅ Đã tạo Log Group"
fi

echo ""
echo "🎯 TỔNG KẾT - GitHub Secrets cần thêm:"
echo "=================================="
echo "AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID"
echo "AWS_REGION=$AWS_REGION"
echo "ECR_REPOSITORY_URI=$ECR_URI"
echo "ECS_CLUSTER_NAME=$CLUSTER_NAME"
echo "ECS_SERVICE_NAME=house-price-service"
echo ""
echo "⚠️  Còn thiếu (cần tạo IAM User):"
echo "AWS_ACCESS_KEY_ID=<từ IAM User>"
echo "AWS_SECRET_ACCESS_KEY=<từ IAM User>"
echo ""
echo "📝 Hướng dẫn tạo IAM User:"
echo "1. Vào AWS Console → IAM → Users → Create User"
echo "2. Tên: github-actions-user"
echo "3. Attach policies:"
echo "   - AmazonEC2ContainerRegistryFullAccess"
echo "   - AmazonECS_FullAccess"
echo "   - CloudWatchLogsFullAccess"
echo "4. Tạo Access Key → Download credentials"
echo ""
echo "✅ Hoàn thành! Copy các giá trị trên vào GitHub Secrets."
