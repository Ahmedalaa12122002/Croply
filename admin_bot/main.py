from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from config import BOT_TOKEN
from handlers.start import start
from handlers.callbacks import admin_callbacks

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(admin_callbacks))  # ⭐ المهم

    print("👑 Admin Bot is running")
    app.run_polling()

if __name__ == "__main__":
    main()
