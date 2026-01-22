from telegram import Update
from telegram.ext import ContextTypes
from security import check_access
from permissions import Role
from keyboards.stats_menu import stats_menu, time_filter_menu

STATS_STATE = {}

async def stats_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📊 قسم الإحصائيات",
        reply_markup=stats_menu()
    )

async def global_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_access(update.effective_user.id, Role.GOLD):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📊 اختر المدة:",
        reply_markup=time_filter_menu("global_stats")
    )

async def handle_global_stats_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    period = update.callback_query.data.split(":")[1]
    await update.callback_query.answer()

    # مثال مؤقت – لاحقًا DB
    await update.callback_query.message.reply_text(
        f"""📊 الإحصائيات العامة ({period})
👥 المستخدمين: 1,250
🟢 أونلاين: 120
💰 الأرباح: 320 USDT
📉 الخسائر: 45 USDT
💎 النقاط المكتسبة: 82,000
"""
    )

async def user_stats_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_access(update.effective_user.id, Role.BRONZE):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    STATS_STATE[update.effective_user.id] = "USER_STATS"
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("✍️ اكتب Telegram ID للمستخدم:")

async def handle_user_stats_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    if STATS_STATE.get(admin_id) != "USER_STATS":
        return

    STATS_STATE.pop(admin_id, None)

    if not update.message.text.isdigit():
        await update.message.reply_text("❌ ID غير صحيح")
        return

    user_id = int(update.message.text)
    await update.message.reply_text(
        f"""📈 إحصائيات المستخدم {user_id}
📅 تاريخ التسجيل: —
🕒 آخر دخول: —
💰 إجمالي الأرباح: —
🏦 إجمالي السحب: —
📋 المهام المكتملة: —
"""
  )
