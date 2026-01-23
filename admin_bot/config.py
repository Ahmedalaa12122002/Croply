import os

# Telegram
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
OWNER_ID = 5102387551

# API Security
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

if not ADMIN_BOT_TOKEN:
    raise RuntimeError("ADMIN_BOT_TOKEN missing")

if not ADMIN_API_KEY:
    raise RuntimeError("ADMIN_API_KEY missing")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL missing")
