# UPGRADED IMPORTS FÜR PYSCRIPT & RFOF-NETWORK 🚀
import hashlib
import json
import time
from typing import Any
from js import console, document # Ermöglicht direkte Log-Ausgaben im Browser

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
        
        # Double Hashing 🔐🔐
        first_pass = hashlib.sha256(block_string).digest()
        return hashlib.sha256(first_pass).hexdigest()

class AIChain:
    def __init__(self):
        # SOVEREIGN ADMIN DATA (PZQQET-Standard)
        self.admin_address = "1JGSqDHRoEfwLaB4wh9Up9j7NgckpyYYjZ"
        self.genesis_validation_ap_hash = "5b3e57a9f4de5a155f5d7d33584467942b456d6e4b02f0139b47b0291f7e626b"
        
        # Startet die Kette mit Echtzeit-Genesis
        self.chain: list[Block] = [self.create_genesis_block()]
        console.log(f"RFOF-Chain initialisiert. Genesis Hash: {self.chain[0].hash}")

    def create_genesis_block(self) -> Block:
        """Erzeugt Block #0 in Echtzeit."""
        genesis_data = {
            "genesis": True,
            "owner": "RFOF-NETWORK",
            "address": self.admin_address,
            "validation_ap_hash": self.genesis_validation_ap_hash,
            "license": "PZQQET-VC-ECC-2020",
            "ranking": 0
        }
        return Block(0, time.time(), genesis_data, "0")

    def latest(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: dict[str, Any]) -> Block:
        """Fügt einen neuen Block hinzu und meldet dies an die Browser-Konsole."""
        prev = self.latest()
        if "ranking" not in data:
            data["ranking"] = len(self.chain)
            
        new_block = Block(len(self.chain), time.time(), data, prev.hash)
        self.chain.append(new_block)
        
        console.log(f"Neuer Block hinzugefügt: #{new_block.index} | Hash: {new_block.hash[:10]}...")
        return new_block

    def is_chain_valid(self) -> bool:
        """Kryptografische Selbstprüfung."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
                console.error(f"CHAIN INTEGRITY COMPROMISED AT BLOCK {i}!")
                return False
        return True
