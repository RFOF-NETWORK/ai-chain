# api/sync.py

def handle(vm):
    """
    Synchronisiert den Blockchain-Zustand.
    Erwartet, dass vm.blockchain optional eine sync- und/oder save_state-Methode hat.
    """
    if hasattr(vm.blockchain, "sync"):
        vm.blockchain.sync()

    if hasattr(vm.blockchain, "save_state"):
        vm.blockchain.save_state()

    return {
        "status": "synced",
        "blocks": vm.viewer.get_blocks()
    }

