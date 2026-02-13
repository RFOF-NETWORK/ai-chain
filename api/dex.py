# api/dex.py
# DEX/Bridge-API: AI/COIN/AIC_LP <-> externe Tokens

from core import dex as core_dex


def handle(vm, from_token: str, to_token: str, amount: float):
    """
    Generische DEX-Schnittstelle.
    from_token: "AI", "COIN", "AIC_LP"
    to_token: externes Symbol (z.B. "ETH", "USDT", ...)
    """
    from_token = from_token.upper()

    if from_token == "AI":
        result = core_dex.swap_ai_to(to_token, amount)
    elif from_token == "COIN":
        result = core_dex.swap_coin_to(to_token, amount)
    elif from_token in ("AIC_LP", "AIC-LP", "AICLP"):
        result = core_dex.swap_lp_to(to_token, amount)
    else:
        return {
            "status": "failed",
            "error": "UNSUPPORTED_FROM_TOKEN"
        }

    # Optional: Blockchain-Zustand speichern
    if hasattr(vm, "blockchain") and hasattr(vm.blockchain, "save_state"):
        vm.blockchain.save_state()

    return {
        "status": "ok" if result.get("success") else "failed",
        "from": result.get("from"),
        "to": result.get("to"),
        "amount": result.get("amount")
    }

