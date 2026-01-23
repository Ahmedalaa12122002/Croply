from telegram import Update
from telegram.ext import ContextTypes
from keyboards import (
    main_menu,
    users_menu,
    points_menu,
    stats_menu,
    settings_menu
)
from config import OWNER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ هذا بوت أدمن خاص")
        return

    await update.message.reply_text(
        "👑 لوحة تحكم الأدمن",
        reply_markup=main_menu()
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != OWNER_ID:
        await query.edit_message_text("❌ غير مصرح")
        return

    data = query.data

    if data == "users":
        await query.edit_message_text("👤 إدارة المستخدمين", reply_markup=users_menu())

    elif data == "points":
        await query.edit_message_text("💰 إدارة النقاط", reply_markup=points_menu())

    elif data == "stats":
        await query.edit_message_text("📊 الإحصائيات", reply_markup=stats_menu())

    elif data == "settings":
        await query.edit_message_text("⚙️ الإعدادات", reply_markup=settings_menu())

    elif data == "back_main":
        await query.edit_message_text("👑 لوحة تحكم الأدمن", reply_markup=main_menu())

    else:
        # noop أو أي زر غير مفعل
        await query.answer("🚧 هذه الميزة لم تُفعل بعد", show_alert=True)
