import json
import logging
from simplegmail import Gmail
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from modules.logger import Customlogger, Logger_type



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        Customlogger(True, "[!] Configuration file not found.", logging.ERROR)
        raise
    except json.JSONDecodeError:
        Customlogger(True, "[!] Error decoding JSON from configuration file.", logging.ERROR)
        raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <second> to set a timer")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send a formatted message to a Telegram chat containing details of unread emails for specified email addresses.

    Args:
        context (ContextTypes.DEFAULT_TYPE): An instance of ContextTypes.DEFAULT_TYPE containing job and bot information.
    """
    job = context.job
    for email in email_addresses:
        try:
            messages = gmail.get_unread_inbox(query=email)
            for message in messages:
                msg_text = (
                    f"📧 New Email Received\n\n"
                    f"👤 From: \n{message.sender}\n"
                    f"📝 Subject: \n{message.subject}\n"
                    f"🔍 Preview: \n{message.snippet}\n"
                )
                message.mark_as_read()
                await context.bot.send_message(job.chat_id, text=msg_text)
        except Exception as e:
            await context.bot.send_message(job.chat_id, text=f"Exception occured : {e}")
            Customlogger(True, f"[-] Exception : {e}" , Logger_type.ERROR)
            


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    # Could be specific chat id for security
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <second>")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Remove the job if the user changed their mind.

    Args:
        update (Update): An object containing information about the incoming update (message) from the user.
        context (ContextTypes.DEFAULT_TYPE): An object providing context for the current state of the application, including job queue management.
    """
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


def main() -> None:
    """
    Initializes and runs a Telegram bot application.
    
    The function sets up logging, creates the bot application with a specified token,
    adds command handlers for different bot commands, and starts polling for updates.
    
    """
    
    # Create the Application and pass it your bot's token
    Customlogger(True, "[+] Initial Telegram Bot.", Logger_type.INFO)
    application = Application.builder().token(telegram_token).build()

    # Add command handlers for different bot commands
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    try:
        Customlogger(True, "[+] Bot polling started.", Logger_type.INFO)
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        Customlogger(True, f"Error in bot polling: {e}", Logger_type.ERROR)

if __name__ == "__main__":
    gmail = Gmail()
    Customlogger(True, f"[+] Initial Gmail client.", Logger_type.INFO)
    config = load_config('config.json')
    email_addresses = config["emails"]
    telegram_token = config["telegram"]["bot_token"]
    # telegram_chat_id = config["telegram"]["chat_id"]
    main()