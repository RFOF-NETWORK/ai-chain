# viewer/portfolio_viewer.py
"""
portfolio_viewer.py
Stellt eine deterministische Übersicht über die Token‑ und Liquiditäts‑Bestände
eines Nutzers bereit. Wird von API, UI und vm_core.py genutzt.

Funktionen:
- Aggregation aller Token‑Balances
- Darstellung von LP‑Anteilen
- Ausgabe in strukturierter Form für UI (scripts/ui.js & charts.js)
"""

from typing import Dict, Any, Optional

# Token‑Module liegen im Root
import ai_token
import coin_token
import aic_lp_token


class PortfolioViewer:
    """
    Aggregiert alle relevanten Token‑ und Pool‑Informationen eines Nutzers.
    """

    def __init__(self, liquidity_pool=None):
        """
        liquidity_pool wird optional übergeben.
        vm_core.py übergibt hier den echten Pool.
        """
        self.pool = liquidity_pool

    # -------------------------------------------------------------------------
    # Token‑Balances
    # -------------------------------------------------------------------------

    def get_token_balances(self, address: str) -> Dict[str, Any]:
        """
        Liefert die Token‑Balances eines Nutzers.
        Token‑Module müssen nur get_balance() bereitstellen.
        """
        return {
            "AI": ai_token.get_balance(address)
            if hasattr(ai_token, "get_balance") else 0,

            "COIN": coin_token.get_balance(address)
            if hasattr(coin_token, "get_balance") else 0,

            "AIC_LP": aic_lp_token.get_balance(address)
            if hasattr(aic_lp_token, "get_balance") else 0,
        }

    # -------------------------------------------------------------------------
    # Liquidity‑Informationen
    # -------------------------------------------------------------------------

    def get_liquidity_info(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Gibt LP‑Anteile und deren Wert aus.
        Falls kein Pool vorhanden ist, wird None zurückgegeben.
        """
        if self.pool is None:
            return None

        if not hasattr(self.pool, "get_provider_info"):
            return None

        provider_info = self.pool.get_provider_info(address)
        return provider_info

    # -------------------------------------------------------------------------
    # Gesamtportfolio
    # -------------------------------------------------------------------------

    def get_portfolio(self, address: str) -> Dict[str, Any]:
        """
        Kombiniert Token‑Balances + Liquidity‑Infos.
        Ideal für UI‑Darstellung und API‑Ausgabe.
        """
        return {
            "address": address,
            "tokens": self.get_token_balances(address),
            "liquidity": self.get_liquidity_info(address),
        }


# Optional: Singleton‑Instanz
portfolio_viewer = PortfolioViewer()

