"""
Event Router Service
Consumes events from Redis and routes them to appropriate function services.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime

import redis
import requests

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
IMAGE_RESIZER_URL = os.getenv("IMAGE_RESIZER_URL", "http://image-resizer:5000")
NOTIFIER_URL = os.getenv("NOTIFIER_URL", "http://notifier:5000")
STREAM_NAME = "events"
CONSUMER_GROUP = "router-group"
CONSUMER_NAME = "router-1"

# Event routing configuration
ROUTES = {
    "image.uploaded": [
        {"name": "image-resizer", "url": f"{IMAGE_RESIZER_URL}/resize"},
        {"name": "notifier", "url": f"{NOTIFIER_URL}/notify"}
    ]
}


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


def setup_consumer_group(redis_client: redis.Redis) -> None:
    """Create the consumer group if it doesn't exist."""
    try:
        redis_client.xgroup_create(STREAM_NAME, CONSUMER_GROUP, id="0", mkstream=True)
        logger.info(f"Created consumer group: {CONSUMER_GROUP}")
    except redis.ResponseError as e:
        if "BUSYGROUP" in str(e):
            logger.info(f"Consumer group already exists: {CONSUMER_GROUP}")
        else:
            raise


def route_event(event: dict) -> list:
    """Route an event to the appropriate services."""
    event_type = event.get("event_type")
    routes = ROUTES.get(event_type, [])
    results = []
    
    for route in routes:
        service_name = route["name"]
        url = route["url"]
        
        try:
            logger.info(f"Routing to {service_name}: {url}")
            response = requests.post(url, json=event, timeout=30)
            
            result = {
                "service": service_name,
                "status_code": response.status_code,
                "success": response.ok,
                "response": response.json() if response.ok else None
            }
            
            if response.ok:
                logger.info(f"  SUCCESS: {service_name} responded with {response.status_code}")
            else:
                logger.warning(f"  FAILED: {service_name} responded with {response.status_code}")
                
        except requests.Timeout:
            logger.error(f"  TIMEOUT: {service_name} did not respond in time")
            result = {"service": service_name, "success": False, "error": "timeout"}
        except requests.RequestException as e:
            logger.error(f"  ERROR: {service_name} - {str(e)}")
            result = {"service": service_name, "success": False, "error": str(e)}
        
        results.append(result)
    
    return results


def process_message(redis_client: redis.Redis, message_id: str, data: dict) -> None:
    """Process a single message from the stream."""
    try:
        event = json.loads(data.get("payload", "{}"))
        
        logger.info("=" * 50)
        logger.info(f"PROCESSING EVENT")
        logger.info(f"  Message ID: {message_id}")
        logger.info(f"  Event Type: {event.get('event_type')}")
        logger.info(f"  Event ID: {event.get('event_id')}")
        logger.info(f"  File: {event.get('file_name')}")
        logger.info("-" * 50)
        
        # Route the event to appropriate services
        results = route_event(event)
        
        # Acknowledge the message
        redis_client.xack(STREAM_NAME, CONSUMER_GROUP, message_id)
        
        # Log summary
        success_count = sum(1 for r in results if r.get("success"))
        logger.info(f"Event processed: {success_count}/{len(results)} services succeeded")
        logger.info("=" * 50)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in message {message_id}: {e}")
        redis_client.xack(STREAM_NAME, CONSUMER_GROUP, message_id)
    except Exception as e:
        logger.error(f"Error processing message {message_id}: {e}")


def main():
    """Main router loop."""
    logger.info("=" * 50)
    logger.info("EVENT ROUTER Service Starting")
    logger.info("=" * 50)
    
    # Connect to Redis
    redis_client = connect_to_redis()
    
    # Setup consumer group
    setup_consumer_group(redis_client)
    
    logger.info(f"Listening on stream: {STREAM_NAME}")
    logger.info(f"Routes configured: {list(ROUTES.keys())}")
    logger.info("-" * 50)
    
    while True:
        try:
            # Read new messages from the stream
            messages = redis_client.xreadgroup(
                CONSUMER_GROUP,
                CONSUMER_NAME,
                {STREAM_NAME: ">"},
                count=1,
                block=5000  # Block for 5 seconds
            )
            
            for stream, stream_messages in messages:
                for message_id, data in stream_messages:
                    process_message(redis_client, message_id, data)
                    
        except redis.ConnectionError as e:
            logger.error(f"Redis connection lost: {e}")
            logger.info("Attempting to reconnect...")
            redis_client = connect_to_redis()
            setup_consumer_group(redis_client)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
