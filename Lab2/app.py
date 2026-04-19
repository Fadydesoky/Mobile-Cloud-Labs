from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

REDIS_REPLICA_HOST = os.getenv("REDIS_REPLICA_HOST", "localhost")
REDIS_REPLICA_PORT = int(os.getenv("REDIS_REPLICA_PORT", 6380))

redis_primary = None
redis_replica = None


def init_redis_connections():
    global redis_primary, redis_replica

    try:
        redis_primary = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        redis_primary.ping()
    except:
        redis_primary = None

    try:
        redis_replica = redis.Redis(host=REDIS_REPLICA_HOST, port=REDIS_REPLICA_PORT, decode_responses=True)
        redis_replica.ping()
    except:
        redis_replica = None


@app.route("/")
def home():
    return jsonify({"message": "Lab2 API working"})


@app.route("/write", methods=["POST"])
def write():
    data = request.get_json()

    if not data or "key" not in data or "value" not in data:
        return jsonify({"error": "Missing key/value"}), 400

    if not redis_primary:
        return jsonify({"error": "Primary unavailable"}), 503

    redis_primary.set(data["key"], data["value"])

    return jsonify({"status": "written"})


@app.route("/read")
def read():
    key = request.args.get("key", "test")

    if not redis_primary:
        return jsonify({"error": "Primary unavailable"}), 503

    value = redis_primary.get(key)

    return jsonify({"key": key, "value": value})


@app.route("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    init_redis_connections()
    app.run(host="0.0.0.0", port=5001)    return "ok", 200


# ----------------------------
# READY (for K8s)
# ----------------------------
@app.route("/ready")
def ready():
    if redis_primary:
        try:
            redis_primary.ping()
            return "ready", 200
        except:
            return "not ready", 503

    return "not ready", 503


# ============================
# MAIN
# ============================

if __name__ == "__main__":
    init_redis_connections()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
