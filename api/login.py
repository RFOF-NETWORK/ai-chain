# api/login.py
# Login-API: nutzt core.login (ein Passwortfeld, Admin/User-Logik)

from core import login as core_login


def handle(vm, username: str, password: str):
    """
    Login eines Users oder des Admins.
    Nutzt core.login.login, NICHT direkt vm.wallet.
    """
    result = core_login.login(username, password)

    if not result.get("success"):
        return {
            "status": "failed",
            "error": result.get("error", "LOGIN_FAILED")
        }

    return {
        "status": "ok",
        "username": result["username"],
        "address": result["wallet_address"],
        "is_admin": result.get("is_admin", False)
    }
