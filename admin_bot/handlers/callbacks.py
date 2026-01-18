from telegram import Update
from telegram.ext import ContextTypes
from database import AsyncSessionLocal
from sqlalchemy import select
from models import User

# تخزين حالة البحث
USER_STATES = {}

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 🧹 امسح الأزرار القديمة
    await query.edit_message_reply_markup(reply_markup=None)

    if query.data == "latest_users":
        await query.edit_message_text(
            "🆕 أحدث المستخدمين:\n\n(سيتم ربطها بقاعدة البيانات)"
        )

    elif query.data == "search_user":
        USER_STATES[query.from_user.id] = "WAITING_ID"
        await query.edit_message_text(
            "🔍 ابعت ID المستخدم اللي عايز تبحث عنه:"
        )
