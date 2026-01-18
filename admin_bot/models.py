# admin_bot/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    role = Column(String, nullable=False)  # owner | admin | moderator
    created_at = Column(DateTime(timezone=True), server_default=func.now())
