# core/hash-generator.py
"""
hash-generator.py
Zentrales Tool für die Double SHA-256 Generierung.
Wird genutzt, um Admin-Phrasen (48 Wörter) und Transaktions-Hashes
mechatronisch zu versiegeln.
"""

import hashlib
import sys

def double_sha256(data: str) -> str:
    """
    Erzeugt einen Double-SHA256 Hash.
    Dies ist der Standard für die AI-Chain (Welle 2 & 3).
    """
    b = data.encode("utf-8")
    # Der erste Pass hasht die Daten, der zweite Pass hasht den Digest des ersten.
    return hashlib.sha256(hashlib.sha256(b).digest()).hexdigest()

def generate_prai_shield(bip39_phrase: str, rfof_phrase: str) -> str:
    """
    Kombiniert den sichtbaren (24 Wörter) und unsichtbaren (24 Wörter) Teil
    zu einem unhackbarer Prai-Raw-Shield Hash.
    """
    combined = f"{bip39_phrase}|{rfof_phrase}"
    return double_sha256(combined)

if __name__ == "__main__":
    # Konsolen-Interface für die manuelle Notarisierung
    if len(sys.argv) < 2:
        print("--- RFOF-NETWORK HASH GENERATOR ---")
        print("Usage: python hash-generator.py \"phrase\"")
        sys.exit(1)

    input_data = sys.argv[1]
    result_hash = double_sha256(input_data)
    
    print(f"Input:  {input_data[:20]}...")
    print(f"Double-SHA256: {result_hash}")
