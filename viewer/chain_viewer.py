# viewer/chain_viewer.py

class ChainViewer:
    def __init__(self, chain):
        self.chain = chain

    def get_blocks(self):
        return [{
            "index": b.index,
            "timestamp": b.timestamp,
            "data": b.data,
            "hash": b.hash,
            "previous_hash": b.previous_hash
        } for b in self.chain.chain]

    def get_portfolio(self, address: str):
        # Diese Funktion kannst du später mit Token-Infos kombinieren
        return {
            "address": address
        }
