import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy import select
from database import AsyncSessionLocal
from models import User

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == tg_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name
            )
            session.add(user)
            await session.commit()
            msg = "🎉 تم تسجيلك لأول مرة"
        else:
            msg = "👋 مرحبًا بعودتك"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 فتح التطبيق", web_app=WebAppInfo(url=APP_URL))]
    ])

    await update.message.reply_text(msg, reply_markup=keyboard)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 Bot is running")
    app.run_polling()

if __name__ == "__main__":
    main()
