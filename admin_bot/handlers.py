from telegram import Update
from telegram.ext import ContextTypes
from keyboards import MAIN_MENU, USERS_MENU
from api_client import get_user

USER_STATE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 5102387551:
        await update.message.reply_text("❌ بوت أدمن خاص")
        return

    await update.message.reply_text(
        "👑 لوحة تحكم الأدمن",
        reply_markup=MAIN_MENU
    )

async def open_users_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "👤 إدارة المستخدمين",
        reply_markup=USERS_MENU
    )

async def ask_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_STATE[update.effective_user.id] = "WAIT_ID"
    await update.callback_query.edit_message_text("✍️ اكتب Telegram ID:")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if USER_STATE.get(update.effective_user.id) != "WAIT_ID":
        return

    USER_STATE.pop(update.effective_user.id)

    if not update.message.text.isdigit():
        await update.message.reply_text("❌ ID غير صحيح")
        return

    data = get_user(int(update.message.text))

    if not data["exists"]:
        await update.message.reply_text("❌ المستخدم غير موجود")
        return

    status_map = {
        "active": "🟢 نشط",
        "inactive": "🟡 لم يدخل الويب",
        "deleted": "❌ محذوف"
    }

    await update.message.reply_text(
        f"""👤 بيانات المستخدم
ID: {data['telegram_id']}
Username: @{data.get('username') or "—"}
الحالة: {status_map[data['status']]}
النقاط: {data['points']}
"""
  )
