# ai-chain.py
"""
ai-chain.py
Öffentliche Python-Schnittstelle der ai_chain-Umgebung.
Ersetzt vollständig die alte web3.py-Struktur.

Aufgaben:
- Einheitlicher Einstiegspunkt für externe Module, API, Tools, VC.ecc
- Direkte Weiterleitung an VMCore (vm_core.py)
- Vereinfachte, stabile Funktionsnamen für Nutzer & API

Diese Datei enthält KEINE Blockchain-Logik.
Sie ist nur ein sauberer Wrapper.
"""

from typing import Any, Dict, Optional
import hashlib
import json
import time
from js import console, document, showSection # PyScript Bridge
from core.vm_core import vm_core

# -------------------------------------------------------------------------
# PHRASEN SYSTEM LOGIK
# -------------------------------------------------------------------------

def validate_access_phrase(phrase_list: list, target_hash: str) -> bool:
    """
    Validiert eine Wörter-Phrase gegen einen Ziel-Hash (Double SHA-256).
    Wahrt die Parität zwischen User-Eingabe und Sovereign-Admin-Status.
    """
    full_phrase = " ".join([w.strip().lower() for w in phrase_list if w])
    if not full_phrase:
        return False

    # Double SHA-256
    first_pass = hashlib.sha256(full_phrase.encode("utf-8")).digest()
    final_hash = hashlib.sha256(first_pass).hexdigest()
    
    return final_hash == target_hash

# -------------------------------------------------------------------------
# Security / integrity
# -------------------------------------------------------------------------

def check_network_integrity() -> Dict[str, Any]:
    """
    Prüft die gesamte Chain-Integrität über den vm_core.
    """
    is_valid = vm_core.blockchain.is_chain_valid()
    return {
        "status": "SECURE" if is_valid else "COMPROMISED",
        "valid": is_valid
    }

# -------------------------------------------------------------------------
# Health / System
# -------------------------------------------------------------------------

def ping() -> str:
    """
    Einfache Systemprüfung.
    """
    return vm_core.ping()


# -------------------------------------------------------------------------
# Chain-Informationen
# -------------------------------------------------------------------------

def chain_info() -> Dict[str, Any]:
    """
    Liefert Basisinformationen über die Chain.
    """
    return vm_core.get_chain_info()


def get_block(height: int) -> Optional[Dict[str, Any]]:
    """
    Liefert einen Block nach Höhe.
    """
    return vm_core.get_block(height)


def last_blocks(limit: int = 10) -> Dict[str, Any]:
    """
    Liefert die letzten N Blöcke.
    """
    return {
        "blocks": vm_core.get_last_blocks(limit)
    }


# -------------------------------------------------------------------------
# Wallet / Portfolio
# -------------------------------------------------------------------------

def wallet_balance(address: str) -> Dict[str, Any]:
    """
    Liefert alle Token-Balances eines Nutzers.
    """
    return vm_core.get_wallet_balance(address)


def portfolio(address: str) -> Dict[str, Any]:
    """
    Liefert vollständiges Portfolio (Tokens + Liquidity).
    """
    return vm_core.viewer.get_portfolio(address)


# -------------------------------------------------------------------------
# Transaktionen
# -------------------------------------------------------------------------

def send_transaction(
    from_addr: str,
    to_addr: str,
    amount: float,
    token: str = "BASE",
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Reicht eine Transaktion ein.
    """
    return vm_core.submit_transaction(
        from_addr=from_addr,
        to_addr=to_addr,
        amount=amount,
        token=token,
        metadata=metadata
    )


# -------------------------------------------------------------------------
# Liquidity
# -------------------------------------------------------------------------

def add_liquidity(provider: str, amount_ai: float, amount_coin: float) -> Dict[str, Any]:
    """
    Fügt dem Liquidity-Pool Liquidität hinzu.
    """
    return vm_core.add_liquidity(provider, amount_ai, amount_coin)


def remove_liquidity(provider: str, share: float) -> Dict[str, Any]:
    """
    Entfernt Liquidität aus dem Pool.
    """
    return vm_core.remove_liquidity(provider, share)


# -------------------------------------------------------------------------
# Smartcontracts
# -------------------------------------------------------------------------

def execute_contract(contract_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Führt einen Smartcontract deterministisch aus.
    """
    return vm_core.execute_contract(contract_name, params)


# -------------------------------------------------------------------------
# State Export
# -------------------------------------------------------------------------

def export_state() -> Dict[str, Any]:
    """
    Exportiert einen kompakten Snapshot des Systemzustands.
    Ideal für VC.ecc, Monitoring, Audits.
    """
    return vm_core.export_state_snapshot()


# -------------------------------------------------------------------------
# ECCU / VC-Hooks (werden durch vc_eccu.py erweitert)
# -------------------------------------------------------------------------

def eccu():
    """
    Platzhalter für ECCU-Funktionen.
    Wird durch vc_eccu.py erweitert.
    """
    return {"status": "eccu_module_ready"}


# -------------------------------------------------------------------------
# Ende
# -------------------------------------------------------------------------

if __name__ == "__main__":
    print("ai-chain.py Interface loaded.")
    print("Ping:", ping())
