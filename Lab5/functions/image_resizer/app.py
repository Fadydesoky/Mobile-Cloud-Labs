"""
Image Resizer Function Service
Processes images by resizing them to specified dimensions.
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

from flask import Flask, request, jsonify
from PIL import Image

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
OUTPUT_DIR = Path("/data/output")
DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "image-resizer",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/resize", methods=["POST"])
def resize():
    """
    Resize an image to the specified dimensions.
    
    Expected JSON payload:
    {
        "event_id": "uuid",
        "event_type": "image.uploaded",
        "file_name": "image.jpg",
        "file_path": "/data/input/image.jpg",
        "target_width": 300  (optional)
    }
    """
    try:
        event = request.get_json()
        
        if not event:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        file_path = event.get("file_path")
        file_name = event.get("file_name")
        target_width = event.get("target_width", DEFAULT_WIDTH)
        
        if not file_path:
            return jsonify({"error": "file_path is required"}), 400
        
        input_path = Path(file_path)
        
        if not input_path.exists():
            logger.error(f"Input file not found: {input_path}")
            return jsonify({"error": f"File not found: {file_path}"}), 404
        
        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        output_filename = f"resized_{input_path.name}"
        output_path = OUTPUT_DIR / output_filename
        
        logger.info(f"Processing image: {file_name}")
        logger.info(f"  Input: {input_path}")
        logger.info(f"  Output: {output_path}")
        
        # Open and resize the image
        with Image.open(input_path) as img:
            original_size = img.size
            
            # Calculate new dimensions maintaining aspect ratio
            ratio = target_width / img.width
            target_height = int(img.height * ratio)
            
            # Resize using high-quality resampling
            resized_img = img.resize(
                (target_width, target_height),
                Image.Resampling.LANCZOS
            )
            
            # Save the resized image
            resized_img.save(output_path, quality=95)
            
            new_size = (target_width, target_height)
        
        logger.info(f"  Original size: {original_size[0]}x{original_size[1]}")
        logger.info(f"  New size: {new_size[0]}x{new_size[1]}")
        logger.info(f"  Status: SUCCESS")
        
        return jsonify({
            "status": "success",
            "event_id": event.get("event_id"),
            "input_file": str(input_path),
            "output_file": str(output_path),
            "original_size": {"width": original_size[0], "height": original_size[1]},
            "new_size": {"width": new_size[0], "height": new_size[1]},
            "processed_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("IMAGE RESIZER Service Starting")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    logger.info("=" * 50)
    
    app.run(host="0.0.0.0", port=5000, debug=False)
