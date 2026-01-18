from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select
from database import AsyncSessionLocal
from models import User
from handlers.permissions import is_admin_or_owner


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تأكيد إن الرسالة نص
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.strip()

    # تحقق صلاحيات
    if not await is_admin_or_owner(user_id):
        return

    # تحقق من الحالة
    state = context.user_data.get("state")

    if state != "WAITING_USER_ID":
        return  # تجاهل أي رسالة خارج السياق

    # تحقق من صحة الـ ID
    if not text.isdigit():
        await update.message.reply_text("❌ من فضلك أرسل ID رقمي صحيح")
        return

    target_id = int(text)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == target_id)
        )
        user = result.scalar_one_or_none()

    # مسح الحالة بعد الاستخدام
    context.user_data.pop("state", None)

    if not user:
        await update.message.reply_text("❌ المستخدم غير موجود في قاعدة البيانات")
        return

    await update.message.reply_text(
        f"""👤 **بيانات المستخدم**
━━━━━━━━━━━━━━
🆔 ID: `{user.telegram_id}`
👤 الاسم: {user.first_name}
📛 اليوزر: @{user.username or "لا يوجد"}
📅 تاريخ التسجيل: {user.created_at}
""",
        parse_mode="Markdown"
                              )
