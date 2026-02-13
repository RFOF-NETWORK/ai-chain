# api/banking.py
# Fiat-Banking-API: EUR/USD <-> AI/COIN/AIC_LP

from core import banking as core_banking


def deposit(vm, username: str, amount: float, currency: str, target_token: str):
    """
    Fiat-Einzahlung (EUR/USD) in AI/COIN/AIC_LP.
    Externe Payment-Provider (PayPal/Stripe/Bank) liegen außerhalb dieser Funktion.
    """
    result = core_banking.fiat_deposit(username, amount, currency, target_token)

    # Optional: Blockchain-Zustand speichern
    if hasattr(vm, "blockchain") and hasattr(vm.blockchain, "save_state"):
        vm.blockchain.save_state()

    return {
        "status": "ok" if result.get("success") else "failed",
        "type": result.get("type"),
        "username": result.get("username"),
        "amount": result.get("amount"),
        "currency": result.get("currency"),
        "token": result.get("target_token")
    }


def withdraw(vm, username: str, amount: float, currency: str, source_token: str):
    """
    Fiat-Auszahlung (EUR/USD) aus AI/COIN/AIC_LP.
    """
    result = core_banking.fiat_withdraw(username, amount, currency, source_token)

    if hasattr(vm, "blockchain") and hasattr(vm.blockchain, "save_state"):
        vm.blockchain.save_state()

    return {
        "status": "ok" if result.get("success") else "failed",
        "type": result.get("type"),
        "username": result.get("username"),
        "amount": result.get("amount"),
        "currency": result.get("currency"),
        "token": result.get("source_token")
    }

