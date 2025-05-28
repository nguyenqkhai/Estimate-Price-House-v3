from flask import Flask, jsonify
import os
from datetime import datetime
import joblib
import pandas as pd

app = Flask(__name__)

# Load model để kiểm tra health
try:
    model = joblib.load("model_estimate_price_house_v5.pkl")
    encoder = joblib.load("encoder_v5.pkl")
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

@app.route('/health')
def health_check():
    """Health check endpoint để monitoring"""
    health_status = {
        "status": "healthy" if model_loaded else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "version": os.getenv("APP_VERSION", "unknown"),
        "model_loaded": model_loaded
    }
    
    if not model_loaded:
        health_status["error"] = model_error
        return jsonify(health_status), 500
    
    return jsonify(health_status), 200

@app.route('/metrics')
def metrics():
    """Metrics endpoint cho monitoring"""
    return jsonify({
        "app_info": {
            "name": "house-price-estimator",
            "version": os.getenv("APP_VERSION", "unknown"),
            "uptime": "placeholder_for_uptime_calculation"
        },
        "model_info": {
            "model_loaded": model_loaded,
            "model_file": "model_estimate_price_house_v5.pkl",
            "encoder_file": "encoder_v5.pkl"
        },
        "system_info": {
            "python_version": "3.9",
            "timestamp": datetime.now().isoformat()
        }
    }), 200

@app.route('/ready')
def readiness_check():
    """Readiness check cho Kubernetes/ECS"""
    if model_loaded:
        return jsonify({"status": "ready"}), 200
    else:
        return jsonify({"status": "not ready", "reason": "model not loaded"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
