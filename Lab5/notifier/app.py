from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/notify", methods=["POST"])
def notify():
    event = request.get_json()

    print("NOTIFY:", event, flush=True)

    return jsonify({
        "status": "notified",
        "time": datetime.now().isoformat()
    })

app.run(host="0.0.0.0", port=5000)
