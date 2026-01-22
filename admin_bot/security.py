# security.py
from config import OWNER_ID, EMERGENCY_LOCK
from permissions import get_admin_role, Role

def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

def is_admin(user_id: int) -> bool:
    return get_admin_role(user_id) is not None

def check_access(user_id: int, required_role: Role) -> bool:
    if is_owner(user_id):
        return True

    if EMERGENCY_LOCK:
        return False

    role = get_admin_role(user_id)
    if not role:
        return False

    return role.value >= required_role.value
