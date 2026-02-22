# UPGRADED IMPORTS FÜR PYSCRIPT & RFOF-NETWORK
import hashlib
import json
import time
from typing import Any
from js import console, document

class Block:
    def __init__(self, index: int, timestamp: float, data: dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # Versiegelung nach PZQQET-Axiom (Double SHA-256)
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Berechnet den Double SHA-256 Hash für PZQQET-Konformität."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        
        # Double Hashing 🔐🔐 (Der Standard für RFOF-Systeme)
        first_pass = hashlib.sha256(block_string).digest()
        return hashlib.sha256(first_pass).hexdigest()

class AIChain:
    def __init__(self):
        # SOVEREIGN ADMIN DATA (PZQQET-Standard & Feste Identität)
        self.admin_address = "1JGSqDHRoEfwLaB4wh9Up9j7NgckpyYYjZ"
        # Dein fester Identifikations-Hash aus dem Genesis-Block
        self.genesis_hash = "d18e84a3edbf211e65fe60a715c5bfbe264f8ed635b96058cfbf69e44b56d541"
        self.genesis_validation_ap_hash = "5b3e57a9f4de5a155f5d7d33584467942b456d6e4b02f0139b47b0291f7e626b"
        
        # Startet die Kette mit dem versiegelten Genesis-Block
        self.chain: list[Block] = [self.create_genesis_block()]
        self.state: dict[str, Any] = {}
        
        console.log(f"RFOF-Chain initialisiert. Genesis Ident-Hash: {self.genesis_hash}")

    def create_genesis_block(self) -> Block:
        """Erzeugt Block #0 (Der absolute Nullpunkt der Admin-Hoheit)."""
        genesis_data = {
            "genesis": True,
            "owner": "RFOF-NETWORK",
            "address": self.admin_address,
            "hash": self.genesis_hash, # Feste Bindung an deine Identität
            "validation_ap_hash": self.genesis_validation_ap_hash,
            "license": "PZQQET-VC-ECC-2020",
            "ranking": 0  # Admin ist immer Rang 0
        }
        # Der berechnete Block-Hash versiegelt diese Daten permanent
        return Block(0, 1577836800.0, genesis_data, "0") # Timestamp 2020-01-01

    def latest(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: dict[str, Any]) -> Block:
        """
        Erstellt einen neuen Block. 
        'data' enthält den validation_ap_hash des Users als Ranking-Anker.
        """
        prev = self.latest()
        
        # Automatische Ranking-Zuweisung durch Block-Index (PZQQET-Wachstum)
        if "ranking" not in data:
            data["ranking"] = len(self.chain)
            
        new_block = Block(len(self.chain), time.time(), data, prev.hash)
        self.chain.append(new_block)
        
        console.log(f"Neuer Block hinzugefügt: #{new_block.index} | Hash: {new_block.hash[:12]}...")
        return new_block

    def is_chain_valid(self) -> bool:
        """Kryptografische Selbstprüfung der gesamten Kette."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Validierung des aktuellen Hashes und des Rückweises
            if current.hash != current.calculate_hash():
                console.error(f"INTEGRITY FAIL: Block {i} Hash mismatch!")
                return False
            if current.previous_hash != previous.hash:
                console.error(f"INTEGRITY FAIL: Block {i} Link broken!")
                return False
        return True

# Initialisierung der Instanz für das Frontend
rfof_chain = AIChain()
