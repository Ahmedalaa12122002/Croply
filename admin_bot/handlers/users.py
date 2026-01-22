from telegram import Update
from telegram.ext import ContextTypes
from security import check_access
from permissions import Role
from keyboards.users_menu import users_menu, confirm_menu

# حالة انتظار إدخال ID
USER_STATES = {}

async def users_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "👤 إدارة المستخدمين",
        reply_markup=users_menu()
    )

async def ask_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
    user_id = update.effective_user.id
    if not check_access(user_id, Role.GOLD if action != "lookup" else Role.BRONZE):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    USER_STATES[user_id] = action
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("✍️ من فضلك اكتب Telegram ID للمستخدم:")

async def handle_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    state = USER_STATES.get(admin_id)
    if not state:
        return

    text = update.message.text.strip()
    if not text.isdigit():
        await update.message.reply_text("❌ ID غير صحيح، أرسل أرقام فقط.")
        return

    target_id = int(text)
    USER_STATES.pop(admin_id, None)

    # 👇 هنا سنربط DB لاحقًا – الآن رسالة توضيحية
    if state == "lookup":
        await update.message.reply_text(
            f"""📄 كشف حساب المستخدم
🆔 ID: {target_id}
📅 تاريخ التسجيل: —
🕒 آخر دخول: —
💰 النقاط: —
📌 الحالة: نشط
"""
        )

    elif state == "reset":
        await update.message.reply_text(
            f"⚠️ هل أنت متأكد من تصفير حساب المستخدم {target_id}؟",
            reply_markup=confirm_menu("reset", target_id)
        )

    elif state == "delete":
        await update.message.reply_text(
            f"🚨 تحذير نهائي!\nسيتم حذف المستخدم {target_id} نهائيًا.",
            reply_markup=confirm_menu("delete", target_id)
        )

async def confirm_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    data = update.callback_query.data.split(":")
    action, target_id = data[1], int(data[2])

    required_role = Role.PLATINUM if action == "delete" else Role.GOLD
    if not check_access(admin_id, required_role):
        await update.callback_query.answer("❌ ليس لديك صلاحية", show_alert=True)
        return

    await update.callback_query.answer()

    if action == "reset":
        await update.callback_query.message.reply_text(
            f"✅ تم تصفير حساب المستخدم {target_id} بنجاح"
        )
    elif action == "delete":
        await update.callback_query.message.reply_text(
            f"🗑️ تم حذف المستخدم {target_id} نهائيًا"
        )

    # 📌 لاحقًا: تسجيل العملية في Admin Logs

async def cancel_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("❌ تم إلغاء العملية.")
