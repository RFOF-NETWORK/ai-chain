# liquidity/liquidity_pool.py

class LiquidityPool:
    def __init__(self, chain, token_ai, token_coin, token_aic_lp):
        self.chain = chain
        self.token_ai = token_ai
        self.token_coin = token_coin
        self.token_aic_lp = token_aic_lp

    def add_liquidity(self, address: str, ai_amount: float, coin_amount: float) -> bool:
        lp_amount = ai_amount + coin_amount

        if self.token_ai.balances.get(address, 0) < ai_amount:
            return False
        if self.token_coin.balances.get(address, 0) < coin_amount:
            return False

        self.token_ai.balances[address] -= ai_amount
        self.token_coin.balances[address] -= coin_amount

        self.token_aic_lp.mint(address, lp_amount)

        self.chain.add_block({
            "event": "lp_add",
            "lp_amount": lp_amount,
            "ai": ai_amount,
            "coin": coin_amount,
            "address": address
        })
        return True

    def get_market_price(self) -> float:
        # Minimaler Platzhalter – du kannst hier deine Formel einsetzen
        total_ai = sum(self.token_ai.balances.values())
        total_coin = sum(self.token_coin.balances.values())
        if total_ai == 0:
            return 0.0
        return total_coin / total_ai
      
