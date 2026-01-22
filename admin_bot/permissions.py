from enum import Enum

class Role(Enum):
    BRONZE = 1
    GOLD = 2
    PLATINUM = 3
    PROFESSOR = 4
    OWNER = 5

# مؤقتًا في الذاكرة (لاحقًا DB)
ADMINS = {
    5102387551: Role.OWNER
}

def get_admin_role(user_id: int):
    return ADMINS.get(user_id)

def add_admin(user_id: int, role: Role):
    ADMINS[user_id] = role

def remove_admin(user_id: int):
    if user_id in ADMINS and ADMINS[user_id] != Role.OWNER:
        ADMINS.pop(user_id)

def update_admin_role(user_id: int, role: Role):
    if user_id in ADMINS and ADMINS[user_id] != Role.OWNER:
        ADMINS[user_id] = role
