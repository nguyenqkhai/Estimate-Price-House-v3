#!/bin/bash

# Script thiết lập cho môi trường phát triển local

set -e

echo "🚀 Thiết lập môi trường phát triển House Price Estimator..."

# Kiểm tra Python đã cài đặt chưa
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 chưa được cài đặt. Vui lòng cài đặt Python 3.9 trở lên."
    exit 1
fi

# Kiểm tra phiên bản Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Cần Python $required_version trở lên. Phiên bản hiện tại: $python_version"
    exit 1
fi

echo "✅ Đã phát hiện Python $python_version"

# Tạo virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Đang tạo virtual environment..."
    python3 -m venv venv
fi

# Kích hoạt virtual environment
echo "🔧 Đang kích hoạt virtual environment..."
source venv/bin/activate

# Nâng cấp pip
echo "⬆️ Đang nâng cấp pip..."
pip install --upgrade pip

# Cài đặt dependencies
echo "📚 Đang cài đặt dependencies..."
pip install -r requirements.txt

# Kiểm tra model files có tồn tại không
if [ ! -f "model_estimate_price_house_v5.pkl" ] || [ ! -f "encoder_v5.pkl" ]; then
    echo "⚠️ Cảnh báo: Không tìm thấy model files. Vui lòng đảm bảo bạn có:"
    echo "   - model_estimate_price_house_v5.pkl"
    echo "   - encoder_v5.pkl"
    echo "   Các files này cần thiết để ứng dụng hoạt động."
fi

# Chạy tests
echo "🧪 Đang chạy tests..."
pytest test_app.py -v

# Kiểm tra Docker đã cài đặt chưa
if command -v docker &> /dev/null; then
    echo "🐳 Đã phát hiện Docker. Bạn cũng có thể chạy app bằng Docker:"
    echo "   docker-compose up --build"
else
    echo "⚠️ Không tìm thấy Docker. Cài đặt Docker để sử dụng containerized deployment."
fi

echo ""
echo "✅ Thiết lập hoàn tất!"
echo ""
echo "Để khởi động ứng dụng:"
echo "1. Kích hoạt virtual environment: source venv/bin/activate"
echo "2. Chạy app: streamlit run app.py"
echo "3. Mở browser: http://localhost:8501"
echo ""
echo "Để deploy bằng Docker:"
echo "1. Build và chạy: docker-compose up --build"
echo "2. Mở browser: http://localhost:8501"
echo ""
echo "Chúc bạn code vui vẻ! 🎉"
