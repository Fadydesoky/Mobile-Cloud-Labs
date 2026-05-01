import redis

r = redis.Redis(host="redis", port=6379)

print("🔔 Notifier Started...")

while True:
    event = r.brpop("notify_queue", timeout=5)
    if event:
        print(f"📢 Notification: processed {event[1].decode()}")
