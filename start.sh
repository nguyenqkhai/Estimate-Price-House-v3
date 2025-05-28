#!/bin/bash

# Script để chạy cả Streamlit app và Flask API

# Chạy Flask API ở background (port 5000)
echo "Starting Flask API on port 5000..."
python api.py &

# Chờ một chút để API khởi động
sleep 2

# Chạy Streamlit app (port 8501)
echo "Starting Streamlit app on port 8501..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
