# api/marketprice.py

def handle(vm):
    """
    Gibt den aktuellen Marktpreis aus dem Liquidity-Pool zurück.
    Erwartet, dass vm.liquidity eine get_market_price-Methode hat.
    """
    price = vm.liquidity.get_market_price()

    return {
        "status": "ok",
        "market_price": price
    }
