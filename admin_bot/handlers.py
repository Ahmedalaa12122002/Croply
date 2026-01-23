from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID
from keyboards import (
    main_menu, users_menu, points_menu,
    ads_menu, finance_menu, stats_menu,
    admin_menu, permissions_menu
)

# ===== حالات الإدخال =====
USER_STATES = {}
WAITING_USER_ID = "WAITING_USER_ID"
WAITING_RESET_ID = "WAITING_RESET_ID"
WAITING_DELETE_ID = "WAITING_DELETE_ID"

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ هذا بوت أدمن خاص")
        return

    await update.message.reply_text(
        "👑 لوحة تحكم الأدمن",
        reply_markup=main_menu()
    )

# ===== التعامل مع الأزرار =====
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != OWNER_ID:
        await query.edit_message_text("❌ غير مصرح")
        return

    data = query.data
    admin_id = query.from_user.id

    # ---- القوائم ----
    if data == "menu_users":
        await query.edit_message_text("👤 إدارة المستخدمين", reply_markup=users_menu())

    elif data == "menu_points":
        await query.edit_message_text("💰 النقاط / العملات", reply_markup=points_menu())

    elif data == "menu_ads":
        await query.edit_message_text("📢 الإعلانات / المهام", reply_markup=ads_menu())

    elif data == "menu_finance":
        await query.edit_message_text("🏦 السحب / الإيداع", reply_markup=finance_menu())

    elif data == "menu_stats":
        await query.edit_message_text("📊 الإحصائيات", reply_markup=stats_menu())

    elif data == "menu_admin":
        await query.edit_message_text("🛡 بيانات الأدمن", reply_markup=admin_menu())

    elif data == "menu_permissions":
        await query.edit_message_text("⚙️ صلاحيات الأدمن", reply_markup=permissions_menu())

    elif data == "back_main":
        USER_STATES.pop(admin_id, None)
        await query.edit_message_text("👑 لوحة تحكم الأدمن", reply_markup=main_menu())

    # ---- إدارة المستخدمين ----
    elif data == "user_check":
        USER_STATES[admin_id] = WAITING_USER_ID
        await query.edit_message_text("✍️ اكتب Telegram ID للمستخدم:")

    elif data == "user_reset":
        USER_STATES[admin_id] = WAITING_RESET_ID
        await query.edit_message_text("⚠️ اكتب Telegram ID لتصفير بياناته:")

    elif data == "user_delete":
        USER_STATES[admin_id] = WAITING_DELETE_ID
        await query.edit_message_text("❗ اكتب Telegram ID لحذف المستخدم نهائيًا:")

    else:
        await query.answer("🚧 هذه الميزة ستُفعل لاحقًا", show_alert=True)

# ===== استقبال النص =====
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.effective_user.id
    state = USER_STATES.get(admin_id)

    if not state:
        return

    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("❌ من فضلك اكتب Telegram ID صحيح (أرقام فقط)")
        return

    USER_STATES.pop(admin_id)
    telegram_id = int(text)

    # ---- كشف حساب (Mock) ----
    if state == WAITING_USER_ID:
        await update.message.reply_text(
            f"""👤 بيانات المستخدم (تجريبية)
🆔 ID: {telegram_id}
👤 الاسم: Test User
📛 يوزرنيم: @testuser
🟡 الحالة: لم يدخل الويب
💰 النقاط: 0
"""
        )

    # ---- تصفير بيانات (Mock) ----
    elif state == WAITING_RESET_ID:
        await update.message.reply_text(
            f"""🧹 تم تصفير بيانات المستخدم (تجريبيًا)
🆔 ID: {telegram_id}
"""
        )

    # ---- حذف مستخدم (Mock) ----
    elif state == WAITING_DELETE_ID:
        await update.message.reply_text(
            f"""❌ تم حذف المستخدم نهائيًا (تجريبيًا)
🆔 ID: {telegram_id}

⚠️ عند ربط DB سيتم الحذف الحقيقي
"""
        )
