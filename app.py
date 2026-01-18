from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import engine, Base
from models import User

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html lang="ar">
    <head><meta charset="UTF-8"></head>
    <body style="text-align:center;font-family:Arial">
        <h1>✅ الويب يعمل بنجاح</h1>
        <p>FastAPI + Railway + PostgreSQL</p>
    </body>
    </html>
    """

@app.get("/db-test")
async def db_test():
    return {"database": "connected"}
