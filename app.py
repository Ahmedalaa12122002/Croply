from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from database import AsyncSessionLocal
from models import User
import json

app = FastAPI(title="Telegram Web App")

# -----------------------------------
# 🔒 حماية: الويب يعمل من Telegram فقط
# -----------------------------------
def get_telegram_user(request: Request):
    """
    يستخرج بيانات المستخدم من Telegram WebApp
    لو لم توجد → ممنوع الوصول
    """
    tg_init_data = request.headers.get("X-Telegram-Init-Data")

    if not tg_init_data:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Telegram access only"
        )

    try:
        data = json.loads(tg_init_data)
        user = data.get("user")
        if not user:
            raise ValueError
        return user
    except Exception:
        raise HTTPException(
            status_code=403,
            detail="Invalid Telegram data"
        )

# -----------------------------------
# 🏠 الصفحة الرئيسية (تسجيل تلقائي)
# -----------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # 🔐 تحقق إن الطلب من Telegram
    tg_user = get_telegram_user(request)

    telegram_id = tg_user.get("id")
    username = tg_user.get("username")
    first_name = tg_user.get("first_name")

    # 🗄️ تسجيل المستخدم تلقائيًا
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name
            )
            session.add(user)
            await session.commit()

    # 🖥️ واجهة بسيطة (مؤقتة)
    return """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>Telegram Web App</title>
    </head>
    <body style="text-align:center;font-family:Arial">
        <h1>✅ تم الدخول بنجاح</h1>
        <p>مرحبًا بك داخل تطبيق تيليجرام</p>
    </body>
    </html>
    """

# -----------------------------------
# ❤️ Health Check (للسيرفر فقط)
# -----------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}
