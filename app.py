import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading

# ======================
# ENV
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", 8080))

# ======================
# FASTAPI
# ======================
app = FastAPI()

app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/")
async def home():
    return FileResponse("web/index.html")

# ======================
# TELEGRAM BOT
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 دخول التطبيق",
                web_app=WebAppInfo(url=APP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 أهلاً بيك!\n\nاضغط على الزر وابدأ 👇",
        reply_markup=reply_markup
    )

def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.run_polling()

# ======================
# START BOT IN THREAD
# ======================
threading.Thread(target=run_bot).start()
