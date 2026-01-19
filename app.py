import os
import json
import hashlib
import hmac
from urllib.parse import parse_qsl

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from sqlalchemy import select
from database import engine, Base, AsyncSessionLocal
from models import User

# ======================
# ENV
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not APP_URL:
    raise RuntimeError("APP_URL is missing")

# ======================
# FastAPI
# ======================
app = FastAPI()

# ======================
# Startup DB
# ======================
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ======================
# Telegram WebApp Verify
# ======================
def verify_telegram_init_data(init_data: str) -> dict:
    data = dict(parse_qsl(init_data))
    hash_received = data.pop("hash", None)

    if not hash_received:
        raise HTTPException(status_code=403, detail="Missing hash")

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    calculated_hash = hmac.new(
        secret_key,
        check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if calculated_hash != hash_received:
        raise HTTPException(status_code=403, detail="Invalid Telegram signature")

    return data

# ======================
# WebApp UI
# ======================
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>Croply</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body style="font-family:Arial;text-align:center">

<h2>⏳ جاري التحقق...</h2>

<script>
const tg = window.Telegram.WebApp;

if (!tg || !tg.initData) {
    document.body.innerHTML = "<h2>❌ Telegram only</h2>";
} else {
    fetch("/auth", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({init_data: tg.initData})
    })
    .then(res => res.json())
    .then(data => {
        document.body.innerHTML = `
            <h1>👋 مرحبًا ${data.first_name}</h1>
            <p>ID: ${data.user_id}</p>
            <p>@${data.username || "—"}</p>
        `;
    })
    .catch(() => {
        document.body.innerHTML = "<h2>❌ Access denied</h2>";
    });
}
</script>

</body>
</html>
"""

# ======================
# Auth API
# ======================
@app.post("/auth")
async def auth(request: Request):
    body = await request.json()
    init_data = body.get("init_data")

    if not init_data:
        raise HTTPException(status_code=403, detail="No init data")

    data = verify_telegram_init_data(init_data)
    user_data = json.loads(data.get("user", "{}"))

    return JSONResponse({
        "user_id": user_data.get("id"),
        "first_name": user_data.get("first_name"),
        "username": user_data.get("username")
    })

# ======================
# Telegram Bot
# ======================
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
            msg = "🎉 تم تسجيلك بنجاح"
        else:
            msg = "👋 مرحبًا بعودتك"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🚀 فتح التطبيق",
            web_app=WebAppInfo(url=APP_URL)
        )]
    ])

    await update.message.reply_text(msg, reply_markup=keyboard)

# ======================
# Run Bot
# ======================
def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# ======================
# Start Bot in background
# ======================
import threading
threading.Thread(target=run_bot).start()
