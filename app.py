from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "web is working"}

@app.get("/db-test")
async def db_test():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        return {"database": result.scalar()}
