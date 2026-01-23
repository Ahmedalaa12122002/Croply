from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 إدارة المستخدمين", callback_data="users")],
        [InlineKeyboardButton("💰 النقاط", callback_data="points")],
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")]
    ])

def users_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 كشف حساب (قريبًا)", callback_data="noop")],
        [InlineKeyboardButton("🧹 مسح بيانات (قريبًا)", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def points_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ إضافة نقاط (قريبًا)", callback_data="noop")],
        [InlineKeyboardButton("➖ خصم نقاط (قريبًا)", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def stats_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 إحصائيات عامة (قريبًا)", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def settings_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 صلاحيات الأدمن (قريبًا)", callback_data="noop")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])
