import redis
import time

r = redis.Redis(host="redis", port=6379)

print("🔀 Event Router Started...")

while True:
    event = r.brpop("events", timeout=5)
    if event:
        event_data = event[1].decode()
        print(f"➡️ Routing event: {event_data}")

        r.lpush("resize_queue", event_data)
        r.lpush("notify_queue", event_data)
