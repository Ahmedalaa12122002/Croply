# admin_bot/keyboards/admin_menu.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def admin_menu():
    keyboard = [
        [InlineKeyboardButton("🆕 أحدث المستخدمين", callback_data="latest_users")],
        [InlineKeyboardButton("🔍 البحث عن مستخدم", callback_data="search_user")]
    ]
    return InlineKeyboardMarkup(keyboard)
