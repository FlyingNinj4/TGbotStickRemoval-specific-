import os
from typing import List

# Bot configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    print("⚠️ TELEGRAM_BOT_TOKEN not found in environment variables!")
    print("Please set it using: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
    print("You can get a bot token from @BotFather on Telegram")

# List of banned sticker sets
# Add sticker set names here (format: username_by_botname)
BANNED_STICKER_SETS: List[str] = [
    "t_me_gfjojnlo_by_fStikBot"  # Example banned sticker set
]

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Message deletion delay (in seconds)
DELETION_DELAY = 0.1

# Optional Twilio configuration for SMS alerts
# Only used if all variables are set
TWILIO_ENABLED = all([
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN'),
    os.getenv('TWILIO_PHONE_NUMBER'),
    os.getenv('ADMIN_PHONE_NUMBER')
])