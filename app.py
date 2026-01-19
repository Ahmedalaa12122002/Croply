from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from database import engine, Base
import os
import hashlib
import hmac
from urllib.parse import parse_qsl
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def verify_telegram_init_data(init_data: str) -> dict:
    data = dict(parse_qsl(init_data))
    hash_received = data.pop("hash", None)

    if not hash_received:
        raise HTTPException(status_code=403, detail="Missing hash")

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != hash_received:
        raise HTTPException(status_code=403, detail="Invalid signature")

    return data

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Croply</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body style="text-align:center;font-family:Arial">
<h2>جاري التحقق...</h2>
<script>
const tg = window.Telegram.WebApp;
if (!tg || !tg.initData) {
    document.body.innerHTML = "<h2>Telegram only</h2>";
} else {
    fetch("/auth", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({init_data: tg.initData})
    })
    .then(r => r.json())
    .then(d => {
        document.body.innerHTML = `<h1>مرحبًا ${d.first_name}</h1>`;
    })
    .catch(() => {
        document.body.innerHTML = "<h2>Access denied</h2>";
    });
}
</script>
</body>
</html>
"""

@app.post("/auth")
async def auth(request: Request):
    body = await request.json()
    data = verify_telegram_init_data(body["init_data"])
    user = json.loads(data.get("user", "{}"))

    return {
        "user_id": user.get("id"),
        "first_name": user.get("first_name"),
        "username": user.get("username")
}
