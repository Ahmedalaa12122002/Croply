from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from database.db import AsyncSessionLocal
from database.models import User
from sqlalchemy import select
import os

BOT_TOKEN = os.getenv("USER_BOT_TOKEN")
APP_URL = os.getenv("WEB_APP_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg = update.effective_user

    async with AsyncSessionLocal() as session:
        res = await session.execute(
            select(User).where(User.telegram_id == tg.id)
        )
        user = res.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=tg.id,
                username=tg.username,
                first_name=tg.first_name
            )
            session.add(user)
            await session.commit()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 فتح التطبيق", web_app=WebAppInfo(url=APP_URL))]
    ])

    await update.message.reply_text(
        "مرحبًا بك 👋",
        reply_markup=keyboard
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
