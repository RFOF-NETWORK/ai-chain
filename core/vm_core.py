# core/vm_core.py
"""
vm_core.py
Zentrale VM-Steuerlogik für die ai_chain-Umgebung.

Aufgabe:
- Einheitlicher Einstiegspunkt für Kernoperationen (Transaktionen, Wallet, Liquidity, Viewer).
- Kapselt Aufrufe an blockchain, fees, wallet_system, liquidity_pool, smartcontracts und Tokens.
- Bietet eine stabile, deterministische Schnittstelle für api/, ai-chain.py und vm.VC.
"""

from typing import Any, Dict, Optional, List

from core.blockchain import Blockchain
from core.fees import FeeCalculator
from wallet.wallet_system import WalletSystem
from liquidity.liquidity_pool import LiquidityPool
from viewer.chain_viewer import ChainViewer

# Tokens liegen im Root
import ai_token
import coin_token
import aic_lp_token

import smartcontracts


class VMCore:
    """
    VMCore ist der zentrale Orchestrator.
    Er kennt:
    - die Blockchain
    - das Wallet-System
    - den Liquidity-Pool
    - die Gebührenlogik
    - die Viewer-Logik
    - die Token-Module
    - die Smartcontracts
    """

    def __init__(self) -> None:
        self.blockchain = Blockchain()
        self.fees = FeeCalculator()
        self.wallets = WalletSystem()
        self.liquidity = LiquidityPool()
        self.viewer = ChainViewer()

        # Token-Referenzen (können einfache Klassen oder Funktionsmodule sein)
        self.ai_token = ai_token
        self.coin_token = coin_token
        self.aic_lp_token = aic_lp_token

        self.smartcontracts = smartcontracts

    # -------------------------------------------------------------------------
    # Basis-Informationen
    # -------------------------------------------------------------------------

    def get_chain_info(self) -> Dict[str, Any]:
        """
        Liefert eine deterministische Übersicht über den aktuellen Chain-Zustand.
        """
        return {
            "height": self.blockchain.get_height(),
            "last_block_hash": self.blockchain.get_last_block_hash(),
            "total_transactions": self.blockchain.get_total_transactions(),
        }

    def get_wallet_balance(self, address: str) -> Dict[str, Any]:
        """
        Liefert die Balances eines Wallets für alle relevanten Token.
        """
        base_balance = self.wallets.get_balance(address)
        return {
            "address": address,
            "base": base_balance,
            "ai_token": self.ai_token.get_balance(address)
            if hasattr(self.ai_token, "get_balance")
            else None,
            "coin_token": self.coin_token.get_balance(address)
            if hasattr(self.coin_token, "get_balance")
            else None,
            "aic_lp_token": self.aic_lp_token.get_balance(address)
            if hasattr(self.aic_lp_token, "get_balance")
            else None,
        }

    # -------------------------------------------------------------------------
    # Transaktionen
    # -------------------------------------------------------------------------

    def submit_transaction(
        self,
        from_addr: str,
        to_addr: str,
        amount: float,
        token: str = "BASE",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Reicht eine Transaktion über die VM ein.
        - Berechnet Gebühren
        - Validiert
        - Übergibt an Blockchain
        """
        metadata = metadata or {}

        fee = self.fees.calculate_fee(amount=amount, token=token)
        tx = {
            "from": from_addr,
            "to": to_addr,
            "amount": amount,
            "token": token,
            "fee": fee,
            "metadata": metadata,
        }

        # Token-spezifische Logik (falls vorhanden)
        if token.upper() == "AI":
            validator = getattr(self.ai_token, "validate_tx", None)
        elif token.upper() == "COIN":
            validator = getattr(self.coin_token, "validate_tx", None)
        elif token.upper() == "AIC_LP":
            validator = getattr(self.aic_lp_token, "validate_tx", None)
        else:
            validator = None

        if callable(validator):
            valid, reason = validator(tx)
            if not valid:
                return {"status": "rejected", "reason": reason}

        # Wallet-Check (Basis-Logik)
        if not self.wallets.has_funds(from_addr, amount + fee):
            return {"status": "rejected", "reason": "insufficient_funds"}

        # Übergabe an Blockchain
        tx_hash = self.blockchain.add_transaction(tx)
        return {"status": "accepted", "tx_hash": tx_hash, "fee": fee}

    # -------------------------------------------------------------------------
    # Liquidity / Pools
    # -------------------------------------------------------------------------

    def add_liquidity(
        self,
        provider: str,
        amount_ai: float,
        amount_coin: float,
    ) -> Dict[str, Any]:
        """
        Fügt dem Liquidity-Pool AI/COIN-Liquidität hinzu.
        """
        if not self.wallets.has_funds(provider, amount_ai + amount_coin):
            return {"status": "rejected", "reason": "insufficient_funds"}

        result = self.liquidity.add_liquidity(provider, amount_ai, amount_coin)
        return {"status": "accepted", "result": result}

    def remove_liquidity(self, provider: str, share: float) -> Dict[str, Any]:
        """
        Entfernt Liquidität aus dem Pool.
        """
        result = self.liquidity.remove_liquidity(provider, share)
        return {"status": "accepted", "result": result}

    # -------------------------------------------------------------------------
    # Viewer / Chain-Ansicht
    # -------------------------------------------------------------------------

    def get_block(self, height: int) -> Optional[Dict[str, Any]]:
        """
        Liefert einen Block nach Höhe.
        """
        return self.viewer.get_block_by_height(self.blockchain, height)

    def get_last_blocks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Liefert die letzten N Blöcke.
        """
        return self.viewer.get_last_blocks(self.blockchain, limit=limit)

    # -------------------------------------------------------------------------
    # Smartcontracts / VC / ECCU-Anbindung (Hook-Ebene)
    # -------------------------------------------------------------------------

    def execute_contract(
        self,
        contract_name: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Führt einen Smartcontract deterministisch aus.
        """
        handler = getattr(self.smartcontracts, contract_name, None)
        if not callable(handler):
            return {"status": "error", "reason": "unknown_contract"}

        try:
            result = handler(self, **params)
            return {"status": "ok", "result": result}
        except Exception as exc:  # bewusst generisch, VM fängt ab
            return {"status": "error", "reason": str(exc)}

    # -------------------------------------------------------------------------
    # Hilfsfunktionen für API / ai-chain.py / vm.VC
    # -------------------------------------------------------------------------

    def ping(self) -> str:
        """
        Einfache Health-Check-Funktion für API und vm.VC.
        """
        return "VMCore:OK"

    def export_state_snapshot(self) -> Dict[str, Any]:
        """
        Exportiert einen kompakten Snapshot des Systemzustands.
        Ideal für Viewer, Monitoring oder VC-Logik.
        """
        return {
            "chain": self.get_chain_info(),
            "liquidity": self.liquidity.get_pool_state()
            if hasattr(self.liquidity, "get_pool_state")
            else None,
        }


# Optional: Singleton-Instanz, falls zentral verwendet
vm_core = VMCore()
