# smartcontracts.py

class TokenContract:
    def __init__(self, chain, name, symbol):
        self.chain = chain
        self.name = name
        self.symbol = symbol
        self.balances: dict[str, float] = {}

    def load_genesis_balances(self, genesis_block):
        """
        PZQQET-Initialisierung: Lädt die Start-Supplys aus dem Genesis-Block.
        Stellt sicher, dass das Dashboard von Anfang an korrekte Werte zeigt.
        """
        # Abgleich mit der tokens-Struktur in block.json
        tokens = genesis_block.get("data", {}).get("tokens", {})
        if self.symbol in tokens:
            # Wir nutzen "GENESIS_RESERVE" als Key für die initiale Menge
            self.balances["GENESIS_RESERVE"] = tokens[self.symbol].get("supply", 0)

    def mint(self, address: str, amount: float):
        self.balances[address] = self.balances.get(address, 0) + amount
        self.chain.add_block({
            "event": "mint",
            "amount": amount,
            "to": address,
            "token": self.symbol,
            "display_metadata": {"layer": 1, "visibility": "public"}
        })

    def transfer(self, sender: str, receiver: str, amount: float) -> bool:
        if self.balances.get(sender, 0) < amount:
            return False
        self.balances[sender] -= amount
        self.balances[receiver] = self.balances.get(receiver, 0) + amount
        self.chain.add_block({
            "event": "transfer",
            "amount": amount,
            "from": sender,
            "to": receiver,
            "token": self.symbol,
            "display_metadata": {"layer": 2, "visibility": "shielded"}
        })
        return True


def create_ai_chain_contracts(chain, genesis_block=None):
    ai = TokenContract(chain, "AI Token", "AI")
    coin = TokenContract(chain, "COIN Token", "COIN")
    aic_lp = TokenContract(chain, "AI-Chain LP Token", "AIC-LP")
    
    # Automatischer Abgleich, falls Genesis-Daten mitgeliefert werden
    if genesis_block:
        ai.load_genesis_balances(genesis_block)
        coin.load_genesis_balances(genesis_block)
        aic_lp.load_genesis_balances(genesis_block)
        
    return ai, coin, aic_lp
