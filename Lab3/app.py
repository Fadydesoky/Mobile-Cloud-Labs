from flask import Flask, request, jsonify
import random
import time
import logging
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# ============================
# Config
# ============================
MAX_DATA_SIZE = int(os.getenv("MAX_DATA_SIZE", 5000))
MIN_DELAY = float(os.getenv("MIN_DELAY", 0.1))
MAX_DELAY = float(os.getenv("MAX_DELAY", 1.5))
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ============================
# Decorator
# ============================
def validate_size(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            size = int(request.args.get("size", 100))
            if size < 1 or size > MAX_DATA_SIZE:
                return jsonify({"error": "invalid size"}), 400
            request.size = size
            return f(*args, **kwargs)
        except ValueError:
            return jsonify({"error": "size must be integer"}), 400
    return wrapper


# ============================
# Routes
# ============================

@app.route("/")
def home():
    delay = round(random.uniform(MIN_DELAY, MAX_DELAY), 2)
    time.sleep(delay)

    return jsonify({
        "message": "Mobile Cloud API",
        "delay": delay,
        "timestamp": datetime.utcnow().isoformat(),
        "env": APP_ENV
    })


@app.route("/data")
@validate_size
def data():
    size = request.size
    data = [random.randint(1, 100) for _ in range(size)]

    return jsonify({
        "count": len(data),
        "sample": data[:5],
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/health")
def health():
    return "ok", 200


@app.route("/status")
def status():
    return jsonify({
        "status": "healthy",
        "env": APP_ENV,
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/metrics")
def metrics():
    return jsonify({
        "max_data_size": MAX_DATA_SIZE,
        "min_delay": MIN_DELAY,
        "max_delay": MAX_DELAY
    })


# ============================
# Errors
# ============================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "internal error"}), 500


# ============================
# Run
# ============================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=(APP_ENV == "development")
    )
