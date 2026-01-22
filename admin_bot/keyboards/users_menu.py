from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def users_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 كشف حساب مستخدم", callback_data="user_lookup")],
        [InlineKeyboardButton("🧹 تصفير حساب مستخدم", callback_data="user_reset")],
        [InlineKeyboardButton("🔴 حذف مستخدم نهائيًا", callback_data="user_delete")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def confirm_menu(action: str, target_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✔️ تأكيد", callback_data=f"confirm:{action}:{target_id}"),
            InlineKeyboardButton("❌ إلغاء", callback_data="cancel")
        ]
    ])
