# aic_lp_token.py

class AICLPTokenExtensions:
    """
    Erweiterte Logik für den LP-Token.
    Repräsentiert Systemwert (AI + COIN + Safe).
    """

    def __init__(self, vm):
        self.vm = vm
        self.token = vm.token_aic_lp

    def reward_lp_provider(self, address: str, reward_amount: float):
        """
        Belohnt LP-Provider mit zusätzlichen LP-Token.
        """
        # Wir fügen hier die Snapshot-Logik hinzu, um den Systemwert zu erfassen
        snapshot = self.vm.get_current_safe_state() # Holt aktuelle 42% Werte
        
        self.token.mint(address, reward_amount)

    def burn_lp(self, address: str, amount: float):
        """
        Verbrennt LP-Token beim Entfernen von Liquidity.
        Optimiert für den ChainViewer-Event-Trigger.
        """
        # Sicherheitscheck: Hat der User genug LP-Token?
        if self.token.balances.get(address, 0) < amount: 
            return False

        # Abzug der Token
        self.token.balances[address] -= amount

        # Event-Trigger für den ChainViewer und die Visualisierung
        self.vm.blockchain.add_block({
            "event": "lp_burn",
            "address": address,
            "amount": amount,
            "token": "AIC-LP",
            "display_metadata": {
                "layer": 2, 
                "visibility": "shielded",
                "label": "Liquidity-Removal"
            }
        })

        return True
