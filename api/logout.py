# api/logout.py
# Logout-API: struktureller Platzhalter

from core import logout as core_logout


def handle(vm, session_token: str):
    """
    Logout eines Users/Admins.
    Session-Handling wäre auf höherer Ebene, hier nur strukturell.
    """
    result = core_logout.logout(session_token)
    return {
        "status": "ok" if result.get("success") else "failed"
    }
