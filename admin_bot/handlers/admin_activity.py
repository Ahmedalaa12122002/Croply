from telegram import Update
from telegram.ext import ContextTypes
from security import check_access
from permissions import Role
from keyboards.stats_menu import time_filter_menu

async def admin_activity_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_access(update.effective_user.id, Role.PROFESSOR):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🧾 اختر مدة سجل نشاط الأدمن:",
        reply_markup=time_filter_menu("admin_logs")
    )

async def handle_admin_logs_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    period = update.callback_query.data.split(":")[1]
    await update.callback_query.answer()

    # مثال مؤقت
    await update.callback_query.message.reply_text(
        f"""🧾 سجل نشاط الأدمن ({period})
👤 أدمن: 5102387551
🔧 العملية: إضافة نقاط
🎯 المستخدم: 123456
🕒 الوقت: قبل 2 ساعة
"""
    )
