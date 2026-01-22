from telegram import Update
from telegram.ext import ContextTypes
from security import check_access
from permissions import Role
from keyboards.ads_menu import ads_menu, ads_decision

async def ads_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📢 الإعلانات / المهام",
        reply_markup=ads_menu()
    )

async def list_pending_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_access(update.effective_user.id, Role.GOLD):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📄 إعلان #55\nالعنوان: مشاهدة فيديو\nالمكافأة: 2 نقطة",
        reply_markup=ads_decision(55)
    )

async def handle_ads_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    action, ad_id = update.callback_query.data.split(":")
    ad_id = int(ad_id)

    if not check_access(admin_id, Role.PLATINUM):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        f"✅ تم تنفيذ القرار ({action}) على الإعلان #{ad_id}"
    )
    # 📌 لاحقًا: DB + إشعار + Logs
