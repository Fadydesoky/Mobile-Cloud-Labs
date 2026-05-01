"""
Event Source - File Watcher Service
Monitors the input directory for new images and publishes events to Redis.
"""

import os
import sys
import json
import time
import uuid
import logging
from pathlib import Path
from datetime import datetime

import redis

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
WATCH_DIR = Path(os.getenv("WATCH_DIR", "/data/input"))
STREAM_NAME = "events"
POLL_INTERVAL = 2  # seconds

# Supported image extensions
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def connect_to_redis(max_retries: int = 10, retry_delay: int = 2) -> redis.Redis:
    """Connect to Redis with retry logic."""
    for attempt in range(max_retries):
        try:
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True,
                socket_connect_timeout=5
            )
            client.ping()
            logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return client
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    logger.error("Failed to connect to Redis after maximum retries")
    sys.exit(1)


def is_image(path: Path) -> bool:
    """Check if the file is a supported image format."""
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def create_event(file_path: Path) -> dict:
    """Create an event payload for a new image."""
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "image.uploaded",
        "file_name": file_path.name,
        "file_path": str(file_path),
        "target_width": 300,
        "created_at": datetime.now().isoformat()
    }


def publish_event(redis_client: redis.Redis, event: dict) -> str:
    """Publish an event to the Redis stream."""
    message_id = redis_client.xadd(STREAM_NAME, {"payload": json.dumps(event)})
    return message_id


def main():
    """Main watcher loop."""
    logger.info("=" * 50)
    logger.info("EVENT SOURCE - File Watcher Service Starting")
    logger.info("=" * 50)
    
    # Ensure watch directory exists
    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Watching directory: {WATCH_DIR}")
    logger.info(f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
    
    # Connect to Redis
    redis_client = connect_to_redis()
    
    # Track seen files to avoid duplicate processing
    seen_files: set = set()
    
    # Initial scan to avoid processing existing files
    for path in WATCH_DIR.iterdir():
        if path.is_file() and is_image(path):
            seen_files.add(str(path))
            logger.info(f"Skipping existing file: {path.name}")
    
    logger.info(f"Watcher ready. Polling every {POLL_INTERVAL} seconds...")
    logger.info("-" * 50)
    
    while True:
        try:
            for path in WATCH_DIR.iterdir():
                if path.is_file() and is_image(path) and str(path) not in seen_files:
                    logger.info(f"New image detected: {path.name}")
                    
                    # Create and publish event
                    event = create_event(path)
                    message_id = publish_event(redis_client, event)
                    seen_files.add(str(path))
                    
                    logger.info(f"Event published: {event['event_type']}")
                    logger.info(f"  Event ID: {event['event_id']}")
                    logger.info(f"  Message ID: {message_id}")
                    logger.info(f"  File: {event['file_name']}")
                    logger.info("-" * 50)
            
            time.sleep(POLL_INTERVAL)
            
        except redis.ConnectionError as e:
            logger.error(f"Redis connection lost: {e}")
            logger.info("Attempting to reconnect...")
            redis_client = connect_to_redis()
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
