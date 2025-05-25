#!/bin/bash

# Setup script for local development

set -e

echo "🚀 Setting up House Price Estimator development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if model files exist
if [ ! -f "model_estimate_price_house_v5.pkl" ] || [ ! -f "encoder_v5.pkl" ]; then
    echo "⚠️ Warning: Model files not found. Please ensure you have:"
    echo "   - model_estimate_price_house_v5.pkl"
    echo "   - encoder_v5.pkl"
    echo "   These files are required for the application to work."
fi

# Run tests
echo "🧪 Running tests..."
pytest test_app.py -v

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "🐳 Docker detected. You can also run the app using Docker:"
    echo "   docker-compose up --build"
else
    echo "⚠️ Docker not found. Install Docker to use containerized deployment."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the app: streamlit run app.py"
echo "3. Open browser: http://localhost:8501"
echo ""
echo "For Docker deployment:"
echo "1. Build and run: docker-compose up --build"
echo "2. Open browser: http://localhost:8501"
echo ""
echo "Happy coding! 🎉"
