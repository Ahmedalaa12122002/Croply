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
2-database.py
(الاتصال بقاعدة البيانات)
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

لازم تكون asyncpg

if DATABASE_URL.startswith("postgresql://"):
DATABASE_URL = DATABASE_URL.replace(
"postgresql://", "postgresql+asyncpg://", 1
)

engine = create_async_engine(
DATABASE_URL,
echo=False,
pool_pre_ping=True
)

AsyncSessionLocal = sessionmaker(
engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
async with AsyncSessionLocal() as session:
yield session

3-models.py
(جداول قاعدة البيانات)
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
tablename = "users"

id = Column(Integer, primary_key=True)  
telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)  
username = Column(String(64))  
first_name = Column(String(64))  
is_active = Column(Boolean, default=True)  
created_at = Column(DateTime(timezone=True), server_default=func.now())
