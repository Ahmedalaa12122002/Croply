
from telegram import Update
from telegram.ext import ContextTypes
from security import check_access
from permissions import Role
from keyboards.finance_menu import finance_menu, decision_menu

async def finance_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🏦 السحب والإيداع",
        reply_markup=finance_menu()
    )

async def list_withdraw_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_access(update.effective_user.id, Role.PLATINUM):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()
    # مثال مؤقت
    await update.callback_query.message.reply_text(
        "📄 طلب سحب #101\nالمستخدم: 123456\nالقيمة: 50 USDT",
        reply_markup=decision_menu("withdraw", 101)
    )

async def handle_finance_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    action, req_id = update.callback_query.data.split(":")
    req_id = int(req_id)

    if not check_access(admin_id, Role.PROFESSOR):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        f"✅ تم تنفيذ القرار ({action}) على الطلب #{req_id}"
    )
    # 📌 لاحقًا: تنفيذ DB + إشعار المستخدم + Admin Logs
