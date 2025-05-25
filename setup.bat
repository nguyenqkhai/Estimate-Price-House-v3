@echo off
echo 🚀 Setting up House Price Estimator development environment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check if model files exist
if not exist "model_estimate_price_house_v5.pkl" (
    echo ⚠️ Warning: model_estimate_price_house_v5.pkl not found
)
if not exist "encoder_v5.pkl" (
    echo ⚠️ Warning: encoder_v5.pkl not found
)

REM Run tests
echo 🧪 Running tests...
pytest test_app.py -v

echo.
echo ✅ Setup complete!
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the app: streamlit run app.py
echo 3. Open browser: http://localhost:8501
echo.
echo For Docker deployment:
echo 1. Build and run: docker-compose up --build
echo 2. Open browser: http://localhost:8501
echo.
echo Happy coding! 🎉
pause
