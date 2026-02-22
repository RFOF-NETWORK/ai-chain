# main.py (ROOT)
# Startpunkt der souveränen VM & Brücke zum UI-Layer

import json
from vm import VC, get_vm_vc
from core.blockchain import rfof_chain

# Brücke zur JavaScript-Umgebung (PyScript/Brython)
try:
    from js import document, console, window
    BROWSER_MODE = True
except ImportError:
    BROWSER_MODE = False

def start_vm():
    """
    Startet die VM-Welt, registriert den Genesis-Block und stellt die UI-Verbindung her.
    Keine externe API, rein souveräner und deterministischer Start.
    """
    vm_vc = get_vm_vc()

    # 1. Reine Logisierung (System-Status)
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

    # 2. UI-BRÜCKE (Aktivierung der Anzeige für Block-Viewer & Pop-Ups)
    if BROWSER_MODE:
        try:
            # Wir machen die Chain-Instanz global für JS-Skripte (ui.js) verfügbar
            window.rfof_chain_data = rfof_chain
            
            console.log("PZQQET-UI-Brücke: Genesis-Block #0 im System-Anker verifiziert.")
            
            # Falls ui.js bereits eine Update-Funktion bereitstellt, triggern wir sie
            if hasattr(window, 'update_chain_viewer'):
                window.update_chain_viewer()
                
        except Exception as e:
            console.error(f"PZQQET-UI-Fehler: {str(e)}")

    print("\nExterne API wird NICHT gestartet (Server bleibt extern).")
    print("VM läuft souverän und deterministisch.")

def get_genesis_data():
    """Gibt den Genesis-Block als JSON für das Frontend zurück (PZQQET-Standard)."""
    genesis = rfof_chain.chain[0]
    return json.dumps({
        "index": genesis.index,
        "hash": genesis.hash,
        "timestamp": genesis.timestamp,
        "data": genesis.data
    })

if __name__ == "__main__":
    start_vm()
