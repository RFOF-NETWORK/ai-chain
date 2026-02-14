---
name: Feature Request
about: Schlage eine neue Funktion für die AI‑Chain vor – im VC‑Layer, VMCore, BOxChain oder State‑System.
title: "[FEATURE] Neuer Impuls im mechatronischen Gefüge"
labels: ["enhancement", "needs-review"]
assignees: ["@RFOF-NETWORK"]

body:
  - type: markdown
    attributes:
      value: |
        ## ✨ AI‑Chain Feature‑Request  
        Danke, dass du einen neuen Impuls in die RFOF‑GOLDEN‑Chain einbringst.  
        Jede Funktion ist ein Baustein im mechatronischen Organismus.

  - type: dropdown
    id: subsystem
    attributes:
      label: Betroffenes Subsystem
      description: Welcher Teil der AI‑Chain soll erweitert werden?
      options:
        - VMCore
        - VC-Layer (VC.ecc / vm.VC)
        - BOxChain
        - GoldenChain
        - Wallet-System
        - Liquidity-Pool
        - Smartcontracts
        - Frontend
        - API-Layer
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Beschreibung der Funktion
      placeholder: "Was soll die Funktion tun? Welche mechatronische Logik steckt dahinter?"
    validations:
      required: true

  - type: textarea
    id: motivation
    attributes:
      label: Warum ist das wichtig?
      placeholder: "Welches Problem löst die Funktion? Welche Souveränität oder Parität wird gestärkt?"
    validations:
      required: true

  - type: textarea
    id: implementation
    attributes:
      label: Mögliche Umsetzung
      placeholder: "Wie könnte die Funktion implementiert werden? Welche States, VC‑Module oder JSON‑Strukturen wären betroffen?"
      render: bash

  - type: input
    id: impact
    attributes:
      label: Erwarteter Einfluss
      placeholder: "z. B. Performance, Parität, State‑Reinheit, VC‑Integrität"
