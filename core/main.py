# api/main.py
# Externe Server-Sicht der AI-Chain
# Startet NUR den Server, NICHT die VM.
# VM wird über vm.VC bereitgestellt.

import uvicorn
from api.server import app
from vm import get_vm_vc

def start_api():
    """
    API-Sicht starten:
    - VM NICHT neu erzeugen
    - VM NICHT verändern
    - VM NICHT initialisieren
    - Nur: bestehende VM/VC-Instanz abrufen
    """
    vm_vc = get_vm_vc()

    print("API-Server wird gestartet...")
    print("VM/VC-Instanz erkannt:")
    print(f" - Interne API: {list(vm_vc.internal_api.keys())}")
    print(" - Externe API wird über server.py bereitgestellt")

    # Server starten (extern)
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_api()

