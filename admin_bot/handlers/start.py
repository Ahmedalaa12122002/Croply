# handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes
from security import is_admin
from keyboards.main_menu import main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("❌ هذا بوت أدمن خاص")
        return

    await update.message.reply_text(
        "👑 مرحبًا بك في لوحة تحكم الأدمن",
        reply_markup=main_menu(user_id)
    )
