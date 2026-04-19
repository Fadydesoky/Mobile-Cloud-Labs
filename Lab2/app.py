from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.route("/")
def home():
    return jsonify({"message": "Lab2 working"})

@app.route("/write", methods=["POST"])
def write():
    data = request.get_json()
    redis_client.set(data["key"], data["value"])
    return jsonify({"status": "ok"})

@app.route("/read")
def read():
    key = request.args.get("key")
    value = redis_client.get(key)
    return jsonify({"value": value})

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
