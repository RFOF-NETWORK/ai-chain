# core/register.py
# de-en: User registration with wallet + mnemonic

import json
from pathlib import Path
from typing import Dict, List

from core.security import double_sha256, generate_mnemonic_24, derive_address_from_mnemonic

USERS_JSON_PATH = Path("data/users.json")


def load_users() -> Dict:
    if not USERS_JSON_PATH.exists():
        return {"users": []}
    with USERS_JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_users(data: Dict) -> None:
    with USERS_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def username_exists(username: str) -> bool:
    data = load_users()
    return any(u["username"] == username for u in data.get("users", []))


def register_user(username: str, password: str) -> Dict:
    """
    Register a new user:
    - generate 24-word mnemonic
    - derive wallet address
    - store username, password_hash, wallet_address
    - return mnemonic + address (for UI to show/download once)
    """
    if username_exists(username):
        return {"success": False, "error": "USERNAME_EXISTS"}

    mnemonic: List[str] = generate_mnemonic_24()
    address: str = derive_address_from_mnemonic(mnemonic)
    password_hash = double_sha256(password)

    data = load_users()
    data["users"].append({
        "username": username,
        "password_hash": password_hash,
        "wallet_address": address,
        "is_admin": False
    })
    save_users(data)

    return {
        "success": True,
        "username": username,
        "wallet_address": address,
        "mnemonic": mnemonic
    }
