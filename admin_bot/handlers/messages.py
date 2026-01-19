from telegram import Update
from telegram.ext import ContextTypes

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نتأكد إنها رسالة نصية
    if not update.message or not update.message.text:
        return

    state = context.user_data.get("state")
    text = update.message.text.strip()

    # لو مش في وضع البحث، تجاهل
    if state != "WAITING_ID":
        return

    # تحقق من ID
    if not text.isdigit():
        await update.message.reply_text("❌ من فضلك ابعت رقم فقط")
        return

    # مسح الحالة بعد الاستخدام
    context.user_data.pop("state", None)

    # رد تجريبي (بدون DB)
    await update.message.reply_text(
        f"✅ استلمت ID: {text}\n\n"
        "🔧 سيتم ربط البحث بقاعدة البيانات في الخطوة القادمة"
    )
