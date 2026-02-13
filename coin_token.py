# coin_token.py

class COINTokenExtensions:
    """
    Erweiterte Logik für den COIN-Token.
    Bindet Zahlungslogik und ECCU-Wertanker.
    """

    def __init__(self, vm):
        self.vm = vm
        self.token = vm.token_coin

    def stabilize(self):
        """
        Platzhalter für spätere Stabilitätslogik (ECCU-Bindung).
        """
        self.vm.blockchain.add_block({
            "event": "coin_stabilize"
        })

    def pay(self, sender: str, receiver: str, amount: float):
        """
        Standard-Zahlungsfunktion.
        """
        return self.token.transfer(sender, receiver, amount)
