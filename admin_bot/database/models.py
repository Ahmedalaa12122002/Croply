from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime, Enum
)
from sqlalchemy.sql import func
from database.db import Base
import enum

class AdminAction(enum.Enum):
    ADD_POINTS = "add_points"
    DEDUCT_POINTS = "deduct_points"
    RESET_USER = "reset_user"
    DELETE_USER = "delete_user"
    APPROVE_WITHDRAW = "approve_withdraw"
    REJECT_WITHDRAW = "reject_withdraw"
    APPROVE_AD = "approve_ad"
    REJECT_AD = "reject_ad"

class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True)
    admin_id = Column(BigInteger, index=True)
    action = Column(Enum(AdminAction))
    target_id = Column(BigInteger, nullable=True)
    details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
