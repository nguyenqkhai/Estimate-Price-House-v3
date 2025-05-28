# Hướng dẫn Setup các thành phần DevOps còn thiếu

## 1. Version Management ✅ (Đã implement)

**Đã thêm:**
- Semantic versioning sử dụng `github.run_number` và `github.sha`
- Version được inject vào Docker image và application

**Cách sử dụng:**
- Mỗi build sẽ có version format: `{run_number}.{git_sha}`
- Version được hiển thị trong health check endpoint

## 2. Artifacts Management ✅ (Đã implement)

**Đã thêm:**
- Upload test results và coverage reports
- Upload SonarCloud scan results  
- Upload Docker build artifacts
- Retention policy 30 ngày

**Artifacts được lưu:**
- Test coverage reports (XML + HTML)
- SonarCloud scan results
- Dockerfile và task definition

## 3. Health Check & Monitoring ✅ (Đã implement)

**Đã thêm:**
- Flask API với health check endpoints:
  - `/health` - Health status
  - `/metrics` - Application metrics
  - `/ready` - Readiness check
- Tests cho các endpoints
- Health check trong Docker container

## 4. ECR (Elastic Container Registry) ✅ (Đã implement)

**Cần setup trên AWS:**

### 4.1 Tạo ECR Repository
```bash
aws ecr create-repository --repository-name house-price-estimator --region us-east-1
```

### 4.2 Thêm GitHub Secrets
Cần thêm các secrets sau vào GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY` 
- `AWS_REGION` (ví dụ: us-east-1)
- `ECR_REPOSITORY_URI` (ví dụ: 123456789012.dkr.ecr.us-east-1.amazonaws.com/house-price-estimator)
- `AWS_ACCOUNT_ID`

## 5. ECS (Elastic Container Service) ✅ (Đã implement)

**Cần setup trên AWS:**

### 5.1 Tạo ECS Cluster
```bash
aws ecs create-cluster --cluster-name house-price-cluster --capacity-providers FARGATE
```

### 5.2 Tạo IAM Roles

**ECS Task Execution Role:**
```bash
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

**ECS Task Role:**
```bash
aws iam create-role --role-name ecsTaskRole --assume-role-policy-document file://trust-policy.json
```

### 5.3 Tạo CloudWatch Log Group
```bash
aws logs create-log-group --log-group-name /ecs/house-price
```

### 5.4 Tạo ECS Service
```bash
aws ecs create-service \
  --cluster house-price-cluster \
  --service-name house-price-service \
  --task-definition house-price-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

### 5.5 Thêm GitHub Secrets cho ECS
- `ECS_CLUSTER_NAME` (house-price-cluster)
- `ECS_SERVICE_NAME` (house-price-service)

## 6. Monitoring Setup (Cần implement thêm)

**Đã có:**
- Health check endpoints
- Application logs qua CloudWatch

**Cần thêm:**
- CloudWatch Alarms
- SNS notifications
- Application Performance Monitoring (APM)

### 6.1 Tạo CloudWatch Alarms
```bash
# CPU Utilization alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "ECS-HighCPU" \
  --alarm-description "Alarm when CPU exceeds 70%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 70 \
  --comparison-operator GreaterThanThreshold

# Health check alarm  
aws cloudwatch put-metric-alarm \
  --alarm-name "ECS-HealthCheck-Failed" \
  --alarm-description "Alarm when health check fails" \
  --metric-name HealthyHostCount \
  --namespace AWS/ApplicationELB \
  --statistic Average \
  --period 60 \
  --threshold 1 \
  --comparison-operator LessThanThreshold
```

## 7. Checklist Implementation

### ✅ Đã hoàn thành:
- [x] Version Management
- [x] Artifacts Management  
- [x] Health Check endpoints
- [x] ECR integration trong CI/CD
- [x] ECS deployment trong CI/CD
- [x] Tests cho API endpoints

### 🔄 Cần setup trên AWS:
- [ ] Tạo ECR repository
- [ ] Setup ECS cluster và service
- [ ] Tạo IAM roles
- [ ] Setup CloudWatch logs
- [ ] Thêm GitHub secrets

### 📈 Cần implement thêm:
- [ ] CloudWatch alarms
- [ ] SNS notifications
- [ ] Application metrics collection
- [ ] Performance monitoring dashboard

## 8. Lệnh để test local

```bash
# Test Flask API
python api.py &
curl http://localhost:5000/health
curl http://localhost:5000/metrics
curl http://localhost:5000/ready

# Test Docker build
docker build -t house-price-test .
docker run -p 8501:8501 -p 5000:5000 house-price-test

# Run tests
pytest test_app.py -v
```
