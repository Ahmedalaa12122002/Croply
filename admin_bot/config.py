# admin_bot/config.py
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

ROLE_OWNER = "owner"
ROLE_ADMIN = "admin"
ROLE_MODERATOR = "moderator"
