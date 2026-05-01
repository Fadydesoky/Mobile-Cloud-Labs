import redis
from PIL import Image
import os

r = redis.Redis(host="redis", port=6379)

INPUT = "/data/input"
OUTPUT = "/data/output"

print("🖼️ Image Resizer Started...")

while True:
    event = r.brpop("resize_queue", timeout=5)
    if event:
        file_name = event[1].decode().split(":")[1]
        input_path = f"{INPUT}/{file_name}"
        output_path = f"{OUTPUT}/resized_{file_name}"

        try:
            img = Image.open(input_path)
            img = img.resize((200, 200))
            img.save(output_path)

            print(f"✅ Image resized: {output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")
