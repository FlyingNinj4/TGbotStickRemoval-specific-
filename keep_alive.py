from flask import Flask, jsonify
from threading import Thread
import logging
from datetime import datetime
import psutil
import os

app = Flask('sticker-removal-bot')
logger = logging.getLogger(__name__)
start_time = datetime.now()

@app.route('/')
def home():
    """Returns bot status information"""
    memory = psutil.Process(os.getpid()).memory_info()
    uptime = datetime.now() - start_time

    return jsonify({
        "status": "Bot is running",
        "uptime": str(uptime),
        "started_at": start_time.isoformat(),
        "memory_usage_mb": round(memory.rss / 1024 / 1024, 2)
    })

@app.route('/ping')
def ping():
    """Simple health check endpoint"""
    return "OK", 200

def run():
    """Runs the Flask app on port 5000"""
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Failed to start monitoring server: {e}")

def keep_alive():
    """Starts the monitoring server in a separate thread"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    logger.info("Monitoring server started on port 5000")