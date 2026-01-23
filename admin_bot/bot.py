from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import requests
from config import ADMIN_BOT_TOKEN, OWNER_ID, ADMIN_API_KEY

API_BASE = "http://127.0.0.1:8000"  # Railway هيستبدلها تلقائي

STATE = {}

MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("👤 إدارة المستخدمين", callback_data="users")]
])

USERS_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔍 كشف حساب", callback_data="check_user")],
    [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ بوت أدمن خاص")
        return

    await update.message.reply_text("👑 لوحة تحكم الأدمن", reply_markup=MAIN_MENU)

async def open_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "👤 إدارة المستخدمين",
        reply_markup=USERS_MENU
    )

async def ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    STATE[update.effective_user.id] = "WAIT_ID"
    await update.callback_query.edit_message_text("✍️ اكتب Telegram ID:")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if STATE.get(update.effective_user.id) != "WAIT_ID":
        return

    STATE.pop(update.effective_user.id)

    if not update.message.text.isdigit():
        await update.message.reply_text("❌ ID غير صحيح")
        return

    r = requests.get(
        f"{API_BASE}/admin/user/{update.message.text}",
        headers={"X-API-Key": ADMIN_API_KEY},
        timeout=10
    )

    data = r.json()

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

def main():
    app = ApplicationBuilder().token(ADMIN_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(open_users, pattern="users"))
    app.add_handler(CallbackQueryHandler(ask_id, pattern="check_user"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
