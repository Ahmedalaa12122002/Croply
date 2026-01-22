from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID

def main_menu(user_id: int):
    buttons = [
        [InlineKeyboardButton("👤 إدارة المستخدمين", callback_data="users")],
        [InlineKeyboardButton("💰 النقاط / العملات", callback_data="points")],
        [InlineKeyboardButton("📢 الإعلانات / المهام", callback_data="ads")],
        [InlineKeyboardButton("🏦 السحب والإيداع", callback_data="finance")],
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")]
    ]

    if user_id == OWNER_ID:
        buttons.append(
            [InlineKeyboardButton("🛡️ صلاحيات الأدمن", callback_data="admin_roles")]
        )

    return InlineKeyboardMarkup(buttons)
