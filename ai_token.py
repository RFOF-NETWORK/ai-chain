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

        # Integration in die Blockchain mit Shield-Logik
        self.vm.blockchain.add_block({
            "event": "burn",
            "token": "AI",
            "address": address,
            "amount": amount,
            "display_metadata": {"layer": 2, "visibility": "shielded"}
        })

        return True

    def reward_for_ai_compute(self, address: str, compute_units: float):
        """
        Belohnt echte Compute-Leistung mit AI-Token.
        PZQQET-Integration: Liefert Layer 3 Details für das Dashboard-Modal.
        """
        reward = compute_units * 0.01  # Beispiel: 0.01 AI pro Compute-Unit
        self.token.mint(address, reward)
        
        # Der Block-Eintrag erhält hier erweiterte Details für das Shield
        self.vm.blockchain.add_block({
            "event": "compute_reward",
            "token": "AI",
            "to": address,
            "amount": reward,
            "compute_units": compute_units,
            "display_metadata": {
                "layer": 3, 
                "visibility": "shielded",
                "shield_active": True
            }
        })
        
        # Rückgabe für das System-Handling (Welle 2 Logik)
        return {"shield_active": True, "reward": reward, "units": compute_units}
