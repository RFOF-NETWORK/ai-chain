core/ — VM Core Layer
de‑en integrated documentation

Der core/‑Ordner enthält die fundamentalen Bausteine der AI‑Chain‑VM.  
Hier laufen Blockchain‑Logik, Gebührenlogik und VM‑Steuerung zusammen.  
Alle höheren Schichten (API, UI, VC.ecc, ECCU‑Fond, Tokens) greifen auf diese
Kernmodule zu.

---

Inhalt

- blockchain.py  
  Deterministische, lineare Blockchain‑Implementierung  
  Block‑Erzeugung, Hashing, Speicherung, Events, Height‑Management

- fees.py  
  Gebührenlogik (transaction, swap, liquidity, network)  
  Übergibt Fees an VC.ecc (45/42/10/3‑Split)  
  Basis‑Fee‑Applier für 45%‑Komponente

- vm_core.py  
  Zentrale VM‑Orchestrierung  
  verbindet Blockchain, Wallet, Liquidity, Viewer, Smartcontracts, Fees  
  bietet API‑kompatible Methoden für Transaktionen, Liquidity, Contracts

---

Architekturrolle

core/ bildet die unterste operative Schicht der AI‑Chain:

`
UI → API → ai-chain.py → vm_core → core/* → data/chain.json
`

- führt Transaktionen deterministisch aus  
- erzeugt Blöcke  
- berechnet Fees  
- ruft VC.ecc‑Fee‑Split auf  
- verwaltet Liquidity‑Pool  
- liefert Chain‑ und Block‑Daten an Viewer  
- stellt Smartcontract‑Ausführung bereit

---

VM‑Flow (vereinfacht)

`
submit_transaction()
    → fees.calculate()
    → fees.apply_*()
        → vcecc.processfee()
            → Safe / Owner / Fond
            → LICENSE‑Event
    → blockchain.add_transaction()
    → return tx_hash
`

---

Wichtige Funktionen

blockchain.py
- add_block(data)  
- add_transaction(tx)  
- get_height()  
- getlastblock_hash()  
- gettotaltransactions()

fees.py
- applytransactionfee(vm, token, amount)  
- applyswapfee(vm, token, amount)  
- applyliquidityfee(vm, aiamount, coinamount)  
- applynetworkfee(vm, token)

vm_core.py
- submit_transaction(from, to, amount, token)  
- add_liquidity(provider, ai, coin)  
- remove_liquidity(provider, share)  
- execute_contract(name, params)  
- getlastblocks(limit)  
- getwalletbalance(address)  
- exportstatesnapshot()

---

Verweise

- Wallet‑System → wallet/wallet_system.py  
- Liquidity‑Pool → liquidity/liquidity_pool.py  
- Viewer → viewer/  
- ECCU‑Adapter → ECCU/vc_eccu.py  
- Öffentliche Schnittstelle → ai-chain.py  
- Datenhaltung → data/chain.json

---

Zusammenfassung

Der core/‑Ordner ist das Herz der AI‑Chain.  
Er definiert die deterministische Logik, auf der GoldenChain‑Komponenten,
VC.ecc‑Fee‑Split, ECCU‑Fond, UI‑Interaktionen und API‑Operationen aufbauen.



