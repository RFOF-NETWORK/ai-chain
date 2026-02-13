# smartcontracts.py

class TokenContract:
    def __init__(self, chain, name, symbol):
        self.chain = chain
        self.name = name
        self.symbol = symbol
        self.balances: dict[str, float] = {}

    def mint(self, address: str, amount: float):
        self.balances[address] = self.balances.get(address, 0) + amount
        self.chain.add_block({
            "event": "mint",
            "amount": amount,
            "to": address,
            "token": self.symbol
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
            "token": self.symbol
        })
        return True


def create_ai_chain_contracts(chain):
    ai = TokenContract(chain, "AI Token", "AI")
    coin = TokenContract(chain, "COIN Token", "COIN")
    aic_lp = TokenContract(chain, "AI-Chain LP Token", "AIC-LP")
    return ai, coin, aic_lp
