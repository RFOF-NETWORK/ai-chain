# core/blockchain.py

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
        self.chain: list[Block] = [self.create_genesis_block()]
        self.state: dict[str, Any] = {}

    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), {"genesis": True}, "0")

    def latest(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: dict[str, Any]) -> Block:
        prev = self.latest()
        block = Block(len(self.chain), time.time(), data, prev.hash)
        self.chain.append(block)
        return block

