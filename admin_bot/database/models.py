from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String)
    first_name = Column(String)

    points = Column(Integer, default=0)

    is_active = Column(Boolean, default=False)  # دخل الويب؟
    created_at = Column(DateTime, server_default=func.now())
    last_web_login = Column(DateTime, nullable=True)

    deleted_at = Column(DateTime, nullable=True)  # حذف نهائي (Soft)
