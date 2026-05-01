from flask import Flask, request, jsonify
from PIL import Image
from pathlib import Path

app = Flask(__name__)

@app.route("/resize", methods=["POST"])
def resize():
    event = request.get_json()

    input_path = Path(event["file_path"])
    output_path = Path("/data/output/resized_" + input_path.name)

    with Image.open(input_path) as img:
        img.thumbnail((300, 300))
        img.save(output_path)

    return jsonify({"status": "done", "output": str(output_path)})

app.run(host="0.0.0.0", port=5000)
