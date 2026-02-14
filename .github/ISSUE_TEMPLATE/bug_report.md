---
name: Bug Report
about: Melde einen Fehler in der AI‑Chain – im VC‑Layer, VMCore, BOxChain oder State‑System.
title: "[BUG] Anomalie im mechatronischen Ablauf"
labels: ["bug", "needs-triage"]
assignees: ["@RFOF-NETWORK"]

body:
  - type: markdown
    attributes:
      value: |
        ## 🧩 AI‑Chain Bug Report  
        Bitte beschreibe die Anomalie so präzise wie möglich.  
        Jeder Fehler ist ein Impuls im mechatronischen Gefüge der RFOF‑GOLDEN‑Chain.

  - type: dropdown
    id: subsystem
    attributes:
      label: Betroffenes Subsystem
      description: Welcher Teil der AI‑Chain zeigt die Anomalie?
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
      label: Beschreibung der Anomalie
      placeholder: "Was ist passiert? Welche Symptome? Welche States betroffen?"
    validations:
      required: true

  - type: textarea
    id: repro
    attributes:
      label: Schritte zur Reproduktion
      value: |
        1.
        2.
        3.
      render: bash
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Erwartetes Verhalten
      placeholder: "Wie sollte sich das System deterministisch verhalten?"
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Tatsächliches Verhalten
      placeholder: "Wie hat sich das System tatsächlich verhalten?"
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: AI‑Chain Version
      placeholder: "z. B. 0.1.0 Genesis"
    validations:
      required: true

  - type: input
    id: environment
    attributes:
      label: Umgebung
      placeholder: "Browser, OS, Gerät, Node-Version, etc."
