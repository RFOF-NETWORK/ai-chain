# liquidity/liquidity_pool.py

class LiquidityPool:
    def __init__(self, chain, token_ai, token_coin, token_aic_lp):
        self.chain = chain
        self.token_ai = token_ai
        self.token_coin = token_coin
        self.token_aic_lp = token_aic_lp

    def add_liquidity(self, address: str, ai_amount: float, coin_amount: float) -> bool:
        """
        Fügt Liquidität hinzu und mintet LP-Token.
        PZQQET-Standard: Verrechnung erfolgt 1:1 in der Summe.
        """
        lp_amount = ai_amount + coin_amount

        # Validierung der Bestände
        if self.token_ai.balances.get(address, 0) < ai_amount:
            return False
        if self.token_coin.balances.get(address, 0) < coin_amount:
            return False

        # Abzug der Basis-Token
        self.token_ai.balances[address] -= ai_amount
        self.token_coin.balances[address] -= coin_amount

        # Minting der LP-Anteile
        self.token_aic_lp.mint(address, lp_amount)

        # Registrierung in der Chain für den Explorer
        self.chain.add_block({
            "event": "lp_add",
            "lp_amount": lp_amount,
            "ai": ai_amount,
            "coin": coin_amount,
            "address": address,
            "display_metadata": {
                "layer_visibility": "public",
                "click_action": "openBlockModal"
            }
        })
        return True

    def get_market_price(self) -> float:
        """
        Berechnet den aktuellen Marktpreis basierend auf dem Verhältnis der Bestände.
        PZQQET-Präzision: 8 Dezimalstellen.
        """
        total_ai = sum(self.token_ai.balances.values())
        total_coin = sum(self.token_coin.balances.values())
        
        if total_ai == 0:
            return 0.0
            
        # Mathematische Formel für das Preis-Verhältnis
        price = total_coin / total_ai
        return round(price, 8)

    def update_ui_price(self):
        """
        Zentrale Schnittstelle für die charts.js Visualisierung.
        Speichert den Preis für die Echtzeit-Anzeige.
        """
        price = self.get_market_price()
        # In einer erweiterten Version könnte hier ein Preis-Log für Charts geführt werden
        return price
