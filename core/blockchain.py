# core/blockchain.py
import hashlib
import json
import time
from typing import Any
from js import console, document

# ---------------------------------------------------------
# BLOCK CLASS (PZQQET-Standard)
# ---------------------------------------------------------
class Block:
    def __init__(self, index: int, timestamp: float, data: dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # Versiegelung nach PZQQET-Axiom (Double SHA-256) 🔐🔐
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Berechnet den Double SHA-256 Hash für PZQQET-Konformität."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        
        # Double Hashing: Der Standard für RFOF-Systeme
        # Sichert die Unumkehrbarkeit und Integrität der Kette
        first_pass = hashlib.sha256(block_string).digest()
        return hashlib.sha256(first_pass).hexdigest()

# ---------------------------------------------------------
# AI-CHAIN CORE (RFOF-NETWORK Backbone)
# ---------------------------------------------------------
class AIChain:
    def __init__(self):
        # 1. SOVEREIGN ADMIN DATA & Identitäts-Check aus dem Shield
        # Zieht die Genesis-Informationen direkt aus dem geschützten HTML-Anker
        try:
            shield_data_raw = document.getElementById("prai-genesis-json").innerHTML
            shield_data = json.loads(shield_data_raw)
            g_data = shield_data["genesis_block"]
        except Exception as e:
            console.error("PZQQET-Fehler: Genesis-Anker im Shield nicht gefunden!")
            # Fallback-Sicherung: Kette wird ohne validen Anker nicht gestartet
            return

        # Festgelegte Identitätswerte für die administrative Hoheit
        self.admin_address = "1JGSqDHRoEfwLaB4wh9Up9j7NgckpyYYjZ"
        self.genesis_hash = g_data.get("hash", "d18e84a3edbf211e65fe60a715c5bfbe264f8ed635b96058cfbf69e44b56d541")
        self.genesis_validation_ap_hash = g_data.get("validation_ap_hash", "5b3e57a9f4de5a155f5d7d33584467942b456d6e4b02f0139b47b0291f7e626b")
        
        # 2. Initialisierung der Kette (Block #0 ist der absolute Ursprung)
        self.chain: list[Block] = [self.create_genesis_block()]
        self.state: dict[str, Any] = {}
        
        console.log(f"RFOF-Chain aktiv. Identität verifiziert: {self.genesis_hash[:12]}...")

    def create_genesis_block(self) -> Block:
        """Erzeugt Block #0 (Der absolute Nullpunkt der Admin-Hoheit)."""
        genesis_data = {
            "genesis": True,
            "owner": "RFOF-NETWORK",
            "address": self.admin_address,
            "hash": self.genesis_hash,
            "validation_ap_hash": self.genesis_validation_ap_hash,
            "license": "PZQQET-VC-ECC-2020",
            "ranking": 0
        }
        # Fester Timestamp 2020 für den Genesis-Anker (PZQQET-Standardzeit)
        return Block(0, 1577836800.0, genesis_data, "0")

    def latest(self) -> Block:
        """Gibt den aktuellsten Block der Kette zurück."""
        return self.chain[-1]

    def add_block(self, data: dict[str, Any]):
        """Fügt einen neuen Block zur Kette hinzu (PZQQET-konform)."""
        previous_block = self.latest()
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """Mathematische Integritätsprüfung der gesamten Kette."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Validierung der Versiegelung
            if current.hash != current.calculate_hash():
                return False
            
            # Validierung der Verkettung
            if current.previous_hash != previous.hash:
                return False
                
        return True

# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------
# Globale Instanz für den Chain Viewer und API-Anbindung
rfof_chain = AIChain()
