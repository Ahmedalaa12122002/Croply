# permissions.py
from enum import Enum

class Role(Enum):
    BRONZE = 1
    GOLD = 2
    PLATINUM = 3
    PROFESSOR = 4
    OWNER = 5

# مؤقتًا (لاحقًا هنربطه بـ DB)
ADMINS = {
    5102387551: Role.OWNER
}

def get_admin_role(user_id: int):
    return ADMINS.get(user_id)
