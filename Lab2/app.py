"""
Lab2: Distributed Consistency and Cloud Systems
Redis-based distributed system simulation with error handling
"""

from flask import Flask, jsonify, request
import redis
import logging
import os
from datetime import datetime

# ============================
# Configuration
# ============================
REDIS_PRIMARY_HOST = os.getenv('REDIS_PRIMARY_HOST', 'localhost')
REDIS_PRIMARY_PORT = int(os.getenv('REDIS_PRIMARY_PORT', 6379))
REDIS_REPLICA_HOST = os.getenv('REDIS_REPLICA_HOST', 'localhost')
REDIS_REPLICA_PORT = int(os.getenv('REDIS_REPLICA_PORT', 6380))
REDIS_TIMEOUT = int(os.getenv('REDIS_TIMEOUT', 5))
APP_ENV = os.getenv('APP_ENV', 'development')

app = Flask(__name__)

# ============================
# Logging
# ============================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================
# Redis Connections
# ============================
redis_primary = None
redis_replica = None


def init_redis_connections():
    global redis_primary, redis_replica

    try:
        redis_primary = redis.Redis(
            host=REDIS_PRIMARY_HOST,
            port=REDIS_PRIMARY_PORT,
            socket_connect_timeout=REDIS_TIMEOUT,
            decode_responses=True
        )
        redis_primary.ping()
        logger.info("Connected to PRIMARY Redis")
    except Exception as e:
        logger.warning(f"Primary Redis failed: {e}")
        redis_primary = None

    try:
        redis_replica = redis.Redis(
            host=REDIS_REPLICA_HOST,
            port=REDIS_REPLICA_PORT,
            socket_connect_timeout=REDIS_TIMEOUT,
            decode_responses=True
        )
        redis_replica.ping()
        logger.info("Connected to REPLICA Redis")
    except Exception as e:
        logger.warning(f"Replica Redis failed: {e}")
        redis_replica = None


# ============================
# CORS
# ============================
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# ============================
# Routes
# ============================

@app.route('/')
def home():
    """Basic API info"""
    return jsonify({
        "service": "Redis Distributed System",
        "env": APP_ENV,
        "time": datetime.utcnow().isoformat()
    })


@app.route('/write', methods=['POST', 'GET'])
def write():
    """
    Write data to PRIMARY Redis
    """

    try:
        if request.method == 'POST':
            data = request.get_json() or {}
            key = data.get("key", "test_key")
            value = data.get("value", "hello")
        else:
            key = request.args.get("key", "test_key")
            value = request.args.get("value", "hello")

        if redis_primary:
            redis_primary.set(key, value)
            return jsonify({
                "status": "success",
                "key": key,
                "value": value,
                "node": "primary"
            })
        else:
            return jsonify({"error": "Primary unavailable"}), 503

    except Exception as e:
        logger.error(e)
        return jsonify({"error": "internal error"}), 500


@app.route('/read-primary')
def read_primary():
    """
    Read from PRIMARY Redis
    """

    key = request.args.get("key", "test_key")

    if redis_primary:
        value = redis_primary.get(key)
        return jsonify({
            "source": "primary",
            "key": key,
            "value": value
        })
    else:
        return jsonify({"error": "Primary unavailable"}), 503


@app.route('/read-replica')
def read_replica():
    """
    Read from REPLICA Redis
    """

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
