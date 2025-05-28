# Sử dụng Python 3.9 slim image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt system dependencies (tắt recommended packages để bảo mật)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để tận dụng Docker cache
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (chỉ copy files cần thiết để tránh sensitive data)
COPY app.py .
COPY api.py .
COPY start.sh .
COPY model_estimate_price_house_v5.pkl .
COPY encoder_v5.pkl .

# Tạo non-root user để bảo mật (giải quyết security hotspot)
# Điều này ngăn container chạy với quyền root, giảm rủi ro bảo mật
# Merge RUN instructions để giảm layers và tối ưu image size
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app && \
    chmod +x start.sh
USER appuser

# Expose ports (8501 cho Streamlit, 5000 cho Flask API)
EXPOSE 8501 5000

# Health check sử dụng Flask API endpoint
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:5000/health"]

# Chạy cả hai ứng dụng
CMD ["./start.sh"]
