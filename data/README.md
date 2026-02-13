data/ — Persistent State Layer
de‑en integrated documentation

Der data/‑Ordner enthält alle persistenten Zustandsdateien der AI‑Chain.
Diese Dateien bilden die dauerhafte Speicher‑ und Audit‑Schicht des Systems.
Sie werden ausschließlich über die VM (vm_core) und die API (sync.py) verändert.

Die Daten sind deterministisch, strukturiert und vollständig auditierbar.

---

Inhalt

- chain.json  
  Persistenter Blockchain‑State  
  Enthält:
  - Blöcke  
  - Transaktionen  
  - LICENSE‑Events  
  - Fee‑Split‑Events  
  - Block‑Hashes  
  - Höhen‑Index  
  - Zeitstempel  

- users.json  
  Nutzerverwaltung  
  Enthält:
  - registrierte Nutzer  
  - Login‑Daten (gehasht)  
  - Session‑Informationen  
  - UI‑Profile  

- settings.json  
  System‑Konfiguration  
  Enthält:
  - API‑Einstellungen  
  - UI‑Konfiguration  
  - VM‑Parameter  
  - Marktpreis‑Mock‑Konfiguration  
  - Debug‑Flags  

---

Architekturrolle

Der data/‑Ordner bildet die Persistenzschicht der AI‑Chain:

`
UI → API → vm_core → core/ → data/.json
`

Er ist verantwortlich für:

- dauerhafte Speicherung des Chain‑Zustands  
- Nutzerverwaltung  
- System‑Konfiguration  
- Wiederherstellung nach Neustart  
- Auditierbarkeit aller Operationen  

---

Daten‑Flow (vereinfacht)

`
vmcore.submittransaction()
    → blockchain.add_transaction()
    → sync.save_chain() → writes chain.json

login/register/logout
    → update users.json

marketprice/sync
    → read settings.json
`

---

Wichtige Dateien

chain.json

- blocks[]  
- transactions[]  
- license_events[]  
- height  
- lastblockhash  
- total_transactions  

Wird geschrieben durch:
- core/blockchain.py  
- ECCU/vc_eccu.py (LICENSE‑Events)  
- api/sync.py  

---

users.json

- users[]  
- password_hash  
- session_token  
- created_at  

Wird geschrieben durch:
- api/register.py  
- api/login.py  
- api/logout.py  

---

settings.json

- marketpriceai  
- marketpricecoin  
- uirefreshrate  
- vm_parameters  
- debug  

Wird gelesen durch:
- api/marketprice.py  
- api/sync.py  
- scripts/ui.js  
- scripts/charts.js  

---

Interaktionen mit anderen Modulen

- core/blockchain.py  
  schreibt Blöcke in chain.json

- ECCU/vc_eccu.py  
  schreibt LICENSE‑Events in chain.json

- api/sync.py  
  lädt und speichert chain.json

- api/login/register/logout  
  schreiben users.json

- scripts/ui.js / charts.js  
  lesen settings.json über API

---

Zusammenfassung

Der Ordner data/ stellt die dauerhafte, deterministische Speicher‑ und Audit‑Schicht
der AI‑Chain bereit.  
Er speichert Blockchain‑Daten, Nutzer‑Informationen und System‑Konfigurationen und
bildet damit die Grundlage für Wiederherstellung, Auditierbarkeit und Stabilität.
