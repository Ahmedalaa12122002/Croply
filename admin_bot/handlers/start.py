from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from keyboards.admin_menu import admin_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ هذا البوت مخصص للأدمن فقط")
        return

    await update.message.reply_text(
        "👑 لوحة تحكم الأدمن\nاختر من القائمة:",
        reply_markup=admin_menu()
    )
