from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.start import start
from handlers.users import (
    users_entry, ask_user_id, handle_user_id,
    confirm_action, cancel_action
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # إدارة المستخدمين
    app.add_handler(CallbackQueryHandler(users_entry, pattern="users"))
    app.add_handler(CallbackQueryHandler(lambda u, c: ask_user_id(u, c, "lookup"), pattern="user_lookup"))
    app.add_handler(CallbackQueryHandler(lambda u, c: ask_user_id(u, c, "reset"), pattern="user_reset"))
    app.add_handler(CallbackQueryHandler(lambda u, c: ask_user_id(u, c, "delete"), pattern="user_delete"))

    app.add_handler(CallbackQueryHandler(confirm_action, pattern="^confirm:"))
    app.add_handler(CallbackQueryHandler(cancel_action, pattern="cancel"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_id))

    app.run_polling()

if __name__ == "__main__":
    main()
