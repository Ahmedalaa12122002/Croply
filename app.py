import os
import asyncio
import json
import hashlib
import hmac
from urllib.parse import parse_qsl

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

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

app = FastAPI()
bot_app: Application | None = None

# ======================
# Startup
# ======================
@app.on_event("startup")
async def startup():
    global bot_app

    # DB
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Bot
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))

    asyncio.create_task(bot_app.initialize())
    asyncio.create_task(bot_app.start())
    asyncio.create_task(bot_app.bot.initialize())
    asyncio.create_task(bot_app.updater.start_polling())

    print("🤖 Bot + 🌐 Web started")

# ======================
# Telegram /start
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
            msg = "🎉 تم تسجيلك لأول مرة بنجاح"
        else:
            msg = "👋 مرحبًا بعودتك"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🚀 فتح التطبيق",
                web_app=WebAppInfo(url=APP_URL)
            )
        ]
    ])

    await update.message.reply_text(msg, reply_markup=keyboard)

# ======================
# Telegram WebApp verify
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
# Web UI
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
<body style="text-align:center;font-family:Arial">

<h2>⏳ جاري التحقق...</h2>

<script>
const tg = window.Telegram.WebApp;

if (!tg || !tg.initData) {
    document.body.innerHTML = "<h2>❌ Telegram only</h2>";
} else {
    fetch("/auth", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ init_data: tg.initData })
    })
    .then(r => r.json())
    .then(d => {
        document.body.innerHTML = `<h1>✅ مرحبًا ${d.first_name}</h1>`;
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
# Auth
# ======================
@app.post("/auth")
async def auth(request: Request):
    body = await request.json()
    init_data = body.get("init_data")

    if not init_data:
        raise HTTPException(status_code=403, detail="No init data")

    data = verify_telegram_init_data(init_data)
    user = json.loads(data.get("user", "{}"))

    return JSONResponse({
        "status": "ok",
        "user_id": user.get("id"),
        "first_name": user.get("first_name"),
        "username": user.get("username")
    })
