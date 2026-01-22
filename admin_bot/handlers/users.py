from telegram import Update
from telegram.ext import ContextTypes
from security import check_access
from permissions import Role
from keyboards.users_menu import users_menu, confirm_menu

USER_STATES = {}

async def users_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "👤 إدارة المستخدمين",
        reply_markup=users_menu()
    )

async def ask_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
    admin_id = update.effective_user.id
    role = Role.GOLD if action != "lookup" else Role.BRONZE

    if not check_access(admin_id, role):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    USER_STATES[admin_id] = action
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("✍️ اكتب Telegram ID للمستخدم:")

async def handle_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    action = USER_STATES.pop(admin_id, None)
    if not action:
        return

    if not update.message.text.isdigit():
        await update.message.reply_text("❌ ID غير صحيح")
        return

    target_id = int(update.message.text)

    if action == "lookup":
        await update.message.reply_text(
            f"📄 كشف حساب المستخدم\n🆔 ID: {target_id}\n💰 النقاط: —\n📌 الحالة: نشط"
        )
    else:
        await update.message.reply_text(
            f"⚠️ تأكيد العملية على المستخدم {target_id}",
            reply_markup=confirm_menu(action, target_id)
        )

async def confirm_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("✅ تم تنفيذ العملية")

async def cancel_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("❌ تم الإلغاء")
