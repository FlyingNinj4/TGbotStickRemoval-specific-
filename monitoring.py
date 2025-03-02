import os
from datetime import datetime
from typing import Optional
from logger import setup_logger
import config

# Set up logger
logger = setup_logger(__name__)

class BotMonitor:
    def __init__(self):
        self.last_activity = datetime.now()
        self.error_count = 0
        self.max_errors = 5
        self.error_window = 300  # 5 minutes

        if config.TWILIO_ENABLED:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(
                    os.getenv('TWILIO_ACCOUNT_SID'),
                    os.getenv('TWILIO_AUTH_TOKEN')
                )
                logger.info("SMS notifications enabled")
            except ImportError:
                logger.warning("Twilio package not installed. SMS notifications disabled.")
                config.TWILIO_ENABLED = False
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                config.TWILIO_ENABLED = False

    def update_activity(self):
        """Update the last activity timestamp"""
        self.last_activity = datetime.now()
        self.error_count = 0

    def log_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Log an error and optionally send SMS notification"""
        self.error_count += 1
        error_msg = f"Error: {str(error)}"
        if context:
            error_msg = f"{context}: {error_msg}"

        logger.error(error_msg, exc_info=True)

        if self.error_count >= self.max_errors and config.TWILIO_ENABLED:
            self._send_alert(f"Critical: Bot experiencing high error rate\n{error_msg}")
            self.error_count = 0

    def _send_alert(self, message: str) -> None:
        """Send alert via Twilio SMS if configured"""
        if not config.TWILIO_ENABLED:
            return

        try:
            self.twilio_client.messages.create(
                body=message,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                to=os.getenv('ADMIN_PHONE_NUMBER')
            )
            logger.info("Alert SMS sent successfully")
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")

# Create global monitor instance
bot_monitor = BotMonitor()