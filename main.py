# main.py (ROOT)
# Startpunkt der souveränen VM (NICHT der API, NICHT des Servers)

from vm import VC, get_vm_vc

def start_vm():
    """
    Startet die VM-Welt, ohne irgendetwas zu verändern.
    Keine API, kein Server, keine Requests.
    Nur: VM laden, VC erzeugen, Blockchain-Logik bereitstellen.
    """
    vm_vc = get_vm_vc()

    # Reine Logisierung – kein Zustand wird verändert
    print("AI-Chain VM gestartet.")
    print("VM-Kontext geladen:")
    print(f" - Blockchain: {type(vm_vc.vm.blockchain).__name__}")
    print(f" - Wallet: {type(vm_vc.vm.wallet).__name__}")
    print(f" - Liquidity: {type(vm_vc.vm.liquidity).__name__}")
    print(f" - Viewer: {type(vm_vc.vm.viewer).__name__}")
    print(f" - Smartcontracts: {vm_vc.vm.smartcontracts.__name__}")
    print(f" - Chain-State geladen: {len(vm_vc.vm.chain_state)} Einträge")

    print("\nInterne API-Funktionen registriert:")
    for name in vm_vc.internal_api.keys():
        print(f" - {name}")

    print("\nExterne API wird NICHT gestartet (Server bleibt extern).")
    print("VM läuft souverän und deterministisch.")

if __name__ == "__main__":
    start_vm()
  
