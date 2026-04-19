from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import logging
import os

app = Flask(__name__)
CORS(app)

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Prometheus Metrics
REQUEST_COUNT = Counter('lab3_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('lab3_request_latency_seconds', 'Request latency', ['endpoint'])
ACTIVE_REQUESTS = Gauge('lab3_active_requests', 'Number of active requests')

@app.route("/")
def home():
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)

    logging.info(f"Home endpoint called - delay: {delay:.2f}s")

    return jsonify({
        "message": "Mobile Cloud API",
        "delay": round(delay, 2)
    })

@app.route("/data")
def data():
    size = int(request.args.get("size", 100))
    data = [random.randint(1, 100) for _ in range(size)]

    logging.info(f"Data endpoint called - size: {size}")

    return jsonify({
        "count": len(data),
        "sample": data[:5]
    })

@app.route("/health")
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health', status='200').inc()
    logging.info("Health check endpoint called")
    return jsonify({
        "status": "healthy",
        "service": "lab3-api",
        "version": os.getenv("APP_VERSION", "1.0.0")
    })


@app.route("/ready")
def ready():
    """Readiness probe for Kubernetes"""
    return jsonify({"status": "ready"}), 200


@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
