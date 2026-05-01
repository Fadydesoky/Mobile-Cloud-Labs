import time
import redis
import os

r = redis.Redis(host="redis", port=6379)

INPUT_FOLDER = "/data/input"

print("📡 Event Source Started...")

while True:
    files = os.listdir(INPUT_FOLDER)
    for f in files:
        event = f"image:{f}"
        r.lpush("events", event)
        print(f"📤 Event sent: {event}")
        time.sleep(2)
    time.sleep(5)
