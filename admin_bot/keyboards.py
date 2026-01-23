from telegram import InlineKeyboardButton, InlineKeyboardMarkup

MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("👤 إدارة المستخدمين", callback_data="users")]
])

USERS_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔍 كشف حساب", callback_data="user_check")],
    [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
])
