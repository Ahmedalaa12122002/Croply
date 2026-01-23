from fastapi import FastAPI, Header, HTTPException
from sqlalchemy import select
from database import engine, Base, AsyncSessionLocal
from models import User
from config import ADMIN_API_KEY

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def check_api_key(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/admin/user/{telegram_id}")
async def get_user(telegram_id: int, x_api_key: str = Header(...)):
    check_api_key(x_api_key)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

    if not user:
        return {"exists": False}

    if user.is_deleted:
        status = "deleted"
    elif user.is_active:
        status = "active"
    else:
        status = "inactive"

    return {
        "exists": True,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "points": user.points,
        "status": status,
        "last_web_login": user.last_web_login
}
