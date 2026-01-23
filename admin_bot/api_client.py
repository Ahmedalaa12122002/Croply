import requests
from config import API_BASE_URL, API_KEY

def get_user(telegram_id: int):
    r = requests.get(
        f"{API_BASE_URL}/admin/user/{telegram_id}",
        headers={"X-API-Key": API_KEY},
        timeout=10
    )
    return r.json()
