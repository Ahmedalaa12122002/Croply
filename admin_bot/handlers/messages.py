# admin_bot/handlers/messages.py
from telegram import Update
from telegram.ext import ContextTypes

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⌛ سيتم تفعيل هذه الميزة قريبًا")
