from fastapi import FastAPI, HTTPException, Header
from sqlalchemy import select, update
from database import AsyncSessionLocal
from models import User
import os

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

app = FastAPI()

def check_key(x_api_key: str):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/admin/user/{telegram_id}")
async def get_user(telegram_id: int, x_api_key: str = Header(...)):
    check_key(x_api_key)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

    if not user:
        return {"exists": False}

    return {
        "exists": True,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "points": user.points,
        "is_active": user.is_active,
        "is_deleted": user.is_deleted,
        "last_web_login": user.last_web_login
    }

@app.post("/admin/user/reset/{telegram_id}")
async def reset_user(telegram_id: int, x_api_key: str = Header(...)):
    check_key(x_api_key)

    async with AsyncSessionLocal() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(points=0)
        )
        await session.commit()

    return {"status": "reset_done"}

@app.post("/admin/user/delete/{telegram_id}")
async def delete_user(telegram_id: int, x_api_key: str = Header(...)):
    check_key(x_api_key)

    async with AsyncSessionLocal() as session:
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(is_deleted=True, is_active=False)
        )
        await session.commit()

    return {"status": "deleted"}
