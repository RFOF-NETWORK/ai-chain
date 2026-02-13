# core/fees.py

class Fees:
    """
    Zentrale Gebührenlogik der AI-Chain.
    Diese Datei berechnet Fees und übergibt sie an VC.ecc,
    welches den 45/42/10/3-Split durchführt.
    """

    def __init__(self, vc_ecc):
        """
        vc_ecc: Instanz von VCECC (vc_ecc.py)
        """
        self.vc_ecc = vc_ecc

        # Standard-Gebührenraten (können später dynamisch werden)
        self.transaction_fee_rate = 0.001     # 0.1%
        self.swap_fee_rate = 0.003            # 0.3%
        self.liquidity_fee_rate = 0.0005      # 0.05%
        self.network_fee_fixed = 0.0001       # fixer kleiner Fee

    # ---------------------------------------------------------
    # Gebührenberechnung
    # ---------------------------------------------------------

    def calculate_transaction_fee(self, amount: float) -> float:
        return amount * self.transaction_fee_rate

    def calculate_swap_fee(self, amount: float) -> float:
        return amount * self.swap_fee_rate

    def calculate_liquidity_fee(self, ai_amount: float, coin_amount: float) -> float:
        return (ai_amount + coin_amount) * self.liquidity_fee_rate

    # ---------------------------------------------------------
    # Basis-Fee-Anwender (45%)
    # ---------------------------------------------------------

    def _apply_base_fee(self, vm, token: str, amount: float):
        """
        Wendet die 45%-Komponente der Fee an.
        Diese Funktion verändert NICHTS an der Safe-Logik.
        Sie nutzt NUR die bestehende Chain-Logik.
        """

        if amount <= 0:
            return

        # Basis-Event (auditierbar)
        vm.blockchain.add_block({
            "event": "fee_base",
            "token": token,
            "amount": amount
        })

        # Basis-Fee wird in AI-Chain NICHT automatisch transferiert.
        # Du kannst hier später Pool/Wallet/Chain-Logik ergänzen.
        # Aktuell: Nur Event, keine Balance-Veränderung.

    # ---------------------------------------------------------
    # Öffentliche Fee-Anwender
    # ---------------------------------------------------------

    def apply_transaction_fee(self, vm, token: str, amount: float):
        """
        Berechnet und verarbeitet eine Transaktionsgebühr.
        """
        raw_fee = self.calculate_transaction_fee(amount)

        return self.vc_ecc.process_fee(
            vm=vm,
            token=token,
            raw_fee_amount=raw_fee,
            base_fee_applier=self._apply_base_fee
        )

    def apply_swap_fee(self, vm, token: str, amount: float):
        """
        Berechnet und verarbeitet eine Swap-Gebühr.
        """
        raw_fee = self.calculate_swap_fee(amount)

        return self.vc_ecc.process_fee(
            vm=vm,
            token=token,
            raw_fee_amount=raw_fee,
            base_fee_applier=self._apply_base_fee
        )

    def apply_liquidity_fee(self, vm, ai_amount: float, coin_amount: float):
        """
        Berechnet und verarbeitet eine Liquidity-Gebühr.
        Liquidity-Fees werden dem AI/COIN-Paar zugeordnet.
        """
        raw_fee = self.calculate_liquidity_fee(ai_amount, coin_amount)

        # Liquidity-Fees betreffen beide Token → AI/COIN-Paar
        # Wir buchen die Fee anteilig auf AI.
        return self.vc_ecc.process_fee(
            vm=vm,
            token="AI",
            raw_fee_amount=raw_fee,
            base_fee_applier=self._apply_base_fee
        )

    def apply_network_fee(self, vm, token: str):
        """
        Verarbeitet eine fixe Netzwerkgebühr.
        """
        raw_fee = self.network_fee_fixed

        return self.vc_ecc.process_fee(
            vm=vm,
            token=token,
            raw_fee_amount=raw_fee,
            base_fee_applier=self._apply_base_fee
      )
      
