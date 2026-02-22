# viewer/portfolio_viewer.py
"""
portfolio_viewer.py
Stellt eine deterministische Übersicht über die Token‑ und Liquiditäts‑Bestände
eines Nutzers bereit. Wird von API, UI und vm_core.py genutzt.
"""

from typing import Dict, Any, Optional

class PortfolioViewer:
    """
    Aggregiert alle relevanten Token‑ und Pool‑Informationen eines Nutzers.
    Nutzt direkten Zugriff auf die Token-Balances für maximale Präzision.
    """

    def __init__(self, liquidity_pool=None):
        """
        liquidity_pool wird optional übergeben.
        vm_core.py übergibt hier den echten Pool.
        """
        self.pool = liquidity_pool

    # -------------------------------------------------------------------------
    # Token‑Balances (Fusionierte Logik)
    # -------------------------------------------------------------------------

    def get_user_assets(self, address: str, tokens: Dict[str, Any]) -> Dict[str, float]:
        """
        PZQQET-Standard: Extrahiert die exakten Balances aus den Token-Instanzen.
        Wird für die Echtzeit-Anzeige in charts.js genutzt.
        """
        return {
            "AI": tokens['AI'].balances.get(address, 0),
            "COIN": tokens['COIN'].balances.get(address, 0),
            "AIC-LP": tokens['AIC-LP'].balances.get(address, 0)
        }

    def get_token_balances(self, address: str, tokens: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Legacy-Wrapper für die UI-Kompatibilität. 
        Falls 'tokens' übergeben wird, nutzt es die neue Asset-Logik.
        """
        if tokens:
            return self.get_user_assets(address, tokens)
        
        # Fallback auf leere Werte, falls keine Instanzen geliefert werden
        return {"AI": 0, "COIN": 0, "AIC-LP": 0}

    # -------------------------------------------------------------------------
    # Liquidity‑Informationen
    # -------------------------------------------------------------------------

    def get_liquidity_info(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Gibt LP‑Anteile und deren Wert aus.
        """
        if self.pool is None or not hasattr(self.pool, "get_provider_info"):
            return None

        return self.pool.get_provider_info(address)

    # -------------------------------------------------------------------------
    # Gesamtportfolio
    # -------------------------------------------------------------------------

    def get_portfolio(self, address: str, tokens: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Kombiniert Token‑Balances + Liquidity‑Infos.
        Ideal für UI‑Darstellung und API‑Ausgabe.
        """
        return {
            "address": address,
            "tokens": self.get_token_balances(address, tokens),
            "liquidity": self.get_liquidity_info(address),
        }

# Singleton‑Instanz für den System-Kern
portfolio_viewer = PortfolioViewer()
