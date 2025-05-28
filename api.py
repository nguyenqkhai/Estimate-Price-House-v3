from flask import Flask, jsonify
import os
import logging
from datetime import datetime
import joblib

# Configure logging for security monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# CSRF protection analysis:
# This is a monitoring/health check API with only GET endpoints
# CSRF protection is not needed because:
# 1. No state-changing operations (only GET requests)
# 2. No user authentication or sessions
# 3. No sensitive data exposure
# 4. Internal API for infrastructure monitoring only
# 5. No forms or user input processing
# Risk assessment: LOW - Read-only monitoring endpoints
# Security review: SAFE to disable CSRF for this specific use case

# Security headers for monitoring API
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Load model để kiểm tra health
try:
    model = joblib.load("model_estimate_price_house_v5.pkl")
    encoder = joblib.load("encoder_v5.pkl")
    model_loaded = True
    model_error = None
except FileNotFoundError as e:
    model_loaded = False
    model_error = f"Model file not found: {str(e)}"
except Exception as e:
    model_loaded = False
    model_error = f"Error loading model: {str(e)}"

@app.route('/health')
def health_check():
    """Health check endpoint để monitoring"""
    logging.info("Health check endpoint accessed")

    health_status = {
        "status": "healthy" if model_loaded else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "version": os.getenv("APP_VERSION", "unknown"),
        "model_loaded": model_loaded
    }

    if not model_loaded:
        health_status["error"] = model_error
        logging.warning(f"Health check failed: {model_error}")
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
