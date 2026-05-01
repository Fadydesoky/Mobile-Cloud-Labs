import os
import json
import time
import uuid
from pathlib import Path
from datetime import datetime
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
WATCH_DIR = Path(os.getenv("WATCH_DIR", "/data/input"))
STREAM_NAME = "events"

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

WATCH_DIR.mkdir(parents=True, exist_ok=True)
seen_files = set()

print(f"Watching folder: {WATCH_DIR}", flush=True)

def is_image(path):
    return path.suffix.lower() in [".png", ".jpg", ".jpeg"]

while True:
    for path in WATCH_DIR.iterdir():
        if path.is_file() and is_image(path) and str(path) not in seen_files:

            event = {
                "event_id": str(uuid.uuid4()),
                "event_type": "image.uploaded",
                "file_name": path.name,
                "file_path": str(path),
                "width": 300,
                "created_at": datetime.now().isoformat()
            }

            r.xadd(STREAM_NAME, {"payload": json.dumps(event)})
            seen_files.add(str(path))

            print("Published event:", event, flush=True)

    time.sleep(2)
