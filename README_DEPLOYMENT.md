# Hướng dẫn Deployment với GitHub Actions

## Tổng quan
Pipeline này sẽ tự động build, test, và deploy ứng dụng dự đoán giá nhà lên EC2 thông qua GitHub Actions.

## Cấu trúc Pipeline

### 1. Test Stage
- Chạy unit tests với pytest
- Tạo coverage report
- Upload coverage lên Codecov

### 2. SonarCloud Analysis
- Phân tích chất lượng code
- Kiểm tra security vulnerabilities
- Tạo báo cáo code quality

### 3. Build & Push Docker Image
- Build Docker image
- Push lên DockerHub với tag latest và commit SHA
- Sử dụng cache để tối ưu build time

### 4. Deploy to EC2
- SSH vào EC2 instance
- Pull image mới từ DockerHub
- Stop container cũ và start container mới
- Clean up old images

## Cấu hình Secrets

Bạn cần thêm các secrets sau vào GitHub repository:

### DockerHub
```
DOCKERHUB_USERNAME: your-dockerhub-username
DOCKERHUB_TOKEN: your-dockerhub-access-token
```

### SonarCloud
```
SONAR_TOKEN: your-sonarcloud-token
```

### EC2 Deployment
```
EC2_HOST: your-ec2-public-ip
EC2_USERNAME: ubuntu (hoặc ec2-user)
EC2_SSH_KEY: your-private-ssh-key
EC2_PORT: 22
```

## Cách thiết lập

### 1. Thiết lập DockerHub
1. Tạo tài khoản DockerHub
2. Tạo Access Token trong Settings > Security
3. Thêm DOCKERHUB_USERNAME và DOCKERHUB_TOKEN vào GitHub Secrets

### 2. Thiết lập SonarCloud
1. Đăng ký SonarCloud với GitHub account
2. Import repository
3. Lấy SONAR_TOKEN từ Account > Security
4. Cập nhật `sonar-project.properties` với organization key của bạn

### 3. Thiết lập EC2
1. Tạo EC2 instance (Ubuntu 20.04 LTS recommended)
2. Cấu hình Security Group mở port 8501
3. Tạo SSH key pair
4. Thêm SSH private key vào GitHub Secrets

### 4. Cấu hình EC2 Instance
```bash
# SSH vào EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Logout và login lại để áp dụng group changes
```

## Chạy Pipeline

Pipeline sẽ tự động chạy khi:
- Push code lên branch `main` hoặc `develop`
- Tạo Pull Request vào branch `main`

## Kiểm tra Deployment

Sau khi deploy thành công, ứng dụng sẽ có sẵn tại:
```
http://your-ec2-public-ip:8501
```

## Troubleshooting

### 1. Test failures
- Kiểm tra logs trong GitHub Actions
- Đảm bảo model files tồn tại trong repository

### 2. Docker build failures
- Kiểm tra Dockerfile syntax
- Đảm bảo requirements.txt đúng format

### 3. SonarCloud failures
- Kiểm tra SONAR_TOKEN
- Cập nhật sonar-project.properties với đúng organization key

### 4. EC2 deployment failures
- Kiểm tra SSH connection
- Đảm bảo EC2 có đủ disk space
- Kiểm tra Security Group rules

## Monitoring

### Health Check
Container có health check endpoint:
```
http://your-ec2-ip:8501/_stcore/health
```

### Logs
Xem logs container:
```bash
docker logs house-price-app
```

### Container Status
Kiểm tra container đang chạy:
```bash
docker ps
```

## Security Best Practices

1. **SSH Keys**: Sử dụng SSH keys thay vì passwords
2. **Secrets**: Không commit secrets vào code
3. **Docker**: Chạy container với non-root user
4. **Network**: Chỉ mở ports cần thiết
5. **Updates**: Thường xuyên update base images và dependencies
