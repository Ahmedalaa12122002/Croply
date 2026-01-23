from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy import select
from .database import engine, Base, AsyncSessionLocal
from .models import User

API_KEY = "ADMIN_SECRET_KEY"  # هتحطها Variable

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/admin/user/{telegram_id}", dependencies=[Depends(verify_api_key)])
async def get_user(telegram_id: int):
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
