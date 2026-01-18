from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN
from handlers.start import start
from handlers.callbacks import admin_callbacks
from handlers.messages import handle_messages


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # أزرار Inline Keyboard (CallbackQuery)
    app.add_handler(CallbackQueryHandler(admin_callbacks))

    # استقبال الرسائل النصية (مثل ID المستخدم)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_messages
        )
    )

    print("👑 Admin Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
