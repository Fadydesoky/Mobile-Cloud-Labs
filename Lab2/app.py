from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

# ============================
# Redis Configuration
# ============================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

REDIS_REPLICA_HOST = os.getenv("REDIS_REPLICA_HOST", "localhost")
REDIS_REPLICA_PORT = int(os.getenv("REDIS_REPLICA_PORT", 6380))

redis_primary = None
redis_replica = None


def init_redis_connections():
    global redis_primary, redis_replica

    try:
        redis_primary = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
        redis_primary.ping()
        print("✅ Connected to PRIMARY Redis")

    except Exception as e:
        print("❌ Primary Redis failed:", e)
        redis_primary = None

    try:
        redis_replica = redis.Redis(
            host=REDIS_REPLICA_HOST,
            port=REDIS_REPLICA_PORT,
            decode_responses=True
        )
        redis_replica.ping()
        print("✅ Connected to REPLICA Redis")

    except Exception as e:
        print("❌ Replica Redis failed:", e)
        redis_replica = None


# ============================
# Routes
# ============================

@app.route("/")
def home():
    return jsonify({
        "message": "Mobile Cloud Lab2 API",
        "status": "running"
    })


# ----------------------------
# WRITE (Primary)
# ----------------------------
@app.route("/write", methods=["POST"])
def write():
    """
    Write data to PRIMARY Redis
    """
    data = request.get_json()

    if not data or "key" not in data or "value" not in data:
        return jsonify({"error": "Missing key or value"}), 400

    if not redis_primary:
        return jsonify({"error": "Primary unavailable"}), 503

    key = data["key"]
    value = data["value"]

    redis_primary.set(key, value)

    return jsonify({
        "message": "Written to primary",
        "key": key,
        "value": value
    })


# ----------------------------
# READ (Primary)
# ----------------------------
@app.route("/read")
def read():
    """
    Read from PRIMARY Redis
    """
    key = request.args.get("key", "test_key")

    if not redis_primary:
        return jsonify({"error": "Primary unavailable"}), 503

    value = redis_primary.get(key)

    return jsonify({
        "source": "primary",
        "key": key,
        "value": value
    })


# ----------------------------
# READ (Replica)
# ----------------------------
@app.route("/read-replica")
def read_replica():
    """
    Read from REPLICA Redis (eventual consistency)
    """
    key = request.args.get("key", "test_key")

    if not redis_replica:
        return jsonify({"error": "Replica unavailable"}), 503

    value = redis_replica.get(key)

    return jsonify({
        "source": "replica",
        "key": key,
        "value": value,
        "note": "eventual consistency"
    })


# ----------------------------
# STATUS
# ----------------------------
@app.route("/status")
def status():
    """
    Check Redis health
    """

    def check(r):
        try:
            r.ping()
            return "healthy"
        except:
            return "down"

    return jsonify({
        "primary": check(redis_primary) if redis_primary else "missing",
        "replica": check(redis_replica) if redis_replica else "missing"
    })


# ----------------------------
# HEALTH (for Docker/K8s)
# ----------------------------
@app.route("/health")
def health():
    return "ok", 200


# ----------------------------
# READY (important for K8s)
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
# Main
# ============================

if __name__ == "__main__":
    init_redis_connections()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
    key = request.args.get("key", "test_key")

    if redis_replica:
        value = redis_replica.get(key)
        return jsonify({
            "source": "replica",
            "key": key,
            "value": value,
            "note": "eventual consistency"
        })
    else:
        return jsonify({"error": "Replica unavailable"}), 503


@app.route('/status')
def status():
    """
    Check system status
    """

    def check(r):
        try:
            r.ping()
            return "healthy"
        except:
            return "down"

    return jsonify({
        "primary": check(redis_primary) if redis_primary else "missing",
        "replica": check(redis_replica) if redis_replica else "missing"
    })


@app.route('/health')
def health():
    return "ok", 200


@app.route('/ready')
def ready():
    if redis_primary:
        try:
            redis_primary.ping()
            return "ready", 200
        except:
            return "not ready", 503
    return "not ready", 503


# ============================
# Main
# ============================
if __name__ == '__main__':
    init_redis_connections()

    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
