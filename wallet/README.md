wallet/ — Wallet System Layer
de‑en integrated documentation

Der wallet/‑Ordner enthält das deterministische Wallet‑System der AI‑Chain.
Es verwaltet Basis‑Balances, prüft verfügbare Mittel, führt Transfers aus und
stellt die Grundlage für Transaktionen, Liquidity‑Operationen und Fees dar.

Das Wallet‑System ist vollständig VM‑integriert und arbeitet eng mit:
- core/blockchain.py  
- core/fees.py  
- liquidity/liquidity_pool.py  
- ECCU/vc_eccu.py  
- ai-chain.py  
zusammen.

---

Inhalt

- wallet_system.py  
  Zentrales Wallet‑Modul  
  Enthält Balance‑Management, Transfer‑Logik, Validierung und deterministische
  State‑Operationen.

---

Architekturrolle

Das Wallet‑System ist die Balance‑Schicht der VM:

`
UI → API → ai-chain.py → vmcore → walletsystem → data/chain.json
`

Es ist verantwortlich für:

- Halten von Basis‑Token‑Balances  
- Prüfen, ob ein Nutzer genügend Mittel hat  
- Ausführen von Transfers (intern, deterministisch)  
- Bereitstellen von Balances für Viewer, API und UI  
- Unterstützung von Fees, Liquidity und Smartcontracts  

---

Wallet‑Flow (vereinfacht)

`
submit_transaction()
    → wallet.hasfunds(fromaddr, amount + fee)
    → wallet.transfer(fromaddr, toaddr, amount)
    → fees.applytransactionfee()
    → blockchain.add_transaction()
`

---

Wichtige Funktionen

wallet_system.py

- get_balance(address)  
  Liefert die Basis‑Balance eines Nutzers.

- set_balance(address, amount)  
  Setzt deterministisch eine Balance (intern genutzt).

- hasfunds(address, requiredamount)  
  Prüft, ob ein Nutzer genügend Mittel besitzt.

- transfer(fromaddr, toaddr, amount)  
  Führt einen deterministischen Transfer aus.

- create_wallet(address)  
  Initialisiert ein Wallet, falls nicht vorhanden.

---

Interaktionen mit anderen Modulen

- core/fees.py  
  prüft Wallet‑Mittel vor Fee‑Anwendung  
- core/vm_core.py  
  ruft Wallet‑Operationen für jede Transaktion auf  
- liquidity/liquidity_pool.py  
  nutzt Wallet‑Mittel für AI/COIN‑Liquidity  
- ECCU/vc_eccu.py  
  erhält logische Owner/Fonds‑Balances (keine direkten Transfers)  
- viewer/portfolio_viewer.py  
  zeigt Wallet‑Balances in der UI an  

---

Zusammenfassung

Der Ordner wallet/ stellt die Balance‑Grundlage der AI‑Chain bereit.
Er ist deterministisch, VM‑integriert und bildet die Basis für Transaktionen,
Liquidity‑Operationen, Fees und Portfolio‑Darstellungen.


