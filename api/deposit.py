# api/deposit.py

def handle(vm, address: str, amount: float):
    """
    Interne Einzahlungslogik.
    Nutzt ausschließlich die VM-Instanz.
    Erwartet, dass vm.wallet eine deposit- und get_balance-Methode hat.
    """
    result = vm.wallet.deposit(address, amount)

    # Optional: Blockchain-Zustand persistieren (wenn deine AIChain das kann)
    if hasattr(vm.blockchain, "save_state"):
        vm.blockchain.save_state()

    return {
        "status": "ok" if result else "failed",
        "address": address,
        "amount": amount,
        "new_balance": vm.wallet.get_balance(address)
    }

