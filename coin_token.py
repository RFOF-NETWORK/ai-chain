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
        Stabilitätslogik (ECCU-Bindung).
        Erzeugt einen Block-Event für die Markt-Stabilisierung.
        """
        self.vm.blockchain.add_block({
            "event": "coin_stabilize",
            "token": "COIN",
            "display_metadata": {
                "layer": 1, 
                "visibility": "public",
                "label": "ECCU-Peg-Sync"
            }
        })

    def pay(self, sender: str, receiver: str, amount: float):
        """
        Standard-Zahlungsfunktion.
        Verweist auf die blockchain.py Validierung über den Token-Transfer.
        """
        # Validierung: Keine Null- oder Negativ-Zahlungen (PZQQET-Standard)
        if amount <= 0:
            return False

        # Durchführung des Transfers via smartcontracts.py
        success = self.token.transfer(sender, receiver, amount)
        
        # Hinweis: Die add_block Logik ist bereits im TokenContract.transfer() 
        # integriert, welche die Layer-2 Sichtbarkeit steuert.
        
        return success
