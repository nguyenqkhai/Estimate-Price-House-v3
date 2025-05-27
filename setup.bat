@echo off
echo 🚀 Thiết lập môi trường phát triển House Price Estimator...

REM Kiểm tra Python đã cài đặt chưa
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python chưa được cài đặt. Vui lòng cài đặt Python 3.9 trở lên.
    pause
    exit /b 1
)

echo ✅ Đã phát hiện Python

REM Tạo virtual environment
if not exist "venv" (
    echo 📦 Đang tạo virtual environment...
    python -m venv venv
)

REM Kích hoạt virtual environment
echo 🔧 Đang kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Nâng cấp pip
echo ⬆️ Đang nâng cấp pip...
python -m pip install --upgrade pip

REM Cài đặt dependencies
echo 📚 Đang cài đặt dependencies...
pip install -r requirements.txt

REM Kiểm tra model files có tồn tại không
if not exist "model_estimate_price_house_v5.pkl" (
    echo ⚠️ Cảnh báo: Không tìm thấy model_estimate_price_house_v5.pkl
)
if not exist "encoder_v5.pkl" (
    echo ⚠️ Cảnh báo: Không tìm thấy encoder_v5.pkl
)

REM Chạy tests
echo 🧪 Đang chạy tests...
pytest test_app.py -v

echo.
echo ✅ Thiết lập hoàn tất!
echo.
echo Để khởi động ứng dụng:
echo 1. Kích hoạt virtual environment: venv\Scripts\activate.bat
echo 2. Chạy app: streamlit run app.py
echo 3. Mở browser: http://localhost:8501
echo.
echo Để deploy bằng Docker:
echo 1. Build và chạy: docker-compose up --build
echo 2. Mở browser: http://localhost:8501
echo.
echo Chúc bạn code vui vẻ! 🎉
pause
