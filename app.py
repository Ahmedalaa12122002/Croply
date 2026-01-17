import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 فتح الويب",
                web_app={"url": APP_URL}
            )
        ]
    ]

    update.message.reply_text(
        "👋 أهلاً بك!\nاضغط على الزر لفتح الويب 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("✅ Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
