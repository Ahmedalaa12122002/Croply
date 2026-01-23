from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID
from keyboards import (
    main_menu, users_menu, points_menu,
    ads_menu, finance_menu, stats_menu,
    admin_menu, permissions_menu
)

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
        await query.edit_message_text("👑 لوحة تحكم الأدمن", reply_markup=main_menu())

    else:
        await query.answer("🚧 هذه الميزة ستُفعل لاحقًا", show_alert=True)
