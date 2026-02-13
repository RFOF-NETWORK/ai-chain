scripts/ — UI Logic Layer (ui.js & charts.js)
de‑en integrated documentation

Der scripts/‑Ordner enthält die gesamte clientseitige Logik der AI‑Chain‑UI.
Hier werden API‑Daten geladen, UI‑Elemente aktualisiert, ECCU‑Werte visualisiert
und Chain‑Informationen in Echtzeit dargestellt.

Die Skripte sind vollständig mit:
- index.html  
- api/server.py  
- api/main.py  
- viewer/*  
- ECCU/vc_eccu.py  
- liquidity/liquidity_pool.py  
- wallet_system  
verbunden.

---

Inhalt

- ui.js  
  Zentrale UI‑Steuerung  
  Lädt API‑Daten, aktualisiert DOM‑Elemente, zeigt Portfolio, Safe, Fond,
  Chain‑History, Wallet‑Daten und ECCU‑Informationen an.

- charts.js  
  Visualisiert deterministische Daten:  
  - AI/COIN‑Preis  
  - Liquidity‑Pool‑State  
  - ECCU‑Fundamentalwerte  
  - Chain‑History  
  - Safe‑Werte  
  - Fonds‑NAV  
  Nutzt Chart‑Komponenten in index.html.

---

Architekturrolle

scripts/ bildet die UI‑Logikschicht:

`
UI (HTML/CSS)
    → scripts/ui.js (DOM, API, Events)
    → scripts/charts.js (Visualisierung)
    → api/* (JSON)
    → vm_core (Execution)
    → core/* (State)
`

Die Skripte sind verantwortlich für:

- Laden von API‑Daten  
- Aktualisieren der UI  
- Anzeigen von Wallet‑ und Portfolio‑Daten  
- Anzeigen von Chain‑Blöcken  
- Visualisieren von ECCU‑Safe, Fond, Fundamentalwerten  
- Anzeigen von Liquidity‑Pool‑Daten  
- Nutzerinteraktionen (Buttons, Inputs, Tabs)  

---

UI‑Flow (vereinfacht)

`
ui.js
    → fetch('/api/portfolio')
    → fetch('/api/chain')
    → fetch('/api/eccu/safe')
    → fetch('/api/eccu/fond')
    → update DOM

charts.js
    → fetch('/api/marketprice')
    → fetch('/api/eccu/fundamental')
    → draw charts
`

---

Wichtige Funktionen

ui.js

- loadPortfolio()  
  lädt Wallet‑, Token‑, LP‑ und ECCU‑Werte

- loadChain()  
  lädt letzte Blöcke, LICENSE‑Events, Block‑Hashes

- loadECCUSafe()  
  zeigt Safe‑Werte (42%‑Komponente)

- loadECCUFond()  
  zeigt Fonds‑State (3%‑Komponente)

- loadOwnerBalance()  
  zeigt Owner‑Werte (10%‑Komponente)

- updateUI()  
  aktualisiert DOM‑Elemente

- bindEvents()  
  verbindet Buttons, Tabs, Inputs

---

charts.js

- drawPriceChart()  
  visualisiert AI/COIN‑Preis

- drawLiquidityChart()  
  zeigt Pool‑State (AI‑Reserve, COIN‑Reserve, LP‑Supply)

- drawFundamentalChart()  
  zeigt fundamentale ECCU‑Werte (Charts 4 & 5)

- drawSafeChart()  
  visualisiert Safe‑Werte

- drawFondNAVChart()  
  zeigt NAV‑Entwicklung des ECCU‑Fonds

---

Interaktionen mit anderen Modulen

- api/server.py  
  liefert JSON‑Daten für UI

- viewer/portfolio_viewer.py  
  liefert Portfolio‑Daten

- ECCU/vc_eccu.py  
  liefert Safe‑, Fond‑ und Fundamentalwerte

- liquidity/liquidity_pool.py  
  liefert Pool‑State für Charts

- core/blockchain.py  
  liefert Chain‑History für Block‑Viewer

---

Zusammenfassung

Der Ordner scripts/ stellt die UI‑Logik und Visualisierungsschicht der
AI‑Chain bereit.  
Er verbindet API, VM, ECCU, Liquidity und Blockchain‑Daten zu einer
interaktiven, deterministischen Benutzeroberfläche.
