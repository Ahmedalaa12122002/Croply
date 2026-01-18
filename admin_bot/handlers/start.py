# admin_bot/handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes
from handlers.permissions import get_user_role
from keyboards.admin_menu import admin_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    role = await get_user_role(user_id)

    if not role:
        await update.message.reply_text("⛔ غير مصرح لك باستخدام هذا البوت")
        return

    await update.message.reply_text(
        f"👑 لوحة تحكم الأدمن\nصلاحيتك: {role}",
        reply_markup=admin_menu()
    )
