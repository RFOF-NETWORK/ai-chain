# ECCU/eccu_fond.py
"""
eccu_fond.py
ECCU-Fondslogik für die ai_chain-Umgebung.

Aufgabe:
- Verwalten eines einfachen, deterministischen Fonds (ECCU-Fond)
- Ein- und Ausstieg von Teilnehmern über Anteile (Shares)
- Berechnung eines Nettoinventarwerts (NAV) pro Anteil
- Saubere, auditierbare Zustandsdarstellung für VC.ecc / vc_eccu.py / vm.VC

Hinweis:
- Persistenz (Speichern/Laden) wird von außen geregelt (z. B. vm.VC, VC.ecc, Datenlayer).
- Diese Datei kümmert sich nur um die Logik im Speicher.
"""

from typing import Dict, Any


class ECCUFond:
    """
    Ein einfacher, deterministischer Fonds:
    - total_assets: Gesamtwert des Fonds in einer Basiseinheit (z. B. COIN)
    - total_shares: Gesamtanzahl der ausgegebenen Anteile
    - holders: Mapping address -> shares
    """

    def __init__(self) -> None:
        self.total_assets: float = 0.0
        self.total_shares: float = 0.0
        self.holders: Dict[str, float] = {}

    # -------------------------------------------------------------------------
    # NAV-Berechnung
    # -------------------------------------------------------------------------

    def get_nav(self) -> float:
        """
        Nettoinventarwert pro Anteil.
        Falls noch keine Anteile existieren, wird 1.0 als Basiswert verwendet.
        """
        if self.total_shares <= 0:
            return 1.0
        return self.total_assets / self.total_shares

    # -------------------------------------------------------------------------
    # Ein- und Ausstieg
    # -------------------------------------------------------------------------

    def invest(self, address: str, amount: float) -> Dict[str, Any]:
        """
        Ein Nutzer investiert einen Betrag in den Fonds.
        Dafür erhält er Anteile (Shares) zum aktuellen NAV.
        """
        if amount <= 0:
            return {"status": "rejected", "reason": "amount_must_be_positive"}

        nav = self.get_nav()
        new_shares = amount / nav

        # Fondsbestand aktualisieren
        self.total_assets += amount
        self.total_shares += new_shares

        # Holder-Bestand aktualisieren
        self.holders[address] = self.holders.get(address, 0.0) + new_shares

        return {
            "status": "accepted",
            "address": address,
            "invested": amount,
            "nav": nav,
            "new_shares": new_shares,
            "total_shares": self.total_shares,
            "total_assets": self.total_assets,
        }

    def redeem(self, address: str, shares: float) -> Dict[str, Any]:
        """
        Ein Nutzer löst Anteile ein und erhält den entsprechenden Gegenwert
        zum aktuellen NAV.
        """
        if shares <= 0:
            return {"status": "rejected", "reason": "shares_must_be_positive"}

        holder_shares = self.holders.get(address, 0.0)
        if holder_shares < shares:
            return {"status": "rejected", "reason": "insufficient_shares"}

        nav = self.get_nav()
        payout = shares * nav

        # Fondsbestand aktualisieren
        self.total_assets -= payout
        self.total_shares -= shares

        # Holder-Bestand aktualisieren
        remaining = holder_shares - shares
        if remaining <= 0:
            self.holders.pop(address, None)
        else:
            self.holders[address] = remaining

        return {
            "status": "accepted",
            "address": address,
            "redeemed_shares": shares,
            "payout": payout,
            "nav": nav,
            "total_shares": self.total_shares,
            "total_assets": self.total_assets,
        }

    # -------------------------------------------------------------------------
    # Abfragen / State
    # -------------------------------------------------------------------------

    def get_holder_info(self, address: str) -> Dict[str, Any]:
        """
        Liefert Informationen zu einem einzelnen Teilnehmer.
        """
        shares = self.holders.get(address, 0.0)
        nav = self.get_nav()
        value = shares * nav
        return {
            "address": address,
            "shares": shares,
            "nav": nav,
            "value": value,
        }

    def get_state(self) -> Dict[str, Any]:
        """
        Liefert einen vollständigen, deterministischen Snapshot des Fonds.
        Ideal für VC.ecc, Monitoring, Audits.
        """
        nav = self.get_nav()
        return {
            "total_assets": self.total_assets,
            "total_shares": self.total_shares,
            "nav": nav,
            "holders": {
                addr: {
                    "shares": shares,
                    "value": shares * nav,
                }
                for addr, shares in self.holders.items()
            },
        }


# Optional: Singleton-Instanz für einfache Nutzung
eccu_fond = ECCUFond()

