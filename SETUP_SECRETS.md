# 🔐 Hướng dẫn Setup GitHub Secrets

Để pipeline CI/CD hoạt động đầy đủ, bạn cần thêm các secrets sau vào GitHub repository.

## 📋 **Danh sách Secrets cần thiết:**

### ✅ **Đã có:**
- `SONAR_TOKEN` - ✅ Đã thêm

### ⚠️ **Cần thêm:**

#### 1. **DockerHub Secrets**
- `DOCKERHUB_USERNAME` - DockerHub username
- `DOCKERHUB_TOKEN` - DockerHub access token

#### 2. **EC2 Deployment Secrets** (Optional)
- `EC2_HOST` - EC2 public IP address
- `EC2_USERNAME` - EC2 username (ubuntu/ec2-user)
- `EC2_SSH_KEY` - SSH private key
- `EC2_PORT` - SSH port (thường là 22)

## 🔧 **Cách thêm Secrets:**

### **Bước 1: Vào GitHub Repository Settings**
1. Vào repository GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**

### **Bước 2: Tạo DockerHub Access Token**
1. Đăng nhập **DockerHub** (https://hub.docker.com)
2. **Avatar** → **Account Settings** → **Security**
3. **New Access Token**:
   - Name: `GitHub Actions`
   - Permissions: `Read, Write, Delete`
4. **Generate** và copy token

### **Bước 3: Thêm DockerHub Secrets**

**Secret 1:**
- Name: `DOCKERHUB_USERNAME`
- Secret: `your-dockerhub-username`

**Secret 2:**
- Name: `DOCKERHUB_TOKEN`
- Secret: `paste-your-access-token`

## 🚀 **Kích hoạt lại Pipeline:**

### **Sau khi thêm DockerHub secrets:**

1. **Uncomment Docker build trong workflow:**
   - Edit `.github/workflows/ci-cd.yml`
   - Bỏ comment các phần `build-and-push` và `deploy`

2. **Push code để trigger pipeline:**
```bash
git add .
git commit -m "Enable Docker build and deploy"
git push
```

## 📊 **Trạng thái hiện tại:**

### ✅ **Đang hoạt động:**
- ✅ Test stage (pytest)
- ✅ SonarCloud analysis (sau khi tắt Automatic Analysis)

### ⏸️ **Tạm thời disabled:**
- ⏸️ Docker build & push (chờ DockerHub secrets)
- ⏸️ EC2 deployment (chờ EC2 secrets)

## 🔍 **Kiểm tra Pipeline:**

1. **Vào GitHub** → **Actions** tab
2. **Xem workflow runs**
3. **Test và SonarCloud** sẽ chạy thành công
4. **Docker build** sẽ được skip cho đến khi có secrets

## 📝 **Ghi chú:**

- **SonarCloud:** Nhớ tắt "Automatic Analysis" trong SonarCloud project settings
- **EC2:** Chỉ cần thiết nếu muốn auto-deploy lên server
- **DockerHub:** Cần thiết để build và lưu trữ Docker images

## 🆘 **Troubleshooting:**

### **Nếu SonarCloud vẫn lỗi:**
1. Kiểm tra đã tắt "Automatic Analysis" chưa
2. Verify SONAR_TOKEN đã được thêm đúng
3. Check project key và organization trong `sonar-project.properties`

### **Nếu muốn test local:**
```bash
# Test ứng dụng
python -m pytest test_app.py -v

# Chạy ứng dụng
streamlit run app.py

# Build Docker image
docker build -t house-price-app .
docker run -p 8501:8501 house-price-app
```
