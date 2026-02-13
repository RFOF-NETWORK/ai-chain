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
        self.token.mint(address, reward_amount)

    def burn_lp(self, address: str, amount: float):
        """
        Verbrennt LP-Token beim Entfernen von Liquidity.
        """
        if self.token.balances.get(address, 0) < amount:
            return False

        self.token.balances[address] -= amount

        self.vm.blockchain.add_block({
            "event": "lp_burn",
            "address": address,
            "amount": amount
        })

        return True
