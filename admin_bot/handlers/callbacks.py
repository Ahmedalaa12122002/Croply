from telegram import Update
from telegram.ext import ContextTypes

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # إزالة الأزرار القديمة
    await query.edit_message_reply_markup(reply_markup=None)

    if query.data == "latest_users":
        await query.edit_message_text(
            "🆕 أحدث المستخدمين\n\n(سيتم ربطها لاحقًا)"
        )

    elif query.data == "search_user":
        await query.edit_message_text(
            "🔍 البحث عن مستخدم\n\n(سيتم تفعيل البحث لاحقًا)"
        )
