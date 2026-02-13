# ECCU/vc_eccu.py
"""
vc_eccu.py
Bindeglied zwischen VC.ecc (Electric Credit Coin Units) und der ai_chain‑VM.

Aufgaben:
- VC.ecc‑Instanz bereitstellen
- Fee‑Split‑Prozesse an VM weiterreichen (45/42/10/3)
- Safe‑Werte, Owner‑Werte und Fonds‑Werte abrufen
- ECCU‑Fond (eccu_fond.py) integrieren
- LICENSE‑Metadaten für Blöcke erzeugen
- Fundamentale Werte für UI/Charts bereitstellen
"""

from typing import Dict, Any

from ECCU.eccu_fond import eccu_fond
from VC.ecc import VCECC, TokenSymbol


class VCECCUAdapter:
    """
    Adapter zwischen VC.ecc und der VM.
    Diese Klasse stellt die offizielle ECCU‑Schnittstelle für die Chain dar.
    """

    def __init__(
        self,
        license_id: str,
        owner_address: str,
        eccu_fund_address: str
    ):
        # VC.ecc‑Instanz
        self.vc = VCECC(
            license_id=license_id,
            owner_address=owner_address,
            eccu_fund_address=eccu_fund_address
        )

        # ECCU‑Fond
        self.fond = eccu_fond

    # -------------------------------------------------------------------------
    # Fee‑Split‑Integration (45/42/10/3)
    # -------------------------------------------------------------------------

    def process_fee(
        self,
        vm,
        token: TokenSymbol,
        raw_fee_amount: float,
        base_fee_applier=None
    ) -> Dict[str, Any]:
        """
        Übergibt Fee‑Split an VC.ecc und integriert ihn in die VM.
        Diese Signatur ist 1:1 kompatibel mit fees.py.
        """
        split = self.vc.process_fee(
            vm=vm,
            token=token,
            raw_fee_amount=raw_fee_amount,
            base_fee_applier=base_fee_applier
        )
        return dict(split)

    # -------------------------------------------------------------------------
    # Safe‑Werte / Owner‑Werte / Fonds‑Werte
    # -------------------------------------------------------------------------

    def get_safe_value(self, token: TokenSymbol) -> float:
        self.vc.state.ensure_token(token)
        return self.vc.state.safe_slots[token].amount

    def get_owner_balance(self, token: TokenSymbol) -> float:
        self.vc.state.ensure_token(token)
        return self.vc.state.owner_balance[token]

    def get_eccu_fund_balance(self, token: TokenSymbol) -> float:
        self.vc.state.ensure_token(token)
        return self.vc.state.eccu_fund_balance[token]

    # -------------------------------------------------------------------------
    # ECCU‑Fond‑Integration
    # -------------------------------------------------------------------------

    def invest_in_fond(self, address: str, amount: float) -> Dict[str, Any]:
        return self.fond.invest(address, amount)

    def redeem_from_fond(self, address: str, shares: float) -> Dict[str, Any]:
        return self.fond.redeem(address, shares)

    def fond_state(self) -> Dict[str, Any]:
        return self.fond.get_state()

    # -------------------------------------------------------------------------
    # Fundamentale Werte (Charts 4 & 5)
    # -------------------------------------------------------------------------

    def fundamental_value(
        self,
        token: TokenSymbol,
        price_in_coin: float,
        coin_to_eccu_rate: float
    ) -> float:
        return self.vc.get_fundamental_value_token(
            token=token,
            price_in_coin=price_in_coin,
            coin_to_eccu_rate=coin_to_eccu_rate
        )

    # -------------------------------------------------------------------------
    # LICENSE‑Metadaten
    # -------------------------------------------------------------------------

    def license_metadata(
        self,
        block_index: int,
        block_hash: str,
        actor: str,
        context: str
    ) -> Dict[str, Any]:
        return self.vc.build_license_metadata(
            block_index=block_index,
            block_hash=block_hash,
            actor=actor,
            context=context
        )


# -------------------------------------------------------------------------
# Singleton‑Instanz für die gesamte Chain
# -------------------------------------------------------------------------

vc_eccu = VCECCUAdapter(
    license_id="LICENSE:AI_CHAIN",
    owner_address="OWNER_WALLET",
    eccu_fund_address="ECCU_FUND_WALLET"
)
