from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import os
from database import SessionLocal
from models import User, AdminLog
from datetime import datetime

# =========================
# ENV
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_SECRET = os.getenv("ADMIN_SECRET")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing")

if not ADMIN_SECRET:
    raise RuntimeError("ADMIN_SECRET is missing")

# =========================
# APP
# =========================
app = FastAPI(title="Admin API", version="1.0")

# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Security Dependency
# =========================
def verify_admin(x_admin_secret: str = Header(...)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin secret")

# =========================
# Utils
# =========================
def log_action(db, admin_id: int, action: str):
    log = AdminLog(
        admin_id=admin_id,
        action=action,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()

# =========================
# Routes
# =========================

@app.get("/")
def root():
    return {"status": "Admin API running securely"}

# -------------------------
# Reset User (تصفير)
# -------------------------
@app.post("/admin/user/reset/{telegram_id}")
def reset_user(
    telegram_id: int,
    admin_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin)
):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.points = 0
    user.balance = 0
    db.commit()

    log_action(db, admin_id, f"Reset user {telegram_id}")
    return {"status": "ok", "message": "User reset successfully"}

# -------------------------
# Delete User (حذف نهائي)
# -------------------------
@app.delete("/admin/user/delete/{telegram_id}")
def delete_user(
    telegram_id: int,
    admin_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin)
):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    log_action(db, admin_id, f"Deleted user {telegram_id}")
    return {"status": "ok", "message": "User deleted permanently"}

# -------------------------
# Get User Info
# -------------------------
@app.get("/admin/user/info/{telegram_id}")
def get_user_info(
    telegram_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin)
):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "telegram_id": user.telegram_id,
        "points": user.points,
        "balance": user.balance,
        "created_at": user.created_at,
        "last_active": user.last_active
    }

# -------------------------
# Admin Logs
# -------------------------
@app.get("/admin/logs")
def admin_logs(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin)
):
    logs = db.query(AdminLog).order_by(AdminLog.created_at.desc()).limit(100).all()
    return [
        {
            "admin_id": log.admin_id,
            "action": log.action,
            "time": log.created_at
        }
        for log in logs
    ]
