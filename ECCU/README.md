ECCU/ — Electric Credit Coin Units (VC.ecc + Safe + Fond)
de‑en integrated documentation

Der ECCU/‑Ordner enthält das vollständige Electric Credit Coin Units‑System:
- VC.ecc (Fee‑Split 45/42/10/3)
- ECCU‑Safe (permanent locked value)
- ECCU‑Owner‑Balance (10% logical)
- ECCU‑Fund‑Balance (3% logical)
- ECCU‑Fond (invest/redeem, NAV)
- LICENSE‑Events für Blöcke
- Fundamentale Wertberechnung (Charts 4 & 5)

ECCU ist vollständig VM‑integriert und bildet die ökonomische Grundlage der
GoldenChain‑Komponente innerhalb der RFOF‑GOLDEN‑Architektur.

---

Inhalt

- vc_eccu.py  
  Adapter zwischen VC.ecc und VM  
  verarbeitet Fees, Safe‑Werte, Owner‑Werte, Fond‑Werte  
  erzeugt LICENSE‑Metadaten  
  liefert fundamentale Werte für UI/Charts

- eccu_fond.py  
  deterministischer ECCU‑Fonds  
  NAV‑Berechnung  
  Investieren / Einlösen  
  State‑Management

- VC.ecc (Root‑Ebene, aber logisch hier zugehörig)  
  Kernmodul für Fee‑Split, Safe‑Slots, Owner/Fonds‑Balances  
  erzeugt LICENSE‑Events  
  berechnet fundamentale Werte

---

Architekturrolle

ECCU bildet die ökonomische Schicht der AI‑Chain:

```
Transaction → Fees → VC.ecc → Safe / Owner / Fond → LICENSE‑Event → Blockchain
```

ECCU ist verantwortlich für:

- ökonomische Sicherheit (Safe‑Slots)  
- Unternehmensanteile (Owner‑Balance)  
- Fonds‑Wachstum (ECCU‑Fond)  
- fundamentale Wertberechnung  
- Lizenz‑Kontext für Blöcke  
- Integration in UI, API und Viewer  

---

ECCU‑Flow (vereinfacht)

```
applytransactionfee()
    → calculate raw fee
    → vceccu.processfee(vm, token, raw_fee)
        → VC.ecc.split_fee(45/42/10/3)
        → 45% basefeeapplier()
        → 42% lockinsafe()
        → 10% credit_owner()
        → 3% crediteccufund()
        → blockchain.addblock({ event: "feesplit", license: ... })
```

---

Wichtige Funktionen

vc_eccu.py

- processfee(vm, token, rawfeeamount, basefee_applier)  
  führt Fee‑Split aus und schreibt LICENSE‑Events

- getsafevalue(token)  
  liefert permanent gesperrte Token

- getownerbalance(token)  
  liefert 10%‑Unternehmensanteil

- geteccufund_balance(token)  
  liefert 3%‑Fondsanteil

- fundamentalvalue(token, priceincoin, cointoeccurate)  
  liefert fundamentalen Wert in ECCU

- licensemetadata(blockindex, block_hash, actor, context)  
  erzeugt LICENSE‑Metadaten für Blöcke

---

eccu_fond.py

- invest(address, amount)  
  investiert deterministisch in den Fonds

- redeem(address, shares)  
  löst Fondsanteile ein

- get_state()  
  liefert NAV, Shares, Fonds‑State

---

VC.ecc (Root)

- split_fee(amount)  
  45% base, 42% safe, 10% owner, 3% fund

- lockinsafe(token, amount)  
  permanent locked value

- credit_owner(token, amount)  
  logische Unternehmensgutschrift

- crediteccufund(token, amount)  
  logische Fondsgutschrift

- processfee(vm, token, rawfeeamount, basefee_applier)  
  vollständiger Fee‑Flow inkl. LICENSE‑Event

- getfundamentalvaluetoken(token, priceincoin, cointoeccurate)  
  fundamentaler Wert in ECCU

---

Interaktionen mit anderen Modulen

- core/fees.py  
  ruft ECCU‑Fee‑Split auf

- core/vm_core.py  
  reicht LICENSE‑Events an Blockchain weiter

- viewer/portfolio_viewer.py  
  zeigt Safe‑Werte, Fond‑Werte, Owner‑Werte

- scripts/charts.js  
  visualisiert fundamentale Werte (Charts 4 & 5)

- scripts/ui.js  
  zeigt ECCU‑Safe, Fond, LICENSE‑Events

- data/chain.json  
  speichert LICENSE‑Events und Fee‑Split‑Blöcke

---

Zusammenfassung

Der Ordner ECCU/ bildet die ökonomische, lizenzrechtliche und fundamentale
Schicht der AI‑Chain.  
Er verbindet VC.ecc, Safe, Fond, Fees, Blockchain‑Events und UI‑Visualisierung
zu einem deterministischen, auditierbaren Gesamtmodell.

