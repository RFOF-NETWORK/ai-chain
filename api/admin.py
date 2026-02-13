# api/admin.py
# Admin-API: Admin-Info + Admin-Portfolio

from core import admin as core_admin


def info(vm):
    """
    Liefert Basisinformationen zum Admin (Genesis-Owner).
    """
    admin_info = core_admin.get_admin_info()
    return {
        "status": "ok",
        "admin": admin_info
    }


def portfolio(vm):
    """
    Liefert Admin-Portfolio:
    - Owner-Balance
    - Fond-Balance
    - Safe-Werte
    Implementierung hängt von deiner VM-Struktur ab.
    Hier: defensive Platzhalter.
    """
    admin_address = core_admin.get_admin_address()

    owner_balance = None
    fund_balance = None
    safe_value = None

    # Beispiel: vm.wallet.get_balance für AI/COIN/AIC_LP
    if hasattr(vm, "wallet") and hasattr(vm.wallet, "get_balance"):
        try:
            owner_balance = vm.wallet.get_balance(admin_address)
        except Exception:
            owner_balance = None

    # Beispiel: vm.eccu oder vm.fund für Fond/Safe
    if hasattr(vm, "eccu") and hasattr(vm.eccu, "get_fund_balance"):
        try:
            fund_balance = vm.eccu.get_fund_balance(admin_address)
        except Exception:
            fund_balance = None

    if hasattr(vm, "eccu") and hasattr(vm.eccu, "get_safe_value"):
        try:
            safe_value = vm.eccu.get_safe_value()
        except Exception:
            safe_value = None

    return {
        "status": "ok",
        "admin_address": admin_address,
        "owner_balance": owner_balance,
        "fund_balance": fund_balance,
        "safe_value": safe_value
    }
