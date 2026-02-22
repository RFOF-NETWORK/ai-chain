# viewer/chain_viewer.py

class ChainViewer:
    def __init__(self, chain):
        self.chain = chain

    def get_blocks(self):
        """
        Gibt die gesamte Kette für die Übersicht im Explorer zurück.
        PZQQET-Standard: Inklusive Layer-Informationen aus der block.json.
        """
        return [{
            "index": b.index,
            "timestamp": b.timestamp,
            "data": b.data,
            "hash": b.hash,
            "previous_hash": b.previous_hash,
            # Erweitert für die Welle-1-Sichtbarkeit
            "layer": b.data.get("display_metadata", {}).get("layer_visibility", "public")
        } for b in self.chain.chain]

    def get_render_data(self, block_index):
        """
        Bereitet spezifische Daten für die Modal-Ansicht vor.
        Nutzt den 'safe_snapshot' für detaillierte Layer-3-Sichten.
        """
        # Wir greifen auf die get_block Methode deiner blockchain.py zu
        block = self.chain.get_block(block_index)
        
        return {
            "index": block.index,
            "details": block.data.get("safe_snapshot", {}),
            "license": block.data.get("license_metadata", {}),
            "shield": True  # Aktiviert das Prai-Raw-Shield im UI 🛡️
        }

    def get_portfolio(self, address: str):
        # Hinweis: Die tiefere Logik wird in portfolio_viewer.py (Code #8) ausgelagert
        return {
            "address": address
        }
