from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, get_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    # تأكيد الاتصال بقاعدة البيانات عند التشغيل
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>Croply Web</title>
    </head>
    <body style="background:#0f172a;color:white;text-align:center;font-family:Arial;margin-top:50px">
        <h1>✅ الويب يعمل بنجاح</h1>
        <p>FastAPI + Railway + Postgres شغالين 100%</p>
    </body>
    </html>
    """


@app.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"database": result.scalar()}
