import asyncio
from typing import Optional
from telegram import Update, Sticker
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
from telegram.constants import ParseMode
import config
from logger import setup_logger
from keep_alive import keep_alive
from monitoring import bot_monitor

# Set up logger
logger = setup_logger(__name__)

async def check_admin_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Check if the bot has admin permissions in the group

    Args:
        update: Telegram update object
        context: Callback context

    Returns:
        bool: True if bot has admin permissions, False otherwise
    """
    try:
        chat_id = update.effective_chat.id
        bot_member = await context.bot.get_chat_member(chat_id, context.bot.id)
        return bot_member.can_delete_messages
    except TelegramError as e:
        bot_monitor.log_error(e, "Error checking admin permissions")
        return False

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming sticker messages

    Args:
        update: Telegram update object
        context: Callback context
    """
    try:
        # Update activity timestamp
        bot_monitor.update_activity()

        # Early return if no message or sticker
        if not update.message or not update.message.sticker:
            return

        # Log received message and sticker details
        chat_id = update.effective_chat.id
        sticker: Sticker = update.message.sticker
        set_name = sticker.set_name

        logger.info(f"Processing sticker from set '{set_name}' in chat {chat_id}")

        # Check if sticker is from a banned set first
        if set_name not in config.BANNED_STICKER_SETS:
            logger.debug(f"Sticker set '{set_name}' is not in banned list")
            return

        # Only check permissions if the sticker is from a banned set
        has_permissions = await check_admin_permissions(update, context)
        if not has_permissions:
            logger.warning(f"Bot lacks admin permissions in chat {chat_id}")
            return

        logger.info(f"Attempting to delete sticker from banned set '{set_name}'")

        try:
            # Minimal delay before deletion
            await asyncio.sleep(config.DELETION_DELAY)
            await update.message.delete()

            logger.info(
                f"Successfully deleted sticker message from set '{set_name}' "
                f"in chat {chat_id} sent by user {update.effective_user.id}"
            )

        except TelegramError as e:
            if "Message to delete not found" in str(e):
                logger.warning(f"Message already deleted in chat {chat_id}")
            else:
                bot_monitor.log_error(e, f"Failed to delete message in chat {chat_id}")

    except Exception as e:
        bot_monitor.log_error(e, "Unexpected error in handle_sticker")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot"""
    bot_monitor.log_error(
        context.error,
        f"Update {update} caused error"
    )

def main() -> None:
    """
    Main function to run the bot
    """
    try:
        # Validate configuration
        if not config.TOKEN:
            raise ValueError("Bot token not found in environment variables")

        # Start the web server
        keep_alive()
        logger.info("Web server started")

        # Create application with specific configuration
        application = (
            Application.builder()
            .token(config.TOKEN)
            .concurrent_updates(True)  # Enable concurrent updates
            .build()
        )

        # Add error handler
        application.add_error_handler(error_handler)

        # Add message handler for stickers with high priority
        application.add_handler(
            MessageHandler(
                filters.Sticker.ALL & filters.ChatType.GROUPS,
                handle_sticker,
                block=False  # Non-blocking handler
            )
        )

        # Start the bot
        logger.info("Starting bot...")
        application.run_polling(
            allowed_updates=["message"],  # Only process message updates
            drop_pending_updates=True,    # Ignore updates from when bot was offline
            close_loop=False              # Keep event loop running
        )

    except Exception as e:
        bot_monitor.log_error(e, "Failed to start bot")
        raise

if __name__ == '__main__':
    main()