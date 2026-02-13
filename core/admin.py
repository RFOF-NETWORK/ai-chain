# core/admin.py
# de-en: Admin and Genesis owner logic

import json
from typing import Dict
from pathlib import Path

ADMIN_JSON_PATH = Path("data/admin.json")


def load_admin_config() -> Dict:
    if not ADMIN_JSON_PATH.exists():
        return {}
    with ADMIN_JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_admin_username() -> str:
    cfg = load_admin_config()
    return cfg.get("admin_username", "")


def get_admin_address() -> str:
    cfg = load_admin_config()
    return cfg.get("admin_address", "")


def get_admin_phrase_hash() -> str:
    cfg = load_admin_config()
    return cfg.get("admin_phrase_hash", "")


def is_admin_username(username: str) -> bool:
    return username == get_admin_username()


def is_admin_address(address: str) -> bool:
    return address == get_admin_address()


def get_admin_info() -> Dict[str, str]:
    cfg = load_admin_config()
    return {
        "admin_username": cfg.get("admin_username", ""),
        "admin_address": cfg.get("admin_address", ""),
        "role": cfg.get("role", "GENESIS_OWNER"),
        "is_admin": cfg.get("is_admin", True)
    }
