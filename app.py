from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import os
import hashlib
import hmac
from urllib.parse import parse_qsl
import json

app = FastAPI()

# ======================
# ENV
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

# ======================
# Telegram verification
# ======================
def verify_telegram_init_data(init_data: str) -> dict:
    if not isinstance(init_data, str):
        raise HTTPException(status_code=403, detail="Invalid init data type")

    data = dict(parse_qsl(init_data))
    hash_received = data.pop("hash", None)

    if not hash_received:
        raise HTTPException(status_code=403, detail="Missing hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if calculated_hash != hash_received:
        raise HTTPException(status_code=403, detail="Invalid Telegram signature")

    return data

# ======================
# Home (Telegram only)
# ======================
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
<body style="font-family:Arial;text-align:center">

<h3>⏳ جاري التحقق...</h3>

<script>
const tg = window.Telegram.WebApp;

if (!tg || !tg.initData) {
    document.body.innerHTML = "<h2>❌ Telegram access only</h2>";
} else {
    fetch("/auth", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            init_data: tg.initData   // ✅ STRING
        })
    })
    .then(res => res.json())
    .then(data => {
        document.body.innerHTML = `
            <h2>✅ مرحبًا ${data.first_name}</h2>
            <p>ID: ${data.user_id}</p>
            <p>@${data.username || "لا يوجد"}</p>
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

    return JSONResponse({
        "status": "ok",
        "user_id": data.get("user[id]"),
        "first_name": data.get("user[first_name]"),
        "username": data.get("user[username]")
    })
