api/ — Internal & External API Layer
de‑en integrated documentation

Der api/‑Ordner enthält die vollständige API‑Schicht der AI‑Chain.  
Sie verbindet:

- UI (index.html, ui.js, charts.js)
- VM (vm_core)
- Wallet‑System
- Liquidity‑Pool
- ECCU‑System (VC.ecc, Safe, Fond)
- Datenhaltung (chain.json, users.json, settings.json)

Die API ist in zwei Bereiche unterteilt:

1. Interne API (für vm.VC, Systemprozesse, Sync, Marktpreise)  
2. Externe API (für UI, Clients, Browser, externe Systeme)

Alle API‑Module sind deterministisch, auditierbar und verändern den Chain‑State
nur über vm_core.

---

Inhalt

- server.py  
  Externer HTTP‑Server, Routing, JSON‑Responses, UI‑Integration.

- main.py  
  Einstiegspunkt für externe API‑Requests, verbindet server.py mit VM.

- deposit.py  
  Interne API für Einzahlungen, Wallet‑Zugänge, Balance‑Erhöhungen.

- withdraw.py  
  Interne API für Auszahlungen, Balance‑Reduktionen, Validierung.

- marketprice.py  
  Liefert deterministische Marktpreise (AI/COIN), Pool‑State, NAV‑Werte.

- sync.py  
  Synchronisiert Chain‑State, lädt chain.json, speichert Änderungen.

- wallet_api.py  
  Externe Wallet‑API für UI (Balances, Transfers, Portfolio).

- login.py / logout.py / register.py  
  Nutzerverwaltung, Session‑Handling, User‑State (users.json).

---

Architekturrolle

Die API bildet die Kommunikationsschicht der AI‑Chain:

```
UI → api/server.py → api/main.py → ai-chain.py → vm_core → core/*
```

Sie ist verantwortlich für:

- Routing von UI‑Requests  
- Bereitstellung von Portfolio‑Daten  
- Ausführen von Transaktionen  
- Liquidity‑Operationen  
- ECCU‑Safe/Fond‑Abfragen  
- LICENSE‑Event‑Ausgabe  
- Nutzerverwaltung  
- Chain‑Synchronisation  

---

API‑Flow (vereinfacht)

```
UI request
    → server.py (route)
    → main.py (dispatch)
    → ai-chain.py (public interface)
    → vm_core (execute)
    → core/blockchain (write)
    → viewer/* (read)
    → return JSON response
```

---

Wichtige Module

server.py
- route(path)  
- json_response(data)  
- handle_request(request)  

main.py
- verbindet server.py mit ai-chain.py  
- zentraler Dispatcher für alle API‑Calls  

deposit.py / withdraw.py
- Wallet‑Operationen  
- Validierung  
- deterministische Balance‑Änderungen  

marketprice.py
- liefert AI/COIN‑Preis  
- Pool‑State  
- NAV‑Werte für ECCU‑Fond  

sync.py
- lädt chain.json  
- speichert chain.json  
- VM‑State‑Synchronisation  

wallet_api.py
- liefert Portfolio  
- Wallet‑Balances  
- Token‑Balances  
- LP‑Anteile  
- ECCU‑Werte  

login/logout/register
- Nutzerverwaltung  
- Session‑Handling  
- users.json‑Integration  

---

Interaktionen mit anderen Modulen

- ai-chain.py  
  öffentliche Schnittstelle für alle API‑Operationen

- vm_core  
  führt Transaktionen, Liquidity, Contracts aus

- viewer/  
  liefert Portfolio‑ und Chain‑Daten

- ECCU/vc_eccu.py  
  liefert Safe‑Werte, Fond‑Werte, Fundamental‑Werte

- scripts/ui.js  
  ruft API‑Endpunkte auf

- scripts/charts.js  
  visualisiert API‑Daten (Chain, ECCU, Preise)

---

Zusammenfassung

Der Ordner api/ stellt die Kommunikations‑ und Integrationsschicht der
AI‑Chain bereit.  
Er verbindet UI, VM, Wallet, Liquidity, ECCU und Datenhaltung zu einem
deterministischen, auditierbaren Gesamtsystem.

