from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select
from database import AsyncSessionLocal
from models import User
from handlers.callbacks import USER_STATES

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if USER_STATES.get(user_id) == "WAITING_ID":
        if not text.isdigit():
            await update.message.reply_text("❌ ابعت ID صحيح")
            return

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == int(text))
            )
            user = result.scalar_one_or_none()

        USER_STATES.pop(user_id, None)

        if not user:
            await update.message.reply_text("❌ المستخدم غير موجود")
        else:
            await update.message.reply_text(
                f"""👤 بيانات المستخدم:
🆔 ID: {user.telegram_id}
👤 الاسم: {user.first_name}
📛 يوزرنيم: @{user.username or "لا يوجد"}"""
            )
