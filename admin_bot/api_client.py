import os
import requests

API_BASE = os.getenv("ADMIN_API_BASE")
API_KEY = os.getenv("ADMIN_API_KEY")

HEADERS = {"X-API-Key": API_KEY}

def api_get_user(telegram_id):
    r = requests.get(
        f"{API_BASE}/admin/user/{telegram_id}",
        headers=HEADERS,
        timeout=10
    )
    return r.json()

def api_reset_user(telegram_id):
    r = requests.post(
        f"{API_BASE}/admin/user/reset/{telegram_id}",
        headers=HEADERS,
        timeout=10
    )
    return r.json()

def api_delete_user(telegram_id):
    r = requests.post(
        f"{API_BASE}/admin/user/delete/{telegram_id}",
        headers=HEADERS,
        timeout=10
    )
    return r.json()
