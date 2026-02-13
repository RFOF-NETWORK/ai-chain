viewer/ — Chain & Portfolio Viewer Layer
de‑en integrated documentation

Der viewer/‑Ordner enthält die deterministischen Viewer‑Module der AI‑Chain.
Sie stellen lesende Funktionen bereit, ohne den Chain‑State zu verändern.
Viewer sind vollständig VM‑integriert und dienen als Datenquelle für:

- UI (index.html)
- scripts/ui.js
- scripts/charts.js
- API‑Endpunkte
- Portfolio‑Darstellungen
- Block‑ und Chain‑Explorer
- ECCU‑Visualisierung (Safe, Fond, Fundamentalwerte)

Viewer sind read‑only, deterministisch und auditierbar.

---

Inhalt

- chain_viewer.py  
  Liefert Chain‑Daten, Blöcke, Block‑History, Transaktionen, Height‑Informationen.

- portfolio_viewer.py  
  Aggregiert Wallet‑Daten, Token‑Balances, LP‑Anteile und Fond‑Werte zu einem
  vollständigen Portfolio‑Snapshot.

---

Architekturrolle

Viewer bilden die read‑only‑Schicht der VM:

`
UI → API → ai-chain.py → vm_core → viewer/* → data/chain.json
`

Sie sind verantwortlich für:

- Block‑Abfragen  
- Chain‑History  
- Portfolio‑Zusammenstellung  
- LP‑Token‑Analyse  
- Pool‑State‑Auswertung  
- ECCU‑Datenbereitstellung (über vmcore → vceccu)  

Viewer verändern niemals den Chain‑State.

---

Viewer‑Flow (vereinfacht)

`
getlastblocks(limit)
    → blockchain.getlastblocks()
    → return list of blocks

get_portfolio(address)
    → wallet.get_balance()
    → aitoken.getbalance()
    → cointoken.getbalance()
    → aiclptoken.get_balance()
    → liquidity.getpoolstate()
    → eccu.getsafevalue()
    → eccu.getfundamentalvalue()
    → return aggregated portfolio object
`

---

Wichtige Funktionen

chain_viewer.py

- getblockby_height(blockchain, height)  
  Liefert einen Block anhand seiner Höhe.

- getlastblocks(blockchain, limit)  
  Liefert die letzten N Blöcke.

- getchainoverview(blockchain)  
  Optionaler Überblick über Height, Hash, Tx‑Count.

---

portfolio_viewer.py

- get_portfolio(address)  
  Aggregiert alle Token‑ und LP‑Balances eines Nutzers.

- getliquiditypositions(address)  
  Liefert LP‑Anteile und deren Wert.

- gettokenpositions(address)  
  Liefert AI/COIN‑Token‑Balances.

- geteccupositions(address)  
  Liefert Safe‑Werte, Owner‑Werte, Fond‑Werte (über vc_eccu).

---

Interaktionen mit anderen Modulen

- core/vm_core.py  
  ruft Viewer‑Methoden auf und reicht Daten an API/UI weiter

- wallet_system  
  liefert Basis‑Balances

- liquidity_pool  
  liefert Pool‑State und LP‑Daten

- ECCU/vc_eccu.py  
  liefert Safe‑Werte, Fond‑Werte, Fundamental‑Werte

- scripts/charts.js  
  visualisiert Chain‑History, Preise, ECCU‑Werte

- scripts/ui.js  
  zeigt Portfolio, Blöcke, Safe‑Werte, Fond‑Werte an

---

Zusammenfassung

Der Ordner viewer/ stellt die read‑only‑Datenebene der AI‑Chain bereit.
Er aggregiert deterministisch alle relevanten Informationen für UI, API,
Portfolio‑Darstellungen, Chain‑Explorer und ECCU‑Visualisierung.
