from telegram import Update
from telegram.ext import ContextTypes
from security import check_access
from permissions import Role
from keyboards.points_menu import points_menu, confirm_points

POINTS_STATE = {}

async def points_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "💰 إدارة النقاط",
        reply_markup=points_menu()
    )

async def ask_points_input(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
    admin_id = update.effective_user.id

    required = Role.GOLD if "all" not in action else Role.PLATINUM
    if not check_access(admin_id, required):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    POINTS_STATE[admin_id] = action
    await update.callback_query.answer()
    if "all" in action:
        await update.callback_query.message.reply_text("✍️ اكتب عدد النقاط (سيتم التطبيق على الجميع):")
    else:
        await update.callback_query.message.reply_text("✍️ اكتب: ID عدد_النقاط (مثال: 123456 50)")

async def handle_points_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    action = POINTS_STATE.get(admin_id)
    if not action:
        return

    text = update.message.text.strip().split()
    POINTS_STATE.pop(admin_id, None)

    if "all" in action:
        if not text[0].lstrip("-").isdigit():
            await update.message.reply_text("❌ رقم نقاط غير صحيح")
            return
        amount = int(text[0])
        await update.message.reply_text(
            f"⚠️ تأكيد تنفيذ العملية الجماعية ({amount} نقطة)",
            reply_markup=confirm_points(action, amount, "ALL")
        )
    else:
        if len(text) != 2 or not text[0].isdigit() or not text[1].lstrip("-").isdigit():
            await update.message.reply_text("❌ الصيغة غير صحيحة")
            return
        target_id, amount = int(text[0]), int(text[1])
        await update.message.reply_text(
            f"⚠️ تأكيد العملية على المستخدم {target_id} ({amount} نقطة)",
            reply_markup=confirm_points(action, amount, str(target_id))
        )

async def confirm_points_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    _, action, amount, target = update.callback_query.data.split(":")
    amount = int(amount)

    required = Role.GOLD if target != "ALL" else Role.PLATINUM
    if not check_access(admin_id, required):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        f"✅ تم تنفيذ عملية النقاط ({action}) بقيمة {amount} على {target}"
    )
    # 📌 لاحقًا: تنفيذ DB + إشعار المستخدمين + Admin Logs
