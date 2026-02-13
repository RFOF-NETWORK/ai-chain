# api/swap.py
# High-Level Swap-API: Routing für Swaps (AI/COIN/AIC_LP <-> extern)

from . import dex as dex_api


def handle(vm, from_token: str, to_token: str, amount: float):
    """
    High-Level Swap-Endpunkt.
    Nutzt api.dex.handle als eigentliche DEX-Logik.
    """
    return dex_api.handle(vm, from_token, to_token, amount)
