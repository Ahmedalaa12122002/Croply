from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def ads_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ إعلانات قيد الانتظار", callback_data="ads_pending")],
        [InlineKeyboardButton("➕ إضافة إعلان", callback_data="ads_add")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def ads_decision(ad_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✔️ قبول", callback_data=f"ads_approve:{ad_id}"),
            InlineKeyboardButton("❌ رفض", callback_data=f"ads_reject:{ad_id}")
        ]
    ])
