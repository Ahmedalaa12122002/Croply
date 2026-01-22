
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def finance_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏳ طلبات السحب", callback_data="withdraw_requests")],
        [InlineKeyboardButton("⏳ طلبات الإيداع", callback_data="deposit_requests")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")]
    ])

def decision_menu(kind: str, req_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✔️ قبول", callback_data=f"{kind}_approve:{req_id}"),
            InlineKeyboardButton("❌ رفض", callback_data=f"{kind}_reject:{req_id}")
        ]
    ])
