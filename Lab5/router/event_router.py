import os, json, time, redis, requests

r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

routes = {
    "image.uploaded": [
        "http://image-resizer:5000/resize",
        "http://notifier:5000/notify"
    ]
}

last_id = "0-0"

print("Router started...", flush=True)

while True:
    events = r.xread({"events": last_id}, block=5000)

    for _, msgs in events:
        for msg_id, data in msgs:
            last_id = msg_id

            event = json.loads(data["payload"])
            print("Received:", event, flush=True)

            for url in routes.get(event["event_type"], []):
                try:
                    res = requests.post(url, json=event)
                    print(f"Sent to {url} → {res.status_code}", flush=True)
                except Exception as e:
                    print("Error:", e, flush=True)
