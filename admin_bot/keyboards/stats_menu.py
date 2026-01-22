from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def stats_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 إحصائيات عامة", callback_data="stats_global")],
        [InlineKeyboardButton("👤 إحصائيات مستخدم", callback_data="stats_user")],
        [InlineKeyboardButton("📤 تصدير CSV", callback_data="stats_export")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def time_filter_menu(prefix: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱️ 24 ساعة", callback_data=f"{prefix}:24h")],
        [InlineKeyboardButton("📅 أسبوع", callback_data=f"{prefix}:7d")],
        [InlineKeyboardButton("📆 شهر", callback_data=f"{prefix}:30d")],
        [InlineKeyboardButton("🗓️ 6 شهور", callback_data=f"{prefix}:180d")],
        [InlineKeyboardButton("📚 سنة", callback_data=f"{prefix}:365d")],
        [InlineKeyboardButton("🏛️ 5 سنين", callback_data=f"{prefix}:1825d")]
    ])
