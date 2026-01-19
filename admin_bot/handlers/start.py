from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆕 أحدث المستخدمين", callback_data="latest_users")],
        [InlineKeyboardButton("🔍 البحث عن مستخدم", callback_data="search_user")]
    ]

    await update.message.reply_text(
        "👑 لوحة تحكم الأدمن\nاختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
