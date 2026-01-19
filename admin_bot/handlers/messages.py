from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select

from database import AsyncSessionLocal
from models import User

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    state = context.user_data.get("state")
    text = update.message.text.strip()

    if state != "WAITING_ID":
        return

    if not text.isdigit():
        await update.message.reply_text("❌ من فضلك ابعت رقم فقط")
        return

    target_id = int(text)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == target_id)
        )
        user = result.scalar_one_or_none()

    context.user_data.pop("state", None)

    if not user:
        await update.message.reply_text("❌ المستخدم غير موجود في قاعدة البيانات")
        return

    await update.message.reply_text(
        f"""👤 بيانات المستخدم
━━━━━━━━━━━━━━
🆔 ID: {user.telegram_id}
👤 الاسم: {user.first_name or 'غير متوفر'}
📛 اليوزر: @{user.username or 'لا يوجد'}
📅 تاريخ التسجيل: {user.created_at}
"""
    )
