from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    username = Column(String)
    first_name = Column(String)
    created_at = Column(DateTime)
