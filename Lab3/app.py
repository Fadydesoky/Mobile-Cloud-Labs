from flask import Flask, request, jsonify
import time
import random
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    logging.info("Health check endpoint called")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
