from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from database import engine, Base
import hashlib
import hmac
import os
from urllib.parse import parse_qsl

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()


# ======================
# Telegram verification
# ======================
def verify_telegram_init_data(init_data: str) -> dict:
    data = dict(parse_qsl(init_data, strict_parsing=True))
    hash_received = data.pop("hash", None)

    if not hash_received:
        raise HTTPException(status_code=403, detail="Missing hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hash_calculated = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if hash_calculated != hash_received:
        raise HTTPException(status_code=403, detail="Invalid Telegram signature")

    return data


# ======================
# Startup
# ======================
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ======================
# WebApp UI (مؤقت)
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
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            init_data: tg.initData
        })
    })
    .then(res => res.json())
    .then(data => {
        document.body.innerHTML = `
        <h1>✅ مرحبًا ${data.first_name}</h1>
        <p>ID: ${data.user_id}</p>
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
# Auth endpoint
# ======================
@app.post("/auth")
async def auth(request: Request):
    body = await request.json()
    init_data = body.get("init_data")

    if not init_data:
        raise HTTPException(status_code=403, detail="No init data")

    data = verify_telegram_init_data(init_data)

    user = eval(data.get("user", "{}"))

    return JSONResponse({
        "status": "ok",
        "user_id": user.get("id"),
        "first_name": user.get("first_name"),
        "username": user.get("username")
    })
