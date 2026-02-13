liquidity/ — Liquidity Pool Layer
de‑en integrated documentation

Der liquidity/‑Ordner enthält den deterministischen AI/COIN‑Liquidity‑Pool
der AI‑Chain.  
Er bildet die Grundlage für:

- AI/COIN‑Swaps  
- LP‑Token (AIC‑LP)  
- Pool‑State‑Berechnung  
- NAV‑Berechnung  
- Fees (0.3% Swap‑Fee, 0.05% Liquidity‑Fee)  
- Interaktion mit VC.ecc (Fee‑Split 45/42/10/3)

Der Liquidity‑Pool ist vollständig VM‑integriert und arbeitet eng mit:
- wallet_system  
- fees.py  
- aitoken / cointoken  
- aiclptoken  
- ECCU/vc_eccu.py  
zusammen.

---

Inhalt

- liquidity_pool.py  
  Implementiert den deterministischen AI/COIN‑Pool  
  (Add Liquidity, Remove Liquidity, Swap, LP‑Token‑Mint/Burn, Pool‑State).

---

Architekturrolle

Der Liquidity‑Pool ist die AMM‑Schicht der AI‑Chain:

`
UI → API → ai-chain.py → vmcore → liquiditypool → wallet_system
`

Er ist verantwortlich für:

- Berechnung von AI/COIN‑Verhältnissen  
- Ausgabe und Einlösung von AIC‑LP‑Token  
- deterministische Preisbildung  
- Swap‑Operationen  
- Weitergabe von Fees an VC.ecc  
- Bereitstellung von Pool‑Daten für Viewer und Charts  

---

Liquidity‑Flow (vereinfacht)

`
add_liquidity(provider, ai, coin)
    → wallet.has_funds()
    → pool.add()
    → mint AIC-LP
    → update pool state

remove_liquidity(provider, share)
    → burn AIC-LP
    → return AI + COIN
    → update pool state

swap()
    → calculate swap fee
    → fees.applyswapfee()
    → vcecc.processfee()
    → update reserves
`

---

Wichtige Funktionen

liquidity_pool.py

- addliquidity(provider, aiamount, coin_amount)  
  Fügt AI/COIN‑Liquidität hinzu und mintet AIC‑LP‑Token.

- remove_liquidity(provider, share)  
  Löst LP‑Anteile ein und gibt AI/COIN zurück.

- swap(fromtoken, totoken, amount)  
  Führt deterministische Swap‑Operationen aus.

- getpoolstate()  
  Liefert AI‑Reserve, COIN‑Reserve, LP‑Supply, Preise.

- calculate_price()  
  Berechnet deterministische AI/COIN‑Preise.

---

Interaktionen mit anderen Modulen

- wallet_system  
  prüft Mittel und führt Transfers aus  
- core/fees.py  
  berechnet Swap‑ und Liquidity‑Fees  
- ECCU/vc_eccu.py  
  erhält Safe/Owner/Fonds‑Anteile aus Swap‑Fees  
- viewer/portfolio_viewer.py  
  zeigt LP‑Anteile und Pool‑State in der UI  
- scripts/charts.js  
  visualisiert Preise, Pool‑State und fundamentale Werte  

---

Zusammenfassung

Der Ordner liquidity/ stellt den AMM‑Kern der AI‑Chain bereit.  
Er ist deterministisch, VM‑integriert und bildet die Grundlage für Swaps,
LP‑Token, Fees, ECCU‑Integration und UI‑Charts.

