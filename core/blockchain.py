import hashlib
import json
import time
from typing import Any

class Block:
    def __init__(self, index: int, timestamp: float, data: dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        # Der Hash des Blocks versiegelt die Daten und den validation_ap_hash permanent
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class AIChain:
    def __init__(self):
        # SOVEREIGN ADMIN DATA (DEINE IDENTITÄT)
        self.admin_address = "1JGSqDHRoEfwLaB4wh9Up9j7NgckpyYYjZ"
        self.genesis_ap_hash = "d18e84a3edbf211e65fe60a715c5bfbe264f8ed635b96058cfbf69e44b56d541"
        self.genesis_validation_ap_hash = "5b3e57a9f4de5a155f5d7d33584467942b456d6e4b02f0139b47b0291f7e626b"
        
        # Startet die Kette mit dem versiegelten Genesis-Block
        self.chain: list[Block] = [self.create_genesis_block()]
        self.state: dict[str, Any] = {}

    def create_genesis_block(self) -> Block:
        # Der absolute Nullpunkt (Admin-Hoheit)
        genesis_data = {
            "genesis": True,
            "owner": "RFOF-NETWORK",
            "address": self.admin_address,
            "ap_hash": self.genesis_ap_hash,
            "validation_ap_hash": self.genesis_validation_ap_hash,
            "license": "PZQQET-VC-ECC-2020",
            "ranking": 0  # Admin ist immer Rang 0
        }
        return Block(0, time.time(), genesis_data, "0")

    def latest(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: dict[str, Any]) -> Block:
        """
        Erstellt einen neuen Block. 
        'data' enthält den einmaligen validation_ap_hash des Users als Ranking-Anker.
        """
        prev = self.latest()
        
        # Automatische Ranking-Zuweisung durch Block-Index
        if "ranking" not in data:
            data["ranking"] = len(self.chain)
            
        block = Block(len(self.chain), time.time(), data, prev.hash)
        self.chain.append(block)
        return block
