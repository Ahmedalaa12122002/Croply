from telegram import Update
from telegram.ext import ContextTypes

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "latest_users":
        await query.edit_message_text(
            "🆕 أحدث المستخدمين:\n\n(لسه هنربطها بقاعدة البيانات)"
        )

    elif query.data == "search_user":
        await query.edit_message_text(
            "🔍 ابعت ID المستخدم اللي عايز تبحث عنه:"
        )
