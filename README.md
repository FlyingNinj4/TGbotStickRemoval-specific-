# Telegram Sticker Removal Bot

A Telegram Bot that automatically removes messages containing stickers from specified sticker packs in group chats.

## Quick Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Set your Telegram bot token:
```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

3. Run the bot:
```bash
python bot.py
```

## Configuration

- Add banned sticker sets in `config.py`
- Optional: Configure SMS alerts by setting Twilio environment variables
- See `DEPLOY_GUIDE.md` for detailed setup instructions

## Requirements

- Python 3.7+
- python-telegram-bot library
- Additional requirements in requirements.txt

## Monitoring

Access bot status at:
- http://localhost:5000/ (detailed status)
- http://localhost:5000/ping (health check)

## Need Help?

- See `DEPLOY_GUIDE.md` for deployment instructions
- Contact the bot creator for support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.