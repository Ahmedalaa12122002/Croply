import os

BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
OWNER_ID = 5102387551  # ايديك انت

if not BOT_TOKEN:
    raise RuntimeError("ADMIN_BOT_TOKEN is missing")
