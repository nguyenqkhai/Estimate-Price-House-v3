#!/bin/bash

# Script để tạo IAM roles cần thiết cho ECS

echo "🔧 Tạo IAM roles cho ECS..."

# Trust policy cho ECS tasks
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Tạo ECS Task Execution Role
echo "📋 Tạo ECS Task Execution Role..."
if ! aws iam get-role --role-name ecsTaskExecutionRole 2>/dev/null; then
  aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://trust-policy.json

  aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
  
  echo "✅ Đã tạo ecsTaskExecutionRole"
else
  echo "✅ ecsTaskExecutionRole đã tồn tại"
fi

# Tạo ECS Task Role
echo "📋 Tạo ECS Task Role..."
if ! aws iam get-role --role-name ecsTaskRole 2>/dev/null; then
  aws iam create-role \
    --role-name ecsTaskRole \
    --assume-role-policy-document file://trust-policy.json
  
  echo "✅ Đã tạo ecsTaskRole"
else
  echo "✅ ecsTaskRole đã tồn tại"
fi

# Lấy Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo ""
echo "🎯 IAM Role ARNs:"
echo "=================================="
echo "Task Execution Role: arn:aws:iam::${ACCOUNT_ID}:role/ecsTaskExecutionRole"
echo "Task Role: arn:aws:iam::${ACCOUNT_ID}:role/ecsTaskRole"

# Cleanup
rm -f trust-policy.json

echo ""
echo "✅ Hoàn thành tạo IAM roles!"
