# ai_token.py

class AITokenExtensions:
    """
    Erweiterte Logik für den AI-Token.
    Bindet Energie, Compute-Leistung und Safe-Werte.
    """

    def __init__(self, vm):
        self.vm = vm
        self.token = vm.token_ai

    def burn(self, address: str, amount: float):
        """
        Verbrennt AI-Token (z.B. für Energieverbrauch).
        """
        if self.token.balances.get(address, 0) < amount:
            return False

        self.token.balances[address] -= amount

        self.vm.blockchain.add_block({
            "event": "burn",
            "token": "AI",
            "address": address,
            "amount": amount
        })

        return True

    def reward_for_ai_compute(self, address: str, compute_units: float):
        """
        Belohnt echte Compute-Leistung mit AI-Token.
        """
        reward = compute_units * 0.01  # Beispiel: 0.01 AI pro Compute-Unit
        self.token.mint(address, reward)
        return reward

