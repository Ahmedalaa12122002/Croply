from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select

from database import AsyncSessionLocal
from models import User
from handlers.callbacks import USER_STATES
from handlers.permissions import get_user_role


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    التعامل مع الرسائل النصية داخل بوت الأدمن
    (مثل إدخال ID المستخدم عند البحث)
    """

    telegram_user_id = update.effective_user.id
    text = update.message.text.strip()

    # 🔐 تحقق من الصلاحيات
    role = await get_user_role(telegram_user_id)
    if not role:
        await update.message.reply_text("⛔ غير مصرح لك باستخدام هذا البوت")
        return

    # 🕒 هل المستخدم في وضع انتظار إدخال ID؟
    if USER_STATES.get(telegram_user_id) != "WAITING_ID":
        # تجاهل أي رسالة عشوائية
        return

    # ✅ التحقق من صحة الـ ID
    if not text.isdigit():
        await update.message.reply_text("❌ من فضلك ابعت Telegram ID صحيح (أرقام فقط)")
        return

    target_user_id = int(text)

    # 🔍 البحث في قاعدة البيانات
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == target_user_id)
        )
        user = result.scalar_one_or_none()

    # 🧹 إزالة حالة الانتظار
    USER_STATES.pop(telegram_user_id, None)

    # ❌ المستخدم غير موجود
    if not user:
        await update.message.reply_text("❌ المستخدم غير موجود في قاعدة البيانات")
        return

    # ✅ عرض بيانات المستخدم
    message = (
        "👤 **بيانات المستخدم**\n\n"
        f"🆔 ID: `{user.telegram_id}`\n"
        f"👤 الاسم: {user.first_name or 'غير متوفر'}\n"
        f"📛 يوزرنيم: @{user.username if user.username else 'لا يوجد'}\n"
        f"📅 تاريخ الانضمام: {user.created_at}\n"
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown"
    )
