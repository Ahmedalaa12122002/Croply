# admin_bot/handlers/permissions.py
from config import ADMIN_ID, ROLE_OWNER
from database import AsyncSessionLocal
from models import AdminUser
from sqlalchemy import select

async def get_user_role(user_id: int):
    # 🔥 طوارئ: صاحب المشروع
    if user_id == ADMIN_ID:
        return ROLE_OWNER

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AdminUser).where(AdminUser.telegram_id == user_id)
        )
        admin = result.scalar_one_or_none()

        if admin:
            return admin.role

    return None
