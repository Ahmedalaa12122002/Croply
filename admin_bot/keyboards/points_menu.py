from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def points_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ إضافة نقاط لمستخدم", callback_data="points_add")],
        [InlineKeyboardButton("➖ خصم نقاط من مستخدم", callback_data="points_deduct")],
        [InlineKeyboardButton("🎁 إضافة نقاط جماعية", callback_data="points_add_all")],
        [InlineKeyboardButton("🔻 خصم نقاط جماعي", callback_data="points_deduct_all")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def confirm_points(action: str, amount: int, target: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✔️ تأكيد", callback_data=f"confirm_points:{action}:{amount}:{target}"),
            InlineKeyboardButton("❌ إلغاء", callback_data="cancel")
        ]
    ])
