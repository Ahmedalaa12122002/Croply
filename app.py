from database import engine
from sqlalchemy import text

@app.get("/db-test")
async def db_test():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            return {"status": "ok", "db": result.scalar()}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
