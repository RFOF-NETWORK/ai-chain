# core/dex.py
# de-en: DEX / bridge adapter (AI/COIN/AIC_LP <-> external tokens)

from typing import Dict


def swap_ai_to(token_symbol: str, amount: float) -> Dict:
    return {
        "success": True,
        "from": "AI",
        "to": token_symbol,
        "amount": amount
    }


def swap_coin_to(token_symbol: str, amount: float) -> Dict:
    return {
        "success": True,
        "from": "COIN",
        "to": token_symbol,
        "amount": amount
    }


def swap_lp_to(token_symbol: str, amount: float) -> Dict:
    return {
        "success": True,
        "from": "AIC_LP",
        "to": token_symbol,
        "amount": amount
    }
