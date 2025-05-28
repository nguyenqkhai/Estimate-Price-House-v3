# Estimate-Price-House-v3 🏠

Bài tập cuối kỳ môn AI - Dự đoán giá nhà tại khu vực Tp.HCM với CI/CD Pipeline

🚀 **Latest Update**: Added ECS + EC2 dual deployment support with manual trigger

## 📋 Mô tả dự án

Ứng dụng dự đoán giá nhà sử dụng Machine Learning với giao diện Streamlit, được triển khai tự động thông qua GitHub Actions.

### 🔍 Quy trình thực hiện:

- **Crawl data** từ nhatot.com

  - Các dữ liệu bao gồm: Tên đường, Tên phường, Quận, Giấy tờ pháp lý, Diện tích, Số tầng, Số phòng ngủ, Số nhà vệ sinh, Hướng cửa chính, Loại hình nhà ở, Giá (VNĐ), Giá hiển thị, Giá/m² (VNĐ)
  - Số lượng dữ liệu: 20,000 tin rao bán

- **Làm sạch dữ liệu:**

  - Bỏ các dòng không hợp lệ
  - Các dòng không có số tầng đặt = 1
  - Cột 'Giấy tờ pháp lý': 1 (Đã có sổ), khác 1 (Chưa có sổ)

- **Chia tập dữ liệu:**

  - Tập train: 80%
  - Tập test: 20%

- **Training:** Sử dụng thuật toán XGBoost
- **Đánh giá mô hình:**
  ![Model Evaluation](https://github.com/user-attachments/assets/419e2cf2-ddb2-4e3c-8a47-000c2b373c7d)

## 🚀 Quick Start

### Cách 1: Chạy local với Python

```bash
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### Cách 2: Chạy với Docker

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 CI/CD Pipeline

🚀 **ECS Deployment Ready** - IAM permissions configured

Pipeline tự động bao gồm:

1. **Test** - Unit tests với pytest và coverage
2. **SonarCloud** - Code quality analysis
3. **Build & Push** - Docker image lên DockerHub
4. **Deploy** - Tự động deploy lên EC2

### 📋 Cấu hình Secrets

Thêm các secrets sau vào GitHub repository:

- `DOCKERHUB_USERNAME` - DockerHub username
- `DOCKERHUB_TOKEN` - DockerHub access token
- `SONAR_TOKEN` - SonarCloud token
- `EC2_HOST` - EC2 public IP
- `EC2_USERNAME` - EC2 username (ubuntu/ec2-user)
- `EC2_SSH_KEY` - SSH private key
- `EC2_PORT` - SSH port (22)

## 📚 Links

- **Colab Notebook:** https://colab.research.google.com/drive/12BuYHNFAIeoHqiWSOwr1ei8n3Q2M0jAe?usp=sharing
- **Live Demo:** https://estimate-price-house-v3-flameo.streamlit.app/
- **Deployment Guide:** [README_DEPLOYMENT.md](README_DEPLOYMENT.md)

## 🛠️ Tech Stack

- **Backend:** Python, Streamlit, XGBoost, Scikit-learn
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Code Quality:** SonarCloud, pytest
- **Deployment:** AWS EC2, DockerHub
- **Monitoring:** Health checks, Logging
