from fastapi import FastAPI, Request, HTTPException
from database.db import engine, Base, AsyncSessionLocal
from database.models import User
from sqlalchemy import select
from datetime import datetime
import hashlib, hmac, os, json
from urllib.parse import parse_qsl

BOT_TOKEN = os.getenv("USER_BOT_TOKEN")
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def verify(init_data: str):
    data = dict(parse_qsl(init_data))
    hash_recv = data.pop("hash")
    check = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret = hashlib.sha256(BOT_TOKEN.encode()).digest()
    h = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    if h != hash_recv:
        raise HTTPException(403)
    return json.loads(data["user"])

@app.post("/auth")
async def auth(req: Request):
    body = await req.json()
    user_data = verify(body["init_data"])

    async with AsyncSessionLocal() as session:
        res = await session.execute(
            select(User).where(User.telegram_id == user_data["id"])
        )
        user = res.scalar_one()
        user.is_active = True
        user.last_web_login = datetime.utcnow()
        await session.commit()

    return {"ok": True}
