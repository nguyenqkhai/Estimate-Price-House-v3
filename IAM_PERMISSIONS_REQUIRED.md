# IAM Permissions Required cho GitHub Actions

## Permissions cần thiết cho IAM User

Khi tạo IAM User `github-actions-user`, cần attach các policies sau:

### 1. **Managed Policies (AWS cung cấp sẵn):**
```
- AmazonEC2ContainerRegistryFullAccess
- AmazonECS_FullAccess  
- CloudWatchLogsFullAccess
- IAMFullAccess (để tạo ECS roles)
- EC2ReadOnlyAccess (để lấy VPC/subnet info)
```

### 2. **Custom Policy (nếu muốn giới hạn quyền hơn):**

Thay vì `IAMFullAccess`, có thể tạo custom policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:GetRole",
                "iam:AttachRolePolicy",
                "iam:PassRole",
                "sts:GetCallerIdentity"
            ],
            "Resource": [
                "arn:aws:iam::*:role/ecsTaskExecutionRole",
                "arn:aws:iam::*:role/ecsTaskRole"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVpcs",
                "ec2:DescribeSubnets", 
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}
```

## Cách thêm permissions:

### Qua AWS Console:
1. IAM → Users → `github-actions-user`
2. Permissions tab → Add permissions
3. Attach policies directly
4. Tìm và chọn các policies trên

### Qua AWS CLI:
```bash
# Attach managed policies
aws iam attach-user-policy --user-name github-actions-user --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
aws iam attach-user-policy --user-name github-actions-user --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess
aws iam attach-user-policy --user-name github-actions-user --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
aws iam attach-user-policy --user-name github-actions-user --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
aws iam attach-user-policy --user-name github-actions-user --policy-arn arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess
```

## Tại sao cần các permissions này:

- **ECR**: Push/pull Docker images
- **ECS**: Tạo cluster, service, task definition
- **CloudWatch**: Tạo log groups, xem logs
- **IAM**: Tạo execution roles cho ECS tasks
- **EC2**: Lấy thông tin VPC, subnets cho ECS networking
- **STS**: Lấy Account ID

## Security Best Practices:

1. **Principle of Least Privilege**: Chỉ cấp quyền tối thiểu cần thiết
2. **Separate Environments**: Dùng IAM users khác nhau cho dev/staging/prod
3. **Regular Rotation**: Rotate access keys định kỳ
4. **Monitoring**: Enable CloudTrail để audit API calls
