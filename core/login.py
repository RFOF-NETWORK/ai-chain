# core/login.py
# de-en: Login logic for admin + users (one password field, different modes)

import json
from pathlib import Path
from typing import Dict, Optional

from core.security import double_sha256
from core.admin import (
    is_admin_username,
    get_admin_phrase_hash,
    get_admin_address,
    get_admin_username,
)

USERS_JSON_PATH = Path("data/users.json")


def load_users() -> Dict:
    if not USERS_JSON_PATH.exists():
        return {"users": []}
    with USERS_JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_user(username: str) -> Optional[Dict]:
    data = load_users()
    for u in data.get("users", []):
        if u["username"] == username:
            return u
    return None


def login(username: str, password_or_phrase: str) -> Dict:
    """
    One password field:
    - If username == admin_username:
        - password_or_phrase can be admin phrase OR admin password
        - we compare double_sha256(input) with admin_phrase_hash OR stored password_hash
    - Else:
        - treat password_or_phrase as normal password
    """
    user = find_user(username)
    if not user:
        return {"success": False, "error": "USER_NOT_FOUND"}

    input_hash = double_sha256(password_or_phrase)

    # Admin-Case
    if is_admin_username(username):
        admin_phrase_hash = get_admin_phrase_hash()
        # Admin kann sich mit Phrase (hash match) oder mit normalem Passwort (user.password_hash) einloggen
        if input_hash == admin_phrase_hash or input_hash == user.get("password_hash"):
            return {
                "success": True,
                "username": username,
                "wallet_address": get_admin_address(),
                "is_admin": True
            }
        return {"success": False, "error": "INVALID_ADMIN_CREDENTIALS"}

    # Normaler User
    if input_hash == user.get("password_hash"):
        return {
            "success": True,
            "username": username,
            "wallet_address": user.get("wallet_address"),
            "is_admin": user.get("is_admin", False)
        }

    return {"success": False, "error": "INVALID_CREDENTIALS"}
