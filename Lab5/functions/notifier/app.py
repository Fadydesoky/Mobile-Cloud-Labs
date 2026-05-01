"""
Notifier Function Service
Logs notifications for processed events in the pipeline.
"""

import sys
import logging
from datetime import datetime

from flask import Flask, request, jsonify

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Track notification statistics
notification_count = 0


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "notifier",
        "notifications_sent": notification_count,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/notify", methods=["POST"])
def notify():
    """
    Handle notification for processed events.
    
    Expected JSON payload:
    {
        "event_id": "uuid",
        "event_type": "image.uploaded",
        "file_name": "image.jpg",
        "file_path": "/data/input/image.jpg",
        "created_at": "ISO timestamp"
    }
    """
    global notification_count
    
    try:
        event = request.get_json()
        
        if not event:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        notification_count += 1
        
        logger.info("=" * 50)
        logger.info(f"NOTIFICATION #{notification_count}")
        logger.info("-" * 50)
        logger.info(f"  Event ID: {event.get('event_id', 'N/A')}")
        logger.info(f"  Event Type: {event.get('event_type', 'N/A')}")
        logger.info(f"  File: {event.get('file_name', 'N/A')}")
        logger.info(f"  Path: {event.get('file_path', 'N/A')}")
        logger.info(f"  Event Created: {event.get('created_at', 'N/A')}")
        logger.info(f"  Notified At: {datetime.now().isoformat()}")
        logger.info("=" * 50)
        
        return jsonify({
            "status": "notified",
            "notification_id": notification_count,
            "event_id": event.get("event_id"),
            "message": f"Notification sent for {event.get('file_name', 'unknown file')}",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing notification: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("NOTIFIER Service Starting")
    logger.info("=" * 50)
    
    app.run(host="0.0.0.0", port=5000, debug=False)
