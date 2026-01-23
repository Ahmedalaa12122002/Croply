from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
from config import BOT_TOKEN
from handlers import start, open_users_menu, ask_user_id, handle_text

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(open_users_menu, pattern="users"))
app.add_handler(CallbackQueryHandler(ask_user_id, pattern="user_check"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

app.run_polling()
